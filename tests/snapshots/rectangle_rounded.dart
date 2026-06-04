import 'package:flutter/material.dart';

abstract final class AppColors {
  static const Color c0a84ff = Color(0xFF0A84FF);
}

class TestScreen extends StatelessWidget {
  const TestScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Column(
          children: [
            Container(
              width: 100,
              height: 40,
              decoration: BoxDecoration(
                color: AppColors.c0a84ff,
                borderRadius: BorderRadius.circular(8),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
