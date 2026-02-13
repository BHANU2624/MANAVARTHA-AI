import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import '../services/api_service.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final TextEditingController _controller = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  
  // List of chat messages (simulated for now, could be persistent)
  final List<Map<String, String>> _messages = [];

  bool _isLoading = false;

  Future<void> _fetchAnswer() async {
    final query = _controller.text.trim();
    if (query.isEmpty) return;

    setState(() {
      _messages.add({"role": "user", "content": query});
      _isLoading = true;
    });
    _controller.clear();
    _scrollToBottom();

    try {
      final uri = Uri.parse('${ApiService.baseUrl}/search?query=${Uri.encodeComponent(query)}');

      final response = await http
          .get(uri)
          .timeout(const Duration(seconds: 40)); 

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final answer = data['answer'] ?? 'సమాధానం అందుబాటులో లేదు.';
        
        if (mounted) {
          setState(() {
            _messages.add({"role": "bot", "content": answer});
          });
        }
      } else {
        throw Exception('Server error ${response.statusCode}');
      }
    } catch (e) {
      if (mounted) {
        String errorMessage = 'క్షమించండి, సర్వర్‌లో సమస్య ఉంది. దయచేసి మళ్లీ ప్రయత్నించండి.';
        if (e.toString().contains('SocketException')) {
           errorMessage = 'కనెక్షన్ లోపం. బ్యాకెండ్ సర్వర్ రన్ అవుతుందని నిర్ధారించుకోండి. (Error: $e)';
        }
        
        setState(() {
          _messages.add({"role": "bot", "content": errorMessage});
        });
      }
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
        _scrollToBottom();
      }
    }
  }
  
  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Row(
          children: [
             Text('📰 '),
             Text('Telugu News AI', style: TextStyle(fontWeight: FontWeight.bold)),
          ],
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () {
              setState(() {
                _messages.clear();
              });
            },
          )
        ],
      ),
      body: Column(
        children: [
          Expanded(
            child: _messages.isEmpty
                ? Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(Icons.newspaper, size: 80, color: Colors.grey[400]),
                        const SizedBox(height: 20),
                        Text(
                          'మీ ప్రశ్న ఇక్కడ అడగండి...', 
                          style: TextStyle(color: Colors.grey[600], fontSize: 18),
                        ),
                      ],
                    ),
                  )
                : ListView.builder(
                    controller: _scrollController,
                    padding: const EdgeInsets.all(16),
                    itemCount: _messages.length + (_isLoading ? 1 : 0),
                    itemBuilder: (context, index) {
                      if (index == _messages.length) {
                        return const Align(
                          alignment: Alignment.centerLeft,
                          child: Padding(
                            padding: EdgeInsets.all(8.0),
                            child: CircularProgressIndicator(),
                          ),
                        );
                      }
                      
                      final msg = _messages[index];
                      final isUser = msg['role'] == "user";
                      return _ChatBubble(
                        content: msg['content']!, 
                        isUser: isUser,
                      );
                    },
                  ),
          ),
          _buildInputArea(),
        ],
      ),
    );
  }
  
  Widget _buildInputArea() {
    return Container(
      padding: const EdgeInsets.all(16),
      color: Colors.white,
      child: Row(
        children: [
          Expanded(
            child: TextField(
              controller: _controller,
              decoration: const InputDecoration(
                hintText: 'ప్రశ్న అడగండి...',
              ),
              onSubmitted: (_) => _fetchAnswer(),
            ),
          ),
          const SizedBox(width: 10),
          FloatingActionButton(
            backgroundColor: Theme.of(context).primaryColor,
            onPressed: _isLoading ? null : _fetchAnswer,
            child: _isLoading 
              ? const SizedBox(width: 24, height: 24, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2)) 
              : const Icon(Icons.send, color: Colors.white),
          ),
        ],
      ),
    );
  }
}

class _ChatBubble extends StatelessWidget {
  final String content;
  final bool isUser;

  const _ChatBubble({required this.content, required this.isUser});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Align(
      alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.symmetric(vertical: 6),
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.75),
        decoration: BoxDecoration(
          color: isUser ? theme.primaryColor : theme.colorScheme.secondary,
          borderRadius: BorderRadius.only(
            topLeft: const Radius.circular(16),
            topRight: const Radius.circular(16),
            bottomLeft: isUser ? const Radius.circular(16) : Radius.zero,
            bottomRight: isUser ? Radius.zero : const Radius.circular(16),
          ),
          boxShadow: [
             BoxShadow(color: Colors.black.withOpacity(0.05), blurRadius: 4, offset: const Offset(0, 2))
          ],
        ),
        child: Text(
          content,
          style: TextStyle(
            color: isUser ? Colors.white : const Color(0xFFD1FFD6),
            fontSize: 16,
            height: 1.4,
          ),
        ),
      ),
    );
  }
}
