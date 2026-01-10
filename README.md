# MANAVARTHA-AI

**MANAVARTHA-AI** is a multilingual Telugu News Question Answering system powered by Retrieval-Augmented Generation (RAG). The application allows users to ask questions in Telugu, English, or Romanized Telugu, and receive accurate answers based on a corpus of Telugu news articles.

## 🌟 Features

- **Multilingual Support**: Ask questions in Telugu (తెలుగు), English, or Romanized Telugu
- **RAG Architecture**: Uses Retrieval-Augmented Generation for accurate, source-based answers
- **Modern Tech Stack**: FastAPI backend + Flutter frontend
- **Semantic Search**: Powered by Cohere's multilingual embeddings
- **Answer Generation**: Uses Cohere's Command-R model for natural language generation
- **Cross-Platform**: Flutter app runs on Web, Android, iOS, Windows, macOS, and Linux

## 🏗️ Architecture

```
┌─────────────────┐
│  Flutter App    │  (Mobile/Web/Desktop)
│  (Dart/Flutter) │
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────┐
│  FastAPI Server │  (Python)
│  + CORS         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   RAG Engine    │
│  - Cohere API   │  (Embeddings + Answer Generation)
│  - FAISS Index  │  (Vector Search)
│  - News Corpus  │  (Telugu Articles)
└─────────────────┘
```

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Python 3.8+**: Programming language
- **Cohere API**: Multilingual embeddings (`embed-multilingual-v3.0`) and answer generation (`command-r`)
- **FAISS**: Facebook AI Similarity Search for efficient vector search
- **Pandas & NumPy**: Data processing and numerical operations
- **python-dotenv**: Environment variable management

### Frontend
- **Flutter**: Google's UI toolkit for building natively compiled applications
- **Dart**: Programming language for Flutter
- **HTTP Package**: For API communication
- **Material Design**: Modern, responsive UI

### Optional
- **Streamlit**: Alternative web interface for testing (included in requirements)
- **Gemini API**: Alternative answer generation model (optional)

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

### Backend Requirements
- Python 3.8 or higher
- pip (Python package manager)

### Frontend Requirements
- Flutter SDK 3.10.1 or higher
- Dart SDK 3.10.1 or higher

### API Keys
You'll need to obtain free API keys from:
- **Cohere**: https://dashboard.cohere.com/api-keys
- **Gemini** (optional): https://aistudio.google.com/app/apikey

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/BHANU2624/MANAVARTHA-AI.git
cd MANAVARTHA-AI
```

### 2. Backend Setup

#### Step 2.1: Create Virtual Environment

```bash
cd backend
python -m venv venv
```

#### Step 2.2: Activate Virtual Environment

**Linux/macOS:**
```bash
source venv/bin/activate
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

