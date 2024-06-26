import 'package:dio/dio.dart';
import 'package:ghoul/model/track.dart';
import 'package:intl/intl.dart';

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

  late String currentPlaylistId;

  Future<String> startNewPlaylist() async {
    final headers = {
      "Authorization": "Token $auth",
    };
    final data = {
      'show': showId,
      'date': DateTime.now().toIso8601String(),
      'notes': 'Ghoul started at ${DateFormat.jm().format(DateTime.now())}',
      'host': 'Graveyard Ghoul'
    };

    final response = await http.post(
      '$baseUrl/playlists/',
      data: data,
      options: Options(
        headers: headers,
      ),
    );

    currentPlaylistId = response.data['id'];
    return currentPlaylistId;
  }

  Future<void> submitSong(Track song) async {
    final headers = {
      "Authorization": "Token $auth",
    };

    final data = {
      'playlist': currentPlaylistId,
      'playlist_id': currentPlaylistId,
      'artist': song.artist,
      'title': song.title,
      'album': song.releaseName,
      'duration': song.duration,
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
  }
}
