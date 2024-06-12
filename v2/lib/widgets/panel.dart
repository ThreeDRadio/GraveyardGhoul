import 'package:flutter/material.dart';

class Panel extends StatelessWidget {
  const Panel({super.key, required this.child, required this.label});

  final Widget child;
  final Widget label;

  @override
  Widget build(BuildContext context) {
    return InputDecorator(
      decoration: InputDecoration(
        label: label,
        enabledBorder: OutlineInputBorder(
          borderSide: BorderSide(),
        ),
      ),
      child: child,
    );
  }
}
