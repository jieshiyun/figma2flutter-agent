import 'package:flutter/material.dart';

abstract final class AppColors {
  static const Color cf0f0f0 = Color(0xFFF0F0F0);
}

abstract final class AppSpacing {
  static const double s4 = 4;
  static const double s8 = 8;
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
              decoration: BoxDecoration(
                color: AppColors.cf0f0f0,
                borderRadius: BorderRadius.circular(8),
              ),
              child: Padding(
                padding: EdgeInsets.all(AppSpacing.s8),
                child: Column(
                  spacing: AppSpacing.s4,
                  children: [
                    Text(
                      'Inner',
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
