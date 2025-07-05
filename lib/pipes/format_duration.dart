String formatDuration(Duration d) {
  return d.toString().split('.').first.padLeft(8, "0").substring(4);
}
