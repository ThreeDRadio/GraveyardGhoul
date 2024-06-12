import 'dart:math';

import 'package:ghoul/database/message_library.dart';
import 'package:ghoul/database/music_library.dart';
import 'package:ghoul/filesystem/file_manager.dart';
import 'package:ghoul/model/play_item.dart';
import 'package:ghoul/model/track.dart';

class Scheduler {
  Scheduler({
    required this.maxConsecutive,
    required this.minConsecutive,
    this.messages,
    required this.music,
    required this.fileManager,
  });

  int playCount = 0;
  int demoCount = 0;
  int localCount = 0;
  int ausCount = 0;
  int femaleCount = 0;
  int consecutiveSongs = 0;
  int totalRequests = 0;

  final int maxConsecutive;
  final int minConsecutive;

  double demoQuota = 0;
  double localQuota = 0;
  double ausQuota = 0;
  double femaleQuota = 0;

  final MusicLibrary music;
  final MessageLibrary? messages;
  final FileManager fileManager;

  Future<Track> getNextSong() {
    if (demoCount.toDouble() / (playCount) < demoQuota) {
      return music.getRandomDemo();
    } else if (localCount.toDouble() / playCount < localQuota) {
      return music.getRandomLocal();
    } else if (ausCount.toDouble() / playCount < ausQuota) {
      return music.getRandomAustralian();
    } else if (femaleCount.toDouble() / playCount < femaleQuota) {
      return music.getRandomTrack(requireFemale: true);
    } else {
      return music.getRandomTrack(requireFemale: false);
    }
  }

  Future<PlayItem?> getNextItem() async {
    PlayItem? nextItem;
    while (true) {
      if (playCount < 5) {
        nextItem = await music.getRandomTrack(requireFemale: false);
      }

      // After 5 totally random tracks, we have enough to start working towards quotas...
      else {
        // absolutely must play a sting...
        if (messages != null && consecutiveSongs >= maxConsecutive) {
          nextItem = await messages!.getRandomSting();
        } else if (consecutiveSongs >= minConsecutive &&
            maxConsecutive - consecutiveSongs > 0) {
          final coin = Random().nextInt(maxConsecutive - consecutiveSongs);
          if (messages != null && coin == 0) {
            nextItem = await messages!.getRandomSting();
          } else {
            nextItem = await getNextSong();
          }
        } else {
          nextItem = await getNextSong();
        }
      }

      if (nextItem is Track) {
        totalRequests += 1;
        if (await fileManager.fileExists(nextItem)) {
          addToPlayCount(nextItem);
          break;
        }
      } else {
        consecutiveSongs = 0;
        break;
      }
    }
    return nextItem;
  }

  void addToPlayCount(Track nextSong) {
    playCount += 1;
    consecutiveSongs += 1;

    if (nextSong.isDemo) {
      demoCount++;
    }
    if (nextSong.isLocal) {
      localCount++;
    }
    if (nextSong.isAustralian) {
      ausCount++;
    }
    if (nextSong.hasFemale) {
      femaleCount++;
    }
  }
}