#### Step 2.3: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 2.4: Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
COHERE_API_KEY=your_actual_cohere_api_key
GEMINI_API_KEY=your_actual_gemini_api_key
```

#### Step 2.5: Prepare Data (Important)

Ensure you have the required data file:
- Place your news corpus CSV at: `backend/data/all_telugu_chunk_embeddings_clean.csv`
- The CSV should contain columns: `chunk` (text) and `embedding` (vector)

If you don't have this file, you'll need to:
1. Collect Telugu news articles
2. Chunk them appropriately
3. Generate embeddings using Cohere's API
4. Save as CSV

#### Step 2.6: Start the Backend Server

**Option 1: Using the batch file (Windows):**
```cmd
start_server.bat
```

**Option 2: Using uvicorn directly:**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Option 3: Using Python module:**
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API Root**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Search Endpoint**: http://localhost:8000/search?query=your_question

### 3. Frontend Setup (Flutter App)

#### Step 3.1: Navigate to Flutter Directory

```bash
cd ../telugu_news_app
```

#### Step 3.2: Install Flutter Dependencies

```bash
flutter pub get
```

#### Step 3.3: Run the App

**For Web:**
```bash
flutter run -d chrome
```

**For Windows Desktop:**
```bash
flutter run -d windows
```

**For Android (with device/emulator connected):**
```bash
flutter run -d android
```

**For iOS (macOS only, with device/simulator):**
```bash
flutter run -d ios
```

#### Step 3.4: Configure Backend URL

If your backend is not running on `localhost:8000`, update the API URL in:
- `lib/services/api_service.dart`
- `lib/screens/home_screen.dart`

Change:
```dart
final String apiBaseUrl = 'http://localhost:8000/search';
```

To your backend URL.

## 📖 API Documentation

### Endpoints

#### 1. Root Endpoint
```
GET /
```
Returns API information and available endpoints.

#### 2. Health Check
```
GET /health
```
Returns server health status and number of loaded chunks.

**Response:**
```json
{
  "status": "healthy",
  "message": "RAG engine is operational",
  "chunks_loaded": 15000
}
```

#### 3. Search/Ask Question
```
GET /search?query=<your_question>
```

**Parameters:**
- `query` (required): User question in Telugu, English, or Romanized Telugu

**Example Request:**
```bash
curl "http://localhost:8000/search?query=తెలంగాణలో%20వరదలు"
```

**Response:**
```json
{
  "query": "తెలంగాణలో వరదలు",
  "answer": "తెలంగాణలో ఇటీవల భారీ వర్షాలు కురిసి అనేక ప్రాంతాల్లో వరద పరిస్థితి ఏర్పడింది...",
  "sources": [
    "వార్త 1: తెలంగాణలో భారీ వర్షాలు...",
    "వార్త 2: హైదరాబాద్‌లో నీటి మునిగిన ప్రాంతాలు...",
    "వార్త 3: సహాయక చర్యలు ప్రారంభం..."
  ],
  "language": "telugu",
  "chunks_retrieved": 7
}
```

## 🧪 Testing

### Test Backend
```bash
# Health check
curl http://localhost:8000/health

# Test query
curl "http://localhost:8000/search?query=తెలుగు%20న్యూస్"
```

### Test Frontend
```bash
cd telugu_news_app
flutter test
```

## 🐛 Troubleshooting

### Backend Issues

**Problem: "COHERE_API_KEY not found"**
- Solution: Create `.env` file in `backend/` directory with your API key

**Problem: "CSV file not found"**
- Solution: Ensure `data/all_telugu_chunk_embeddings_clean.csv` exists in backend directory

**Problem: "Port 8000 already in use"**
- Solution: Use a different port: `uvicorn main:app --port 8001`

**Problem: PowerShell execution policy error**
- Solution: Use `start_server.bat` instead or change policy: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### Frontend Issues

**Problem: "Failed to connect to backend"**
- Solution: Ensure backend is running on http://localhost:8000
- Check if CORS is properly configured
- Verify API URL in Flutter code

**Problem: Flutter build errors**
- Solution: Run `flutter clean && flutter pub get`
- Ensure Flutter SDK is up to date: `flutter upgrade`

**Problem: Web build fails**
- Solution: Enable web support: `flutter config --enable-web`

## 📁 Project Structure

```
MANAVARTHA-AI/
├── backend/                    # FastAPI backend
│   ├── data/                  # Data files (CSV, embeddings)
│   ├── main.py               # Main FastAPI application
│   ├── rag_engine.py         # RAG implementation
│   ├── models.py             # Pydantic models
│   ├── news_loader.py        # Data loading utilities
│   ├── requirements.txt      # Python dependencies
│   ├── .env.example          # Environment variables template
│   ├── README.md             # Backend documentation
│   └── QUICKSTART.md         # Quick start guide
├── telugu_news_app/          # Flutter frontend
│   ├── lib/
│   │   ├── screens/          # UI screens
│   │   ├── services/         # API services
│   │   ├── widgets/          # Reusable widgets
│   │   └── main.dart         # App entry point
│   ├── pubspec.yaml          # Flutter dependencies
│   └── README.md             # Frontend documentation
├── api.py                    # Legacy API (optional)
├── app.py                    # Streamlit app (optional)
├── .gitignore               # Git ignore rules
├── .env.example             # Root environment template
└── README.md                # This file
```

## 🔒 Security Best Practices

1. **Never commit `.env` files** - They contain sensitive API keys
2. **Use `.env.example`** for documentation without actual keys
3. **Rotate API keys** regularly
4. **Limit CORS origins** in production (currently set to `*` for development)
5. **Use HTTPS** in production deployments
6. **Rate limit** API endpoints in production
7. **Validate input** to prevent injection attacks

## 🚢 Deployment

### Docker Deployment (Recommended)

The easiest way to deploy the backend is using Docker:

#### Prerequisites
- Docker installed
- Docker Compose installed

#### Steps

1. **Clone the repository:**
```bash
git clone https://github.com/BHANU2624/MANAVARTHA-AI.git
cd MANAVARTHA-AI
```

2. **Configure environment:**
```bash
cd backend
cp .env.example .env
nano .env  # Add your API keys
```

3. **Place your data file:**
Ensure `backend/data/all_telugu_chunk_embeddings_clean.csv` exists.

4. **Build and run with Docker Compose:**
```bash
cd ..  # Back to root directory
docker-compose up -d
```

5. **Check logs:**
```bash
docker-compose logs -f backend
```

6. **Stop the service:**
```bash
docker-compose down
```

#### Docker Commands Reference

```bash
# Build only
docker-compose build

