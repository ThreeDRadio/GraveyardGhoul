import 'dart:math';

import 'package:ghoul/model/play_item.dart';

class Message extends PlayItem {
  static String? basePath;

  Message({
    required this.category,
    required this.title,
    required this.code,
    required this.filename,
    super.localPath,
    super.duration = Duration.zero,
  }) {
    final catPath =
        category.toLowerCase().substring(0, min(12, category.length));
    super.localPath = '${basePath}${catPath}/${filename}';
  }

  final String category;
  final String title;
  final String code;
  final String filename;

  @override
  String getDetails() {
    return "$category - $title";
  }
}
