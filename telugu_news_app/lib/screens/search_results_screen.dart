import 'package:flutter/material.dart';
import '../services/api_service.dart';

class SearchResultsScreen extends StatefulWidget {
  final String query;

  const SearchResultsScreen({super.key, required this.query});

  @override
  State<SearchResultsScreen> createState() => _SearchResultsScreenState();
}

class _SearchResultsScreenState extends State<SearchResultsScreen> {
  final ApiService api = ApiService();
  String? result;
  bool loading = true;
  String? error;

  @override
  void initState() {
    super.initState();
    fetchResults();
  }

  Future<void> fetchResults() async {
    try {
      final answer = await api.searchNews(widget.query);
      setState(() {
        result = answer;
        loading = false;
      });
    } catch (e) {
      setState(() {
        error = e.toString();
        loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Search Results"),
        backgroundColor: Colors.deepPurple,
      ),
      body: Center(
        child: loading
            ? const CircularProgressIndicator()
            : error != null
                ? Text(
                    error!,
                    style: const TextStyle(color: Colors.red),
                  )
                : Padding(
                    padding: const EdgeInsets.all(16),
                    child: Text(
                      result ?? "No result",
                      style: const TextStyle(fontSize: 18),
                    ),
                  ),
      ),
    );
  }
}
