import 'package:flutter/material.dart';

abstract final class AppColors {
  static const Color c0a84ff = Color(0xFF0A84FF);
  static const Color cffffff = Color(0xFFFFFFFF);
}

abstract final class AppSpacing {
  static const double s12 = 12;
  static const double s16 = 16;
}

class TestScreen extends StatelessWidget {
  const TestScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Column(
          children: [
            ElevatedButton(
              onPressed: () {},
              style: ElevatedButton.styleFrom(
                backgroundColor: AppColors.c0a84ff,
                foregroundColor: AppColors.cffffff,
                padding: EdgeInsets.symmetric(horizontal: AppSpacing.s16, vertical: AppSpacing.s12),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
              child: Text(
                'Continue',
              ),
            ),
          ],
        ),
      ),
    );
  }
}
