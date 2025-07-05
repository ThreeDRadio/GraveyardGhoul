import 'dart:io';

import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:ghoul/database/message_library.dart';
import 'package:ghoul/database/music_library.dart';
import 'package:ghoul/filesystem/external_file_manager.dart';
import 'package:ghoul/filesystem/file_manager.dart';
import 'package:ghoul/filesystem/local_file_manager.dart';
import 'package:ghoul/logger.dart';
import 'package:ghoul/model/message.dart';
import 'package:ghoul/model/play_item.dart';
import 'package:ghoul/model/track.dart' as song;
import 'package:ghoul/pipes/format_duration.dart';
import 'package:ghoul/scheduler.dart';
import 'package:ghoul/widgets/panel.dart';
import 'package:ghoul/widgets/play_table.dart';
import 'package:ghoul/widgets/progress_bar.dart';
import 'package:postgres/postgres.dart';
import 'package:yaml/yaml.dart';
import 'package:media_kit/media_kit.dart';
import 'package:rxdart/rxdart.dart';

void main(List<String> args) async {
  WidgetsFlutterBinding.ensureInitialized();
  MediaKit.ensureInitialized();

  final configFile =
      await File('/Users/Michael/code/ThreeD/GraveyardGhoul/v2/config.yaml')
          .readAsString();
  final config = loadYaml(configFile);

  final libraryDb = await Connection.open(
    Endpoint(
      host: config['music_database']['host'],
      username: config['music_database']['user'],
      password: config['music_database']['password'],
      database: config['music_database']['database'],
    ),
    settings: const ConnectionSettings(
      sslMode: SslMode.disable,
    ),
  );

  Connection? messageDB;
  MessageLibrary? messages;

  try {
    messageDB = await Connection.open(
      Endpoint(
        host: config['msg_database']['host'],
        username: config['msg_database']['user'],
        password: config['msg_database']['password'],
        database: config['msg_database']['database'],
      ),
      settings: const ConnectionSettings(
        sslMode: SslMode.disable,
      ),
    );

    messages = MessageLibrary(
      connection: messageDB,
      stingCategories:
          List<String>.from(config['messages']['sting_categories'] as YamlList),
    );
  } catch (err) {
    print('No message library configured');
  }

  Message.basePath = config['file_manager']['message_base_path'];

  late FileManager fm;
  switch (config['file_manager']['mode']) {
    case 'external':
      fm = ExternalFileManager(
        userId: config['file_manager']['user_id'].toString(),
        passwordHash: config['file_manager']['password'],
        httpUser: config['file_manager']['httpUser'],
        httpPass: config['file_manager']['httpPass'],
        http: Dio(),
      );
      break;
    case 'local':
      fm = LocalFileManager(
        basePath: config['file_manager']['music_base_path'],
      );
      break;
    default:
      throw Exception('unsupported file manager');
  }
  final library = MusicLibrary(
    connection: libraryDb,
    maxSongLength: config['music']['max_song_length'],
    australianNames:
        List<String>.from((config['music']['aus_names'] as YamlList)),
  );

  final logger = PlaylistLogger(
    auth: config['logger']['auth'],
    baseUrl: config['logger']['baseURL'],
    showId: config['logger']['showID'],
    http: Dio(),
  );

  final scheduler = Scheduler(
    maxConsecutive: config['scheduler']['consecutive_songs']['max'],
    minConsecutive: config['scheduler']['consecutive_songs']['min'],
    messages: messages,
    music: library,
    fileManager: fm,
  );
  scheduler.demoQuota = (config['scheduler']['quotas']['demo']);
  scheduler.localQuota = (config['scheduler']['quotas']['local']);
  scheduler.ausQuota = (config['scheduler']['quotas']['aus']);
  scheduler.femaleQuota = (config['scheduler']['quotas']['female']);

  final Player player = Player();
  runApp(Ghoul(
    player: player,
    scheduler: scheduler,
    manager: fm,
    logger: logger,
  ));
}

enum PlaybackState {
  initialising,
  idle,
  playing,
  paused,
  stopping,
}

class Ghoul extends StatelessWidget {
  const Ghoul({
    super.key,
    required this.scheduler,
    required this.player,
    required this.manager,
    this.logger,
  });

  final Scheduler scheduler;
  final Player player;
  final FileManager manager;
  final PlaylistLogger? logger;

  // This widget is Vjthe root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Graveyard Ghoul',
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.green,
          brightness: Brightness.light,
        ),
      ),
      home: MainScreen(
        scheduler: scheduler,
        player: player,
        manager: manager,
        logger: logger,
      ),
    );
  }
}

class MainScreen extends StatefulWidget {
  const MainScreen({
    super.key,
    required this.scheduler,
    required this.player,
    required this.manager,
    this.logger,
  });

  final Scheduler scheduler;
  final Player player;
  final FileManager manager;
  final PlaylistLogger? logger;

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  /// The upcoming things to play
  final List<PlayItem> upcoming = [];

  /// The thing that is currently playing
  PlayItem? current;

  /// History
  final List<PlayItem> completed = [];

  /// Whether we want to be playing
  PlaybackState playbackState = PlaybackState.initialising;

