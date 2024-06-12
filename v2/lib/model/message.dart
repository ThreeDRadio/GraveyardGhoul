import 'package:ghoul/model/play_item.dart';

class Message extends PlayItem {
  Message({
    required this.category,
    required this.title,
    required this.code,
    required this.filename,
    super.localPath,
    super.duration = Duration.zero,
  });

  final String category;
  final String title;
  final String code;
  final String filename;

  @override
  String getDetails() {
    return "$category - $title";
  }
}
