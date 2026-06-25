import 'package:flutter/material.dart';

abstract final class AppColors {
  static const Color c111111 = Color(0xFF111111);
  static const Color c5db075 = Color(0xFF5DB075);
  static const Color c6b7380 = Color(0xFF6B7380);
  static const Color c9ca3b0 = Color(0xFF9CA3B0);
  static const Color cd1d6db = Color(0xFFD1D6DB);
  static const Color cf7fafc = Color(0xFFF7FAFC);
  static const Color cffffff = Color(0xFFFFFFFF);
}

abstract final class AppSpacing {
  static const double s120 = 120;
  static const double s16 = 16;
  static const double s24 = 24;
}

abstract final class AppTextStyles {
  static const TextStyle inters14w500 = TextStyle(fontFamily: 'Inter', fontSize: 14, fontWeight: FontWeight.w500);
  static const TextStyle inters16w400 = TextStyle(fontFamily: 'Inter', fontSize: 16, fontWeight: FontWeight.w400);
  static const TextStyle inters16w600 = TextStyle(fontFamily: 'Inter', fontSize: 16, fontWeight: FontWeight.w600);
  static const TextStyle inters28w700 = TextStyle(fontFamily: 'Inter', fontSize: 28, fontWeight: FontWeight.w700);
}

class LoginScreen extends StatelessWidget {
  const LoginScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.cffffff,
      body: SafeArea(
        child: Padding(
          padding: EdgeInsets.fromLTRB(AppSpacing.s24, AppSpacing.s120, AppSpacing.s24, AppSpacing.s24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            mainAxisAlignment: MainAxisAlignment.start,
            spacing: AppSpacing.s16,
            children: [
              Container(
                width: 72,
                height: 72,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: AppColors.c5db075,
                ),
              ),
              Text(
                'Welcome back',
                style: AppTextStyles.inters28w700.copyWith(color: AppColors.c111111, height: 1.21),
                textAlign: TextAlign.center,
              ),
              Text(
                'Sign in to continue',
                style: AppTextStyles.inters16w400.copyWith(color: AppColors.c6b7380, height: 1.21),
                textAlign: TextAlign.center,
              ),
              SizedBox(
                width: double.infinity,
                child: const EmailField(),
              ),
              SizedBox(
                width: double.infinity,
                child: const PasswordField(),
              ),
              SizedBox(
                width: double.infinity,
                child: const SignInButton(),
              ),
              Text(
                'Forgot password?',
                style: AppTextStyles.inters14w500.copyWith(color: AppColors.c5db075, height: 1.21),
                textAlign: TextAlign.center,
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class EmailField extends StatelessWidget {
  const EmailField({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 52,
      decoration: BoxDecoration(
        color: AppColors.cf7fafc,
        borderRadius: BorderRadius.circular(10),
        border: Border.all(
          color: AppColors.cd1d6db,
          width: 1,
        ),
      ),
      child: Padding(
        padding: EdgeInsets.all(AppSpacing.s16),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.center,
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            Text(
              'Email',
              style: AppTextStyles.inters16w400.copyWith(color: AppColors.c9ca3b0, height: 1.21),
            ),
          ],
        ),
      ),
    );
  }
}

class PasswordField extends StatelessWidget {
  const PasswordField({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 52,
      decoration: BoxDecoration(
        color: AppColors.cf7fafc,
        borderRadius: BorderRadius.circular(10),
        border: Border.all(
          color: AppColors.cd1d6db,
          width: 1,
        ),
      ),
      child: Padding(
        padding: EdgeInsets.all(AppSpacing.s16),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.center,
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            Text(
              'Password',
              style: AppTextStyles.inters16w400.copyWith(color: AppColors.c9ca3b0, height: 1.21),
            ),
          ],
        ),
      ),
    );
  }
}

class SignInButton extends StatelessWidget {
  const SignInButton({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 52,
      decoration: BoxDecoration(
        color: AppColors.c5db075,
        borderRadius: BorderRadius.circular(10),
      ),
      child: Padding(
        padding: EdgeInsets.all(AppSpacing.s16),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.center,
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Sign In',
              style: AppTextStyles.inters16w600.copyWith(color: AppColors.cffffff, height: 1.21),
            ),
          ],
        ),
      ),
    );
  }
}
