import 'package:flutter/material.dart';

import 'demos/login.dart' as login;
import 'demos/profile_posts.dart' as profile;
import 'demos/settings.dart' as settings;
import 'demos/shop.dart' as shop;
import 'demos/simple_sample.dart' as simple;

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      title: 'Figma2Flutter Demos',
      debugShowCheckedModeBanner: false,
      home: DemoGallery(),
    );
  }
}

/// One generated screen, shown as a row in the gallery.
class DemoEntry {
  const DemoEntry(this.title, this.subtitle, this.builder);

  final String title;
  final String subtitle;
  final WidgetBuilder builder;
}

/// Add a line here for each new generated demo screen.
final List<DemoEntry> demos = <DemoEntry>[
  DemoEntry(
    'Profile / Posts',
    'Complex page — avatar, segmented tabs, post list (deterministic)',
    (_) => const profile.ProfilePosts(),
  ),
  DemoEntry(
    'Simple Sample',
    'Basic auto-layout screen from figma_sample.json',
    (_) => const simple.ProfileScreen(),
  ),
  DemoEntry(
    'Login',
    'Centered form — fields/button fill width (layoutAlign)',
    (_) => const login.LoginScreen(),
  ),
  DemoEntry(
    'Shop / Product grid',
    '2×2 card grid — Row of Columns, prices, corner radius',
    (_) => const shop.ShopScreen(),
  ),
  DemoEntry(
    'Settings',
    'Grouped cards — spaceBetween rows, dividers',
    (_) => const settings.SettingsScreen(),
  ),
];

class DemoGallery extends StatelessWidget {
  const DemoGallery({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Figma2Flutter Demos')),
      body: ListView.separated(
        itemCount: demos.length,
        separatorBuilder: (_, _) => const Divider(height: 1),
        itemBuilder: (context, index) {
          final demo = demos[index];
          return ListTile(
            title: Text(demo.title),
            subtitle: Text(demo.subtitle),
            trailing: const Icon(Icons.chevron_right),
            onTap: () => Navigator.of(context).push(
              MaterialPageRoute<void>(builder: demo.builder),
            ),
          );
        },
      ),
    );
  }
}
