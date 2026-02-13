import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;

class ApiService {
  static String get baseUrl {
    if (kIsWeb) {
      return "http://127.0.0.1:8000"; // Web
    }
    if (defaultTargetPlatform == TargetPlatform.android) {
      // Use 10.0.2.2 for Android Emulator. 
      // If using physical device, change this to your PC's IP (e.g., 192.168.x.x)
      return "http://10.0.2.2:8000"; 
    }
    return "http://127.0.0.1:8000"; // Windows/Linux/Mac
  }

  Future<String> searchNews(String query) async {
    final uri = Uri.parse("$baseUrl/search?query=$query");

    try {
      final response = await http.get(uri).timeout(const Duration(seconds: 120));

      if (response.statusCode == 200) {
        final data = json.decode(utf8.decode(response.bodyBytes)); // Handle UTF-8 safely
        return data["answer"] ?? "No answer found";
      } else {
        throw Exception("Server returned error: ${response.statusCode}");
      }
    } catch (e) {
      throw Exception("Connection Error: $e");
    }
  }
}
