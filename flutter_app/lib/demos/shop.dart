import 'package:flutter/material.dart';

abstract final class AppColors {
  static const Color c111111 = Color(0xFF111111);
  static const Color c5db075 = Color(0xFF5DB075);
  static const Color ce8edf5 = Color(0xFFE8EDF5);
  static const Color ce8f5ed = Color(0xFFE8F5ED);
  static const Color cf5f0e8 = Color(0xFFF5F0E8);
  static const Color cfae8e8 = Color(0xFFFAE8E8);
  static const Color cffffff = Color(0xFFFFFFFF);
}

abstract final class AppSpacing {
  static const double s20 = 20;
  static const double s24 = 24;
  static const double s8 = 8;
}

abstract final class AppTextStyles {
  static const TextStyle inters15w600 = TextStyle(fontFamily: 'Inter', fontSize: 15, fontWeight: FontWeight.w600);
  static const TextStyle inters16w700 = TextStyle(fontFamily: 'Inter', fontSize: 16, fontWeight: FontWeight.w700);
  static const TextStyle inters28w700 = TextStyle(fontFamily: 'Inter', fontSize: 28, fontWeight: FontWeight.w700);
}

class ShopScreen extends StatelessWidget {
  const ShopScreen({super.key});

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
            spacing: AppSpacing.s20,
            children: [
              Text(
                'Shop',
                style: AppTextStyles.inters28w700.copyWith(color: AppColors.c111111, height: 1.21),
              ),
              const Row1(),
              const Row2(),
            ],
          ),
        ),
      ),
    );
  }
}

class Card extends StatelessWidget {
  const Card({super.key});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 165,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        spacing: AppSpacing.s8,
        children: [
          Container(
            width: 165,
            height: 120,
            decoration: BoxDecoration(
              color: AppColors.ce8edf5,
              borderRadius: BorderRadius.circular(12),
            ),
          ),
          Text(
            'Studio Headphones',
            style: AppTextStyles.inters15w600.copyWith(color: AppColors.c111111, height: 1.21),
          ),
          Text(
            '\$129',
            style: AppTextStyles.inters16w700.copyWith(color: AppColors.c5db075, height: 1.21),
          ),
        ],
      ),
    );
  }
}

class Card2 extends StatelessWidget {
  const Card2({super.key});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 165,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        spacing: AppSpacing.s8,
        children: [
          Container(
            width: 165,
            height: 120,
            decoration: BoxDecoration(
              color: AppColors.cfae8e8,
              borderRadius: BorderRadius.circular(12),
            ),
          ),
          Text(
            'Mini Speaker',
            style: AppTextStyles.inters15w600.copyWith(color: AppColors.c111111, height: 1.21),
          ),
          Text(
            '\$89',
            style: AppTextStyles.inters16w700.copyWith(color: AppColors.c5db075, height: 1.21),
          ),
        ],
      ),
    );
  }
}

class Row1 extends StatelessWidget {
  const Row1({super.key});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 184,
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        spacing: AppSpacing.s20,
        children: [
          const Card(),
          const Card2(),
        ],
      ),
    );
  }
}

class Card3 extends StatelessWidget {
  const Card3({super.key});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 165,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        spacing: AppSpacing.s8,
        children: [
          Container(
            width: 165,
            height: 120,
            decoration: BoxDecoration(
              color: AppColors.ce8f5ed,
              borderRadius: BorderRadius.circular(12),
            ),
          ),
          Text(
            'Smart Watch',
            style: AppTextStyles.inters15w600.copyWith(color: AppColors.c111111, height: 1.21),
          ),
          Text(
            '\$199',
            style: AppTextStyles.inters16w700.copyWith(color: AppColors.c5db075, height: 1.21),
          ),
        ],
      ),
    );
  }
}

class Card4 extends StatelessWidget {
  const Card4({super.key});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 165,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        spacing: AppSpacing.s8,
        children: [
          Container(
            width: 165,
            height: 120,
            decoration: BoxDecoration(
              color: AppColors.cf5f0e8,
              borderRadius: BorderRadius.circular(12),
            ),
          ),
          Text(
            'Action Camera',
            style: AppTextStyles.inters15w600.copyWith(color: AppColors.c111111, height: 1.21),
          ),
          Text(
            '\$349',
            style: AppTextStyles.inters16w700.copyWith(color: AppColors.c5db075, height: 1.21),
          ),
        ],
      ),
    );
  }
}

class Row2 extends StatelessWidget {
  const Row2({super.key});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 184,
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        spacing: AppSpacing.s20,
        children: [
          const Card3(),
          const Card4(),
        ],
      ),
    );
  }
}
