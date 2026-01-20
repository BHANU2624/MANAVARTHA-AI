import 'dart:ui' as ui;
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'screens/home_screen.dart';

void main() {
  // 🔹 Ensure Flutter framework is ready
  WidgetsFlutterBinding.ensureInitialized();

  // 🔹 Handle early plugin messages (Flutter Web debug)
  ui.channelBuffers.setListener(
    'flutter/platform',
    (ByteData? data, ui.PlatformMessageResponseCallback? callback) {},
  );

  ui.channelBuffers.setListener(
    'flutter/lifecycle',
    (ByteData? data, ui.PlatformMessageResponseCallback? callback) {},
  );

  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Telugu News AI',
      theme: ThemeData(
        primarySwatch: Colors.deepPurple,
      ),
      home: const HomeScreen(),
    );
  }
}
