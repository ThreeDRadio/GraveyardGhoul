import 'package:ghoul/model/play_item.dart';

class Track extends PlayItem {
  Track({
    required this.id,
    required this.releaseId,
    required this.trackNumber,
    required this.title,
    required this.trackArtist,
    required this.albumArtist,
    required this.releaseName,
    required this.isLocal,
    required this.isAustralian,
    required this.isDemo,
    required this.hasFemale,
    super.duration,
    super.localPath,
  });

  factory Track.deserialise({
    required Map<String, dynamic> cdInfo,
    required Map<String, dynamic> trackInfo,
    List<String> australianNames = const [],
  }) {
    return Track(
      id: trackInfo['trackid'],
      releaseId: cdInfo['id'],
      trackNumber: trackInfo['tracknum'],
      title: trackInfo['tracktitle'],
      trackArtist: trackInfo['trackartist'],
      albumArtist: cdInfo['artist'],
      releaseName: cdInfo['title'],
      isLocal: cdInfo['local'] == 2,
      isDemo: cdInfo['demo'] == 2,
      hasFemale: cdInfo['female'] == 2,
      duration: Duration(seconds: trackInfo['tracklength'] ?? 0),
      isAustralian:
          cdInfo['local'] == 2 || australianNames.contains(cdInfo['cpa']),
    );
  }

  final int id;
  final int releaseId;
  final int trackNumber;
  final String title;
  final String? trackArtist;
  final String albumArtist;
  final String releaseName;
  final bool isLocal;
  final bool isAustralian;
  final bool isDemo;
  final bool hasFemale;

  @override
  String getDetails() {
    return '$artist - $title';
  }

  String get artist {
    if (trackArtist != null && trackArtist!.isNotEmpty) {
      return trackArtist!;
    } else {
      return albumArtist;
    }
  }
}
