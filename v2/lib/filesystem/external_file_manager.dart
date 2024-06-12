import 'dart:io';

import 'package:dio/dio.dart';
import 'package:ghoul/filesystem/file_manager.dart';
import 'package:ghoul/model/track.dart';

/// The FileManager class is responsible for actually getting playable files
/// from entries in the catalogue.
///
/// This particular class gets songs from Three D Radio's intranet, and should
/// only be used for testing.
class ExternalFileManager implements FileManager {
  ExternalFileManager({
    required this.userId,
    required this.passwordHash,
    required this.httpPass,
    required this.httpUser,
    required this.http,
  }) {
    cookies = 'threed_id=$userId; threed_password=$passwordHash;';
  }
  final String userId;
  final String passwordHash;
  final String httpUser;
  final String httpPass;
  final Dio http;
  late String cookies;

  ///
  /// Constructs a URL for obtaining a Song from Three D's intranet.
  ///
  String constructUrl(Track song) {
    final paddedRelease = song.releaseId.toString().padLeft(7, '0');
    final paddedTrack = song.trackNumber.toString().padLeft(2, '0');
    return "https://intranet.threedradio.com/database/play/$paddedRelease-$paddedTrack-lo.mp3";
  }

  @override
  Future<bool> fileExists(Track track) async {
    final songUrl = constructUrl(track);

    final r = await http.head(
      songUrl,
      options: Options(
        headers: {
          'Cookie': cookies,
        },
      ),
    );
    return r.headers.value('Content-Type') == 'audio/mpeg';
  }

  @override
  Future<String> getPath(Track track) async {
    return "/tmp/${track.id}.mp3";
  }

  @override
  Future<void> prepare(Track track) async {
    final songUrl = constructUrl(track);
    final localPath = await getPath(track);

    http.download(
      songUrl,
      localPath,
      options: Options(
        headers: {
          'Cookie': cookies,
        },
      ),
    );
    track.localPath = localPath;
  }
}
