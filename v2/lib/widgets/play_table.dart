import 'package:flutter/material.dart';
import 'package:ghoul/model/message.dart';
import 'package:ghoul/model/play_item.dart';
import 'package:ghoul/model/track.dart';

class PlayTable extends StatelessWidget {
  const PlayTable({super.key, this.items = const []});

  final List<PlayItem> items;

  @override
  Widget build(BuildContext context) {
    return Table(
      defaultVerticalAlignment: TableCellVerticalAlignment.middle,
      columnWidths: const {
        0: FlexColumnWidth(),
        1: FlexColumnWidth(),
        2: IntrinsicColumnWidth(),
        3: IntrinsicColumnWidth(),
        4: IntrinsicColumnWidth(),
      },
      children: [
        TableRow(
          decoration: BoxDecoration(
            border: Border(
              bottom: BorderSide(
                width: 1,
                color: Theme.of(context).dividerColor,
              ),
            ),
          ),
          children: [
            Padding(
              padding: const EdgeInsets.only(bottom: 4.0),
              child: Text(
                'Artist',
                style: Theme.of(context)
                    .textTheme
                    .labelLarge!
                    .copyWith(fontWeight: FontWeight.bold),
              ),
            ),
            Text(
              'Title',
              style: Theme.of(context)
                  .textTheme
                  .labelLarge!
                  .copyWith(fontWeight: FontWeight.bold),
            ),
            Text(
              '🏠',
              textAlign: TextAlign.center,
              style: Theme.of(context)
                  .textTheme
                  .labelLarge!
                  .copyWith(fontWeight: FontWeight.bold),
            ),
            Text(
              '🇦🇺',
              textAlign: TextAlign.center,
              style: Theme.of(context)
                  .textTheme
                  .labelLarge!
                  .copyWith(fontWeight: FontWeight.bold),
            ),
            Text(
              '♀️',
              textAlign: TextAlign.center,
              style: Theme.of(context)
                  .textTheme
                  .labelLarge!
                  .copyWith(fontWeight: FontWeight.bold),
            ),
          ],
        ),
        ...items
            .asMap()
            .map((index, item) {
              final EdgeInsets padding =
                  index == 0 ? const EdgeInsets.only(top: 4) : EdgeInsets.zero;
              final BoxDecoration? decoration = index % 2 == 0
                  ? null
                  : BoxDecoration(color: Colors.green.shade50);
              if (item is Track) {
                Track t = item as Track;
                return MapEntry(
                    index,
                    TableRow(
                      decoration: decoration,
                      children: [
                        Padding(
                          padding: padding,
                          child: Text(t.artist.toString()),
                        ),
                        Padding(
                          padding: padding,
                          child: Text(
                            t.title.toString(),
                          ),
                        ),
                        Padding(
                          padding: padding,
                          child: Checkbox(
                            value: t.isLocal,
                            onChanged: null,
                            visualDensity: VisualDensity.compact,
                          ),
                        ),
                        Padding(
                          padding: padding,
                          child: Checkbox(
                            value: t.isAustralian,
                            onChanged: null,
                            visualDensity: VisualDensity.compact,
                          ),
                        ),
                        Padding(
                          padding: padding,
                          child: Checkbox(
                            value: t.hasFemale,
                            onChanged: null,
                            visualDensity: VisualDensity.compact,
                          ),
                        ),
                      ],
                    ));
              } else {
                Message m = item as Message;
                return MapEntry(
                    index,
                    TableRow(
                      decoration: decoration,
                      children: [
                        Padding(
                          padding: padding,
                          child: Text('**MESSAGE**'),
                        ),
                        Padding(
                          padding: padding,
                          child: Text(m.title),
                        ),
                        Text(''),
                        Text(''),
                        Text(''),
                      ],
                    ));
              }
            })
            .values
            .toList()
      ],
    );
  }
}
