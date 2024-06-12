abstract class PlayItem {
  PlayItem({
    this.localPath,
    this.duration,
  });
  String? localPath;
  Duration? duration;

  /// Returns a friendly string for printing to log files, etc.
  String getDetails();
}
