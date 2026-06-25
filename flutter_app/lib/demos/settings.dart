import 'package:flutter/material.dart';

abstract final class AppColors {
  static const Color c111111 = Color(0xFF111111);
  static const Color c5db075 = Color(0xFF5DB075);
  static const Color c9ca3b0 = Color(0xFF9CA3B0);
  static const Color ce6e8eb = Color(0xFFE6E8EB);
  static const Color cf7fafc = Color(0xFFF7FAFC);
  static const Color cffffff = Color(0xFFFFFFFF);
}

abstract final class AppSpacing {
  static const double s12 = 12;
  static const double s16 = 16;
  static const double s20 = 20;
  static const double s24 = 24;
  static const double s4 = 4;
}

abstract final class AppTextStyles {
  static const TextStyle inters12w600 = TextStyle(fontFamily: 'Inter', fontSize: 12, fontWeight: FontWeight.w600);
  static const TextStyle inters16w400 = TextStyle(fontFamily: 'Inter', fontSize: 16, fontWeight: FontWeight.w400);
  static const TextStyle inters18w400 = TextStyle(fontFamily: 'Inter', fontSize: 18, fontWeight: FontWeight.w400);
  static const TextStyle inters28w700 = TextStyle(fontFamily: 'Inter', fontSize: 28, fontWeight: FontWeight.w700);
}

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.cffffff,
      body: SafeArea(
        child: Padding(
          padding: EdgeInsets.symmetric(horizontal: AppSpacing.s20, vertical: AppSpacing.s24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            mainAxisAlignment: MainAxisAlignment.start,
            spacing: AppSpacing.s12,
            children: [
              Text(
                'Settings',
                style: AppTextStyles.inters28w700.copyWith(color: AppColors.c111111, height: 1.21),
              ),
              Text(
                'ACCOUNT',
                style: AppTextStyles.inters12w600.copyWith(color: AppColors.c9ca3b0, height: 1.21),
              ),
              const AccountSection(),
              Text(
                'PREFERENCES',
                style: AppTextStyles.inters12w600.copyWith(color: AppColors.c9ca3b0, height: 1.21),
              ),
              const PreferencesSection(),
            ],
          ),
        ),
      ),
    );
  }
}

class AccountSection extends StatelessWidget {
  const AccountSection({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 350,
      decoration: BoxDecoration(
        color: AppColors.cf7fafc,
        borderRadius: BorderRadius.circular(12),
      ),
      child: Padding(
        padding: EdgeInsets.symmetric(horizontal: AppSpacing.s16, vertical: AppSpacing.s4),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            SizedBox(
              height: 48,
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.center,
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    'Profile',
                    style: AppTextStyles.inters16w400.copyWith(color: AppColors.c111111, height: 1.21),
                  ),
                  Text(
                    'Victoria',
                    style: AppTextStyles.inters16w400.copyWith(color: AppColors.c9ca3b0, height: 1.21),
                  ),
                ],
              ),
            ),
            Container(
              width: 318,
              height: 1,
              color: AppColors.ce6e8eb,
            ),
            SizedBox(
              height: 48,
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.center,
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    'Notifications',
                    style: AppTextStyles.inters16w400.copyWith(color: AppColors.c111111, height: 1.21),
                  ),
                  Text(
                    'On',
                    style: AppTextStyles.inters16w400.copyWith(color: AppColors.c5db075, height: 1.21),
                  ),
                ],
              ),
            ),
            Container(
              width: 318,
              height: 1,
              color: AppColors.ce6e8eb,
            ),
            SizedBox(
              height: 48,
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.center,
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    'Privacy',
                    style: AppTextStyles.inters16w400.copyWith(color: AppColors.c111111, height: 1.21),
                  ),
                  Text(
                    '›',
                    style: AppTextStyles.inters18w400.copyWith(color: AppColors.c9ca3b0, height: 1.21),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class PreferencesSection extends StatelessWidget {
  const PreferencesSection({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 350,
      decoration: BoxDecoration(
        color: AppColors.cf7fafc,
        borderRadius: BorderRadius.circular(12),
      ),
      child: Padding(
        padding: EdgeInsets.symmetric(horizontal: AppSpacing.s16, vertical: AppSpacing.s4),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            SizedBox(
              height: 48,
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.center,
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    'Theme',
                    style: AppTextStyles.inters16w400.copyWith(color: AppColors.c111111, height: 1.21),
                  ),
                  Text(
                    'Light',
                    style: AppTextStyles.inters16w400.copyWith(color: AppColors.c9ca3b0, height: 1.21),
                  ),
                ],
              ),
            ),
            Container(
              width: 318,
              height: 1,
              color: AppColors.ce6e8eb,
            ),
            SizedBox(
              height: 48,
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.center,
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    'Language',
                    style: AppTextStyles.inters16w400.copyWith(color: AppColors.c111111, height: 1.21),
                  ),
                  Text(
                    'English',
                    style: AppTextStyles.inters16w400.copyWith(color: AppColors.c9ca3b0, height: 1.21),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