# Start in foreground (see logs)
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Restart
docker-compose restart

# Stop
docker-compose down

# Remove everything including volumes
docker-compose down -v
```

### Manual Backend Deployment (Ubuntu Server)

```bash
# Install dependencies
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Clone and setup
git clone https://github.com/BHANU2624/MANAVARTHA-AI.git
cd MANAVARTHA-AI/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Add your API keys

# Run with production server
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

#### Using systemd (production)

Create `/etc/systemd/system/manavartha.service`:

```ini
[Unit]
Description=MANAVARTHA-AI Backend
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/path/to/MANAVARTHA-AI/backend
Environment="PATH=/path/to/MANAVARTHA-AI/backend/venv/bin"
ExecStart=/path/to/MANAVARTHA-AI/backend/venv/bin/gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable manavartha
sudo systemctl start manavartha
sudo systemctl status manavartha
```

### Frontend Deployment (Web)

```bash
cd telugu_news_app
flutter build web --release
# Deploy the build/web directory to your hosting provider
# (Netlify, Vercel, Firebase Hosting, GitHub Pages, etc.)
```

#### Deploy to Netlify
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
cd telugu_news_app
flutter build web --release
netlify deploy --prod --dir=build/web
```

#### Deploy to Firebase Hosting
```bash
# Install Firebase CLI
npm install -g firebase-tools

# Initialize
cd telugu_news_app
firebase init hosting

# Build and deploy
flutter build web --release
firebase deploy --only hosting
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is part of a capstone project. Please contact the repository owner for licensing information.

## 👥 Authors

- **BHANU2624** - [GitHub Profile](https://github.com/BHANU2624)

## 🙏 Acknowledgments

- **Cohere** for providing multilingual embeddings and language models
- **Google** for Gemini API
- **Facebook AI** for FAISS
- **FastAPI** and **Flutter** communities

## 📞 Support

For issues, questions, or contributions:
- Open an issue on [GitHub Issues](https://github.com/BHANU2624/MANAVARTHA-AI/issues)
- Check existing documentation in `/backend/README.md` and `/backend/QUICKSTART.md`

## 🗺️ Roadmap

- [ ] Add user authentication
- [ ] Implement conversation history
- [ ] Add more news sources
- [ ] Improve answer quality with fine-tuning
- [ ] Add voice input/output
- [ ] Implement caching for faster responses
- [ ] Add analytics dashboard
- [ ] Support more Indian languages

---

**Made with ❤️ for Telugu news enthusiasts**
