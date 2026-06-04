import 'package:flutter/material.dart';

abstract final class AppColors {
  static const Color c111111 = Color(0xFF111111);
}

abstract final class AppTextStyles {
  static const TextStyle s24w700 = TextStyle(fontSize: 24, fontWeight: FontWeight.w700);
}

class TestScreen extends StatelessWidget {
  const TestScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Column(
          children: [
            Text(
              'Hello',
              style: AppTextStyles.s24w700.copyWith(color: AppColors.c111111),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }
}
