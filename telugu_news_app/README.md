# Telugu News App

A cross-platform Flutter application for the MANAVARTHA-AI Telugu News Question Answering system.

## Overview

This Flutter app provides a modern, responsive user interface for asking questions about Telugu news and receiving AI-generated answers based on a RAG (Retrieval-Augmented Generation) system.

## Features

- **Clean UI**: Modern Material Design interface
- **Real-time Search**: Ask questions and get instant answers
- **Multilingual Support**: Ask questions in Telugu, English, or Romanized Telugu
- **Error Handling**: Proper error messages and loading states
- **Cross-Platform**: Runs on Web, Android, iOS, Windows, macOS, and Linux

## Tech Stack

- **Flutter**: Google's UI toolkit (SDK >=3.10.1)
- **Dart**: Programming language
- **HTTP Package**: For API communication
- **Google Fonts**: Typography
- **Flutter SpinKit**: Loading indicators

## Prerequisites

- Flutter SDK 3.10.1 or higher
- Dart SDK 3.10.1 or higher
- A running backend server (see `/backend/README.md`)

## Installation

### 1. Install Flutter

Follow the official Flutter installation guide:
https://docs.flutter.dev/get-started/install

Verify installation:
```bash
flutter doctor
```

### 2. Clone and Setup

```bash
cd telugu_news_app
flutter pub get
```

### 3. Configure Backend URL

Edit `lib/services/api_service.dart` and `lib/screens/home_screen.dart` if your backend is not running on `localhost:8000`:

```dart
// In api_service.dart
static const String baseUrl = "http://your-backend-url:8000";

// In home_screen.dart
final String apiBaseUrl = 'http://your-backend-url:8000/search';
```

## Running the App

### Web
```bash
flutter run -d chrome
```

### Android
```bash
flutter run -d android
```

### iOS (macOS only)
```bash
flutter run -d ios
```

### Windows Desktop
```bash
flutter run -d windows
```

### macOS Desktop
```bash
flutter run -d macos
```

### Linux Desktop
```bash
flutter run -d linux
```

## Building for Production

### Web
```bash
flutter build web
# Output: build/web/
```

### Android APK
```bash
flutter build apk
# Output: build/app/outputs/flutter-apk/app-release.apk
```

### Android App Bundle
```bash
flutter build appbundle
# Output: build/app/outputs/bundle/release/app-release.aab
```

### iOS
```bash
flutter build ios
# Requires macOS and Xcode
```

### Windows
```bash
flutter build windows
# Output: build/windows/runner/Release/
```

## Project Structure

```
telugu_news_app/
├── lib/
│   ├── main.dart              # App entry point
│   ├── screens/
│   │   ├── home_screen.dart   # Main question/answer screen
│   │   └── search_results_screen.dart  # Alternative search screen
│   ├── services/
│   │   └── api_service.dart   # Backend API integration
│   └── widgets/
│       └── news_card.dart     # Reusable news card widget
├── pubspec.yaml               # Dependencies configuration
├── android/                   # Android-specific files
├── ios/                       # iOS-specific files
├── web/                       # Web-specific files
├── windows/                   # Windows-specific files
├── linux/                     # Linux-specific files
└── macos/                     # macOS-specific files
```

## Dependencies

Main dependencies (from `pubspec.yaml`):
- `http: ^1.2.0` - HTTP client for API calls
- `google_fonts: ^6.2.1` - Beautiful fonts
- `flutter_spinkit: ^5.2.0` - Loading animations
- `cupertino_icons: ^1.0.8` - iOS-style icons

Dev dependencies:
- `flutter_test` - Testing framework
- `flutter_lints: ^6.0.0` - Linting rules

## Troubleshooting

### "Failed to connect to backend"
- Ensure the backend server is running on the specified URL
- Check if the backend URL in the code matches your server
- Verify CORS is enabled in the backend

### "No connected devices"
- For web: Enable web support with `flutter config --enable-web`
- For Android: Connect a device or start an emulator
- For iOS: Start a simulator (macOS only)
- For desktop: Platform must be enabled

### Build errors
```bash
flutter clean
flutter pub get
flutter pub upgrade
```

### Lint errors
```bash
flutter analyze
```

## Development

### Enable additional platforms
```bash
flutter config --enable-web
flutter config --enable-windows-desktop
flutter config --enable-macos-desktop
flutter config --enable-linux-desktop
```

### Hot reload during development
When running `flutter run`, press `r` for hot reload or `R` for hot restart.

## Testing

Run all tests:
```bash
flutter test
```

## API Integration

The app communicates with the backend via REST API:

### Endpoint
```
GET /search?query=<question>
```

### Response Format
```json
{
  "query": "user question",
  "answer": "generated answer",
  "sources": ["source1", "source2"],
  "language": "telugu",
  "chunks_retrieved": 7
}
```

## Contributing

See the main project [CONTRIBUTING.md](../CONTRIBUTING.md) for contribution guidelines.

## Resources

- [Flutter Documentation](https://docs.flutter.dev/)
- [Dart Documentation](https://dart.dev/guides)
- [Flutter Cookbook](https://docs.flutter.dev/cookbook)
- [Material Design](https://m3.material.io/)

## License

Part of the MANAVARTHA-AI project. See main repository for license information.

## Support

For issues specific to the Flutter app:
1. Check this README's troubleshooting section
2. Check the main project README
3. Open an issue on GitHub with the `flutter` label
