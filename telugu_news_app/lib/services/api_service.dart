import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = "http://127.0.0.1:8000";

  Future<String> searchNews(String query) async {
    final uri = Uri.parse("$baseUrl/search?query=$query");

    final response = await http.get(uri);

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return data["answer"] ?? "No answer found";
    } else {
      throw Exception("Failed to fetch results");
    }
  }
}
