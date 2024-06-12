import 'package:ghoul/model/track.dart';
import 'package:postgres/postgres.dart';

class MusicLibrary {
  const MusicLibrary({
    required this.connection,
    required this.maxSongLength,
    this.australianNames = const [],
  });

  Future<Track> getRandomDemo() async {
    final cdRes = await connection.execute(
        "SELECT * FROM cd WHERE demo = '2' AND ghoul_approved = true ORDER BY RANDOM() LIMIT 1");

    final cd = cdRes.first.toColumnMap();

    final trackRes = await connection.execute(
        Sql.named(
            "SELECT * from cdtrack WHERE cdid = @cdid AND tracklength <= @maxLength ORDER BY RANDOM() LIMIT 1;"),
        parameters: {
          'cdid': cd['id'],
          'maxLength': maxSongLength,
        });

    final track = trackRes.first.toColumnMap();
    return Track.deserialise(
      cdInfo: cd,
      trackInfo: track,
      australianNames: this.australianNames,
    );
  }

  Future<Track> getRandomLocal() async {
    final cdRes = await connection.execute(
        "SELECT * FROM cd WHERE local = '2' AND ghoul_approved = true ORDER BY RANDOM() LIMIT 1");

    final cd = cdRes.first.toColumnMap();

    final trackRes = await connection.execute(
        Sql.named(
            "SELECT * from cdtrack WHERE cdid = @cdid AND tracklength <= @maxLength ORDER BY RANDOM() LIMIT 1;"),
        parameters: {
          'cdid': cd['id'],
          'maxLength': maxSongLength,
        });

    final track = trackRes.first.toColumnMap();
    return Track.deserialise(
      cdInfo: cd,
      trackInfo: track,
      australianNames: australianNames,
    );
  }

  Future<Track> getRandomAustralian() async {
    final cdRes = await connection.execute(
        Sql.named(
            "SELECT * FROM cd WHERE cpa = ANY( @australianNames ) AND ghoul_approved = true ORDER BY RANDOM() LIMIT 1"),
        parameters: {
          'australianNames': australianNames,
        });

    final cd = cdRes.first.toColumnMap();

    final trackRes = await connection.execute(
        Sql.named(
            "SELECT * from cdtrack WHERE cdid = @cdid AND tracklength <= @maxLength ORDER BY RANDOM() LIMIT 1;"),
        parameters: {
          'cdid': cd['id'],
          'maxLength': maxSongLength,
        });

    final track = trackRes.first.toColumnMap();
    return Track.deserialise(
      cdInfo: cd,
      trackInfo: track,
      australianNames: australianNames,
    );
  }

  Future<Track> getRandomTrack({required bool requireFemale}) async {
    late Result cdRes;
    if (requireFemale == true) {
      cdRes = await connection.execute(
          "SELECT * FROM cd WHERE female = '2' AND ghoul_approved = true ORDER BY RANDOM() LIMIT 1");
    } else {
      cdRes = await connection.execute(
          "SELECT * FROM cd WHERE ghoul_approved = true ORDER BY RANDOM() LIMIT 1");
    }
    final cd = cdRes.first.toColumnMap();

    final trackRes = await connection.execute(
        Sql.named(
          "SELECT * from cdtrack WHERE cdid = @cdid AND tracklength <= @maxLength ORDER BY RANDOM() LIMIT 1;",
        ),
        parameters: {
          'cdid': cd['id'],
          'maxLength': maxSongLength,
        });

    final track = trackRes.first.toColumnMap();
    return Track.deserialise(
      cdInfo: cd,
      trackInfo: track,
      australianNames: australianNames,
    );
  }

  final Connection connection;
  final int maxSongLength;
  final List<String> australianNames;
}
