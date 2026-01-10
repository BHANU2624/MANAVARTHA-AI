import 'dart:convert';
import 'dart:async';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = "http://localhost:8000";

  Future<String> searchNews(String query) async {
    final uri = Uri.parse("$baseUrl/search?query=${Uri.encodeComponent(query)}");

    try {
      final response = await http
          .get(uri)
          .timeout(const Duration(seconds: 40)); // Important for RAG latency

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return data["answer"] ?? "No answer found";
      } else {
        throw Exception("Server error ${response.statusCode}");
      }
    } on TimeoutException {
      throw Exception("Request timeout. Please try again.");
    } on http.ClientException {
      throw Exception("Connection error. Ensure backend is running.");
    } catch (e) {
      throw Exception("Error: ${e.toString()}");
    }
  }
}
