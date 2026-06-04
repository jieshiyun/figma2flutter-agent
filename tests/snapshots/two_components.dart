import 'package:flutter/material.dart';

abstract final class AppColors {
  static const Color ceeeeee = Color(0xFFEEEEEE);
}

abstract final class AppSpacing {
  static const double s8 = 8;
}

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Column(
          spacing: AppSpacing.s8,
          children: [
            Text(
              'Home',
            ),
            const Card(),
          ],
        ),
      ),
    );
  }
}

class Card extends StatelessWidget {
  const Card({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      color: AppColors.ceeeeee,
      child: Column(
        children: [
          Text(
            'Card body',
          ),
        ],
      ),
    );
  }
}
