import 'package:flutter/material.dart';

class ProgressBar extends StatelessWidget {
  const ProgressBar({
    super.key,
    this.progress,
    this.text,
    this.color,
    this.semanticsLabel,
    this.semanticsValue,
  });

  final double? progress;
  final String? text;
  final MaterialColor? color;
  final String? semanticsLabel;
  final String? semanticsValue;

  @override
  Widget build(BuildContext context) {
    return Stack(
      alignment: Alignment.center,
      children: [
        LinearProgressIndicator(
          borderRadius: BorderRadius.circular(4),
          minHeight: 28,
          color: color?.shade600,
          backgroundColor: color?.shade100,
          semanticsValue: semanticsValue,
          semanticsLabel: semanticsLabel,
          value: progress,
        ),
        if (text != null)
          Text(
            text!,
            style: const TextStyle(
                inherit: true,
                fontSize: 18,
                letterSpacing: 2.5,
                color: Colors.white,
                shadows: [
                  Shadow(
                      // bottomLeft
                      offset: Offset(-1.0, -1.0),
                      color: Colors.black),
                  Shadow(
                      // bottomRight
                      offset: Offset(1.0, -1.0),
                      color: Colors.black),
                  Shadow(
                      // topRight
                      offset: Offset(1.0, 1.0),
                      color: Colors.black),
                  Shadow(
                      // topLeft
                      offset: Offset(-1.0, 1.0),
                      color: Colors.black),
                ]),
          ),
      ],
    );
  }
}
