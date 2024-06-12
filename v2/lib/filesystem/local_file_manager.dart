import 'dart:io';
import 'package:ghoul/filesystem/file_manager.dart';
import 'package:ghoul/model/play_item.dart';
import 'package:ghoul/model/track.dart';

class LocalFileManager implements FileManager {
  const LocalFileManager({required this.basePath});

  final String basePath;

  @override
  Future<bool> fileExists(Track track) async {
    final path = await getPath(track);
    final file = File.fromUri(Uri.file(path));
    return file.exists();
  }

  @override
  Future<String> getPath(Track track) async {
    final paddedRelease = track.releaseId.toString().padLeft(7, '0');
    final paddedTrack = track.trackNumber.toString().padLeft(2, '0');
    return '$basePath/$paddedRelease-${paddedTrack}.mp3';
  }

  @override
  Future<void> prepare(PlayItem item) async {
    if (item is Track) {
      item.localPath = await getPath(item);
    }
  }
}
