import 'package:ghoul/model/track.dart';

abstract class FileManager {
  Future<bool> fileExists(Track track);

  Future<void> prepare(Track track);

  Future<String> getPath(Track track);
}