  @override
  void initState() {
    super.initState();

    initialPlaylistFill();

    widget.player.stream.completed
        .where((complete) => complete == true)
        .forEach((complete) {
      if (complete && playbackState == PlaybackState.playing) {
        next();
      } else {
        setState(() {
          playbackState = PlaybackState.idle;
          current = null;
        });
      }
    });
    widget.player.stream.error.forEach((error) {
      stderr.write('Could not play ${current?.getDetails()}. $error\n');
      if (playbackState == PlaybackState.playing) {
        next();
      } else {
        setState(() {
          playbackState = PlaybackState.idle;
          current = null;
        });
      }
    });
  }

  initialPlaylistFill() async {
    await fillPlaylist();
    setState(() {
      playbackState = PlaybackState.idle;
    });
  }

  fillPlaylist() async {
    while (upcoming.length < 3) {
      try {
        final item = await widget.scheduler.getNextItem();
        if (item is song.Track) {
          await widget.manager.prepare(item);
        }
        if (item != null) {
          upcoming.add(item);
        }
      } catch (err) {
        print(err);
      }
    }
  }

  /// Start's playback
  void start() async {
    final item = upcoming.first;
    completed.add(item);
    if (item is song.Track) {
      widget.logger?.submitSong(item);
    }
    upcoming.remove(item);
    widget.player.open(Media(item.localPath!));
    await fillPlaylist();
    setState(() {
      current = item;
      playbackState = PlaybackState.playing;
    });
  }

  /// Start playing the next song, skipping the current one if playing
  next() async {
    final item = upcoming.first;
    widget.player.open(Media(item.localPath!));
    current = item;
    completed.add(item);
    upcoming.remove(item);
    if (item is song.Track) {
      widget.logger?.submitSong(item);
    }
    await fillPlaylist();
    setState(() {
      playbackState = PlaybackState.playing;
    });
  }

  /// Stop playback after the current song
  void stop() {
    setState(() {
      playbackState = PlaybackState.stopping;
    });
  }

  void pause() {
    widget.player.pause();
    setState(() {
      playbackState = PlaybackState.paused;
    });
  }

  void resume() {
    widget.player.play();
    setState(() {
      playbackState = PlaybackState.playing;
    });
  }

  String getMessage() {
    late String message;
    switch (playbackState) {
      case PlaybackState.initialising:
        message = 'Preparing';
        break;
      case PlaybackState.idle:
        message = 'Ready';
        break;
      case PlaybackState.playing:
      case PlaybackState.paused:
        message = current?.getDetails() ?? 'Playing';
        break;
      case PlaybackState.stopping:
        message = 'STOPPING AT END';
        break;
    }
    return message;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(8.0),
        child: Column(
          children: [
            Panel(
              label: const Text('Now Playing'),
              child: Column(
                children: [
                  Text(
                    getMessage(),
                    style: Theme.of(context).textTheme.bodyLarge!.copyWith(
                        color: playbackState == PlaybackState.stopping
                            ? Colors.red.shade600
                            : null),
                    textAlign: TextAlign.center,
                  ),
                  Padding(
                    padding: const EdgeInsets.symmetric(vertical: 16.0),
                    child: StreamBuilder(
                      stream: widget.player.stream.position
                          .throttleTime(const Duration(milliseconds: 100)),
                      builder: (context, position) => ProgressBar(
                        color: playbackState != PlaybackState.stopping
                            ? null
                            : Colors.red,
                        semanticsValue: position.data.toString(),
                        semanticsLabel: 'Track Progress',
                        progress: (position.data?.inMilliseconds ?? 0) > 0
                            ? position.data!.inMilliseconds /
                                widget.player.state.duration.inMilliseconds
                            : playbackState == PlaybackState.initialising
                                ? null
                                : 0,
                        text: position.hasData
                            ? '${formatDuration(position.data!)}  / ${formatDuration(widget.player.state.duration)}'
                            : null,
                      ),
                    ),
                  ),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      IconButton(
                        onPressed: playbackState == PlaybackState.playing
                            ? pause
                            : playbackState == PlaybackState.paused
                                ? resume
                                : playbackState == PlaybackState.stopping
                                    ? resume
                                    : start,
                        icon: Icon(playbackState == PlaybackState.playing
                            ? Icons.pause
                            : Icons.play_arrow),
                        tooltip: playbackState == PlaybackState.playing
                            ? 'Pause'
                            : 'Resume',
                      ),
                      IconButton(
                        onPressed: playbackState == PlaybackState.playing
                            ? next
                            : null,
                        icon: const Icon(Icons.skip_next),
                        tooltip: 'Skip to next item',
                      ),
                      IconButton(
                        onPressed: stop,
                        icon: const Icon(Icons.stop),
                        tooltip: 'Stop at end of this track',
                      ),
                    ],
                  ),
                ],
              ),
            ),
            Padding(
              padding: const EdgeInsets.only(top: 16.0),
              child: Panel(
                label: const Text('Up Next'),
                child: SingleChildScrollView(
                  child: PlayTable(
                    items: upcoming,
                  ),
                ),
              ),
            ),
            Expanded(
              child: Padding(
                padding: const EdgeInsets.only(top: 16.0),
                child: Panel(
                  label: const Text('History'),
                  child: SizedBox.expand(
                    child: SingleChildScrollView(
                        child: PlayTable(items: completed)),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
