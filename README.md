# Visionary - AI Personal Scheduler

An AI-powered personal scheduling assistant that learns from user inputs to create personalized daily, weekly, or monthly schedules. The system trains on uploaded data including daily routines, class schedules, and user-defined visions across financial, health, nutrition, and psychological domains.

## Features

✅ **Multi-Modal Data Input**
- Document upload (PDF, TXT, DOCX)
- Voice input processing
- Direct text input
- Real-time content categorization

✅ **AI-Powered Scheduling**
- Intelligent schedule generation
- Pattern recognition and learning
- Flexible schedule modifications
- Alternative suggestions

✅ **Progress Tracking**
- Vision-based goal tracking
- Real-time progress updates
- Achievement celebrations
- Comprehensive reporting

✅ **Real-Time Synchronization**
- WebSocket-based live updates
- Cross-platform data sync
- Instant notifications

✅ **Visual Design Gallery**
- 19 curated design concepts
- AI-powered image analysis
- Interactive image selector
- Design recommendations

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Primary database
- **Redis** - Caching and session storage
- **SQLAlchemy** - ORM with async support
- **WebSockets** - Real-time communication
- **JWT** - Authentication

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Material-UI** - Component library
- **Axios** - HTTP client
- **WebSocket API** - Real-time updates

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-service orchestration

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### 1. Clone the Repository
```bash
git clone <repository-url>
cd visionary
```

### 2. Start with Docker Compose
```bash
docker-compose up --build
```

This will start:
- PostgreSQL database on port 5432
- Redis cache on port 6379
- Backend API on port 8000
- Frontend app on port 3000

### 3. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### 4. Demo Login
Use any email and password to login (demo mode).

### 5. Explore the Design Gallery
- **Image Gallery**: http://localhost:3000/gallery - Browse all 19 design concepts
- **Image Selector**: http://localhost:3000/selector - Interactive image analysis tool
- **Design Recommendations**: See `IMAGE_RECOMMENDATIONS.md` for detailed analysis

## Development Setup

### Backend Development
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Development
```bash
cd frontend
npm install
npm start
```

### Run Tests
```bash
cd backend
python -m pytest tests/ -v
```

## API Endpoints

### Upload Processing
- `POST /api/upload/document` - Upload documents
- `POST /api/upload/text` - Process text input
- `POST /api/upload/voice` - Process voice input
- `GET /api/upload/history` - Get upload history

### Schedule Management
- `GET /api/schedule/` - Get user schedules
- `POST /api/schedule/` - Create new schedule
- `POST /api/schedule/generate` - AI-generate schedule
- `PUT /api/schedule/{id}` - Update schedule
- `GET /api/schedule/{id}/alternatives` - Get alternatives

### Progress Tracking
- `GET /api/progress/overview` - Get progress overview
- `GET /api/progress/vision/{id}` - Get vision progress
- `PUT /api/progress/vision/{id}/metric` - Update metric
- `GET /api/progress/report` - Generate report
- `GET /api/progress/achievements` - Get achievements

### Reminders
- `GET /api/reminders/` - Get reminders
- `POST /api/reminders/` - Create reminder
- `PUT /api/reminders/{id}` - Update reminder

### Real-Time Updates
- `WebSocket /ws/{user_id}` - Real-time connection

## Project Structure

```
visionary/
├── backend/                 # Python FastAPI backend
│   ├── api/                # API route handlers
│   ├── tests/              # Test files
│   ├── models.py           # Database models
│   ├── database.py         # Database configuration
│   ├── auth.py             # Authentication
│   ├── upload_service.py   # Upload processing
│   ├── ai_service.py       # AI processing
│   ├── schedule_service.py # Schedule generation
│   ├── reminder_service.py # Reminder management
│   ├── progress_service.py # Progress tracking
│   ├── websocket_service.py # Real-time updates
│   └── main.py             # Application entry point
├── frontend/               # React TypeScript frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API services
│   │   └── App.tsx         # Main app component
│   └── public/
├── .kiro/                  # Kiro specs and configuration
│   └── specs/
│       └── ai-personal-scheduler/
├── docker-compose.yml      # Multi-service setup
└── README.md
```

## Implementation Status

### Completed Tasks ✅
- [x] Project structure and infrastructure
- [x] Core data models (User, Vision, Schedule, etc.)
- [x] Upload processing service (documents, text, voice placeholder)
- [x] AI processing service (categorization, pattern recognition)
- [x] Schedule generation service
- [x] Reminder system
- [x] Progress tracking service
- [x] Real-time WebSocket communication
- [x] Frontend components (Dashboard, Upload, Schedule, Progress)
- [x] API integration
- [x] Authentication system
- [x] Docker containerization

### In Progress 🚧
- [ ] Voice input processing (Google Speech-to-Text integration)
- [ ] Advanced AI features (proactive suggestions)
- [ ] Mobile application (React Native)
- [ ] Comprehensive testing suite

### Planned Features 📋
- [ ] Calendar integrations (Google Calendar, Apple Calendar)
- [ ] Advanced analytics and insights
- [ ] Team collaboration features
- [ ] Third-party integrations
- [ ] Mobile push notifications

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For questions or support, please open an issue in the repository.