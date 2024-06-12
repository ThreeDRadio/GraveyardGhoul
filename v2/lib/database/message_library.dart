import 'package:ghoul/model/message.dart';
import 'package:postgres/postgres.dart';

class MessageLibrary {
  const MessageLibrary({
    required this.connection,
    this.stingCategories = const [],
  });

  final Connection connection;
  final List<String> stingCategories;

  Future<Message> getRandomSting() async {
    final res = await connection.execute(
        "SELECT * FROM messagelist WHERE type = ANY(@type) ORDER BY RANDOM() LIMIT 1",
        parameters: {
          'type': stingCategories,
        });
    final details = res.first.toColumnMap();

    return Message(
        category: details['type'],
        code: details['code'],
        duration: details['duration'],
        title: details['title'],
        filename: details['filename']);
  }
}
