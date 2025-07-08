import 'package:dio/dio.dart';
import 'package:ghoul/model/track.dart';
import 'package:intl/intl.dart';
import 'package:sentry_flutter/sentry_flutter.dart';

class PlaylistLogger {
  PlaylistLogger({
    required this.auth,
    required this.baseUrl,
    required this.showId,
    required this.http,
  });

  final String baseUrl;
  final String showId;
  final String auth;
  final Dio http;

  final DateFormat dateFormat = DateFormat('yyyy-MM-dd');

  String? currentPlaylistId;

  Future<void> startNewPlaylist() async {
    try {
      final headers = {
        "Authorization": "Token $auth",
      };
      final data = {
        'show': showId,
        'date': dateFormat.format(DateTime.now()),
        'notes':
            'Ghoul Testing started at ${DateFormat.jm().format(DateTime.now())}',
        'host': 'Graveyard Ghoul V2'
      };

      final response = await http.post(
        '$baseUrl/playlists/',
        data: data,
        options: Options(
          headers: headers,
        ),
      );

      currentPlaylistId = response.data['id'].toString();
    } catch (error) {
      Sentry.captureException(error);
      print('Could not create playlist');
      print(error);
    }
  }

  Future<void> submitSong(Track song) async {
    final headers = {
      "Authorization": "Token $auth",
    };

    try {
      if (currentPlaylistId == null) {
        await startNewPlaylist();
      }

      final data = {
        'playlist': currentPlaylistId,
        'playlist_id': currentPlaylistId,
        'artist': song.artist,
        'title': song.title,
        'album': song.releaseName,
        'duration': song.duration.toString(),
        'local': song.isLocal,
        'australian': song.isAustralian,
        'female': song.hasFemale,
        'newRelease': 'false' // we don't want Ghoul in Top 20+1
      };

      await http.post(
        '$baseUrl/playlistentries/',
        data: data,
        options: Options(
          headers: headers,
        ),
      );
    } catch (error) {
      Sentry.captureException(error);
      print('Could not log song');
      print(error);
    }
  }
}
