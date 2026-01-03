import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final TextEditingController _controller = TextEditingController();

  bool _isLoading = false;
  String? _answer;
  String? _error;

  // 🔹 Backend API URL
  final String apiBaseUrl = 'http://localhost:8000/search';

  Future<void> _fetchAnswer() async {
    final query = _controller.text.trim();
    if (query.isEmpty) return;

    setState(() {
      _isLoading = true;
      _answer = null;
      _error = null;
    });

    try {
      final uri =
          Uri.parse('$apiBaseUrl?query=${Uri.encodeComponent(query)}');

      final response = await http
          .get(uri)
          .timeout(const Duration(seconds: 40)); // Important for RAG latency

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);

        if (mounted) {
          setState(() {
            _answer = data['answer'] ?? 'సమాధానం అందుబాటులో లేదు.';
          });
        }
      } else {
        throw Exception('Server error ${response.statusCode}');
      }
    } on TimeoutException {
      if (mounted) {
        setState(() {
          _error =
              'సమాధానం రావడానికి కొంత సమయం పడుతోంది. దయచేసి వేచిచూడండి.';
        });
      }
    } on http.ClientException {
      if (mounted) {
        setState(() {
          _error = 'సర్వర్ కనెక్షన్ లోపం. దయచేసి బ్యాకెండ్ సర్వర్ నడుస్తోందో తనిఖీ చేయండి.';
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _error = 'లోపం: ${e.toString()}';
        });
      }
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Telugu News AI'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              controller: _controller,
              decoration: InputDecoration(
                hintText: 'మీ ప్రశ్న ఇక్కడ టైప్ చేయండి...',
                border: const OutlineInputBorder(),
                suffixIcon: IconButton(
                  icon: const Icon(Icons.search),
                  onPressed: _isLoading ? null : _fetchAnswer,
                ),
              ),
              onSubmitted: (_) => _fetchAnswer(),
            ),
            const SizedBox(height: 20),
            Expanded(
              child: Center(child: _buildContent()),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildContent() {
    if (_isLoading) {
      return const CircularProgressIndicator();
    }

    if (_error != null) {
      return Text(
        _error!,
        style: const TextStyle(color: Colors.red, fontSize: 16),
        textAlign: TextAlign.center,
      );
    }

    if (_answer == null) {
      return const Text(
        'ప్రశ్న అడగండి',
        style: TextStyle(fontSize: 16),
      );
    }

    return SingleChildScrollView(
      child: Text(
        _answer!,
        style: const TextStyle(fontSize: 16, height: 1.5),
      ),
    );
  }
}
