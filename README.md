# Visionary AI Personal Scheduler

A cloud-native, mobile-first AI-powered personal scheduling assistant that learns from user inputs to create personalized schedules with intelligent reminders and goal tracking.

## Architecture Overview

- **Cloud Backend**: Python FastAPI with cloud-native microservices
- **Mobile App**: React Native with Expo for cross-platform development
- **Web App**: Progressive Web App (PWA) with service workers
- **Databases**: PostgreSQL for user data, MongoDB for knowledge base
- **Cache**: Redis for high-performance caching
- **Storage**: Encrypted AWS S3 for file storage
- **Infrastructure**: Docker containers with Kubernetes orchestration

## Features

- 🤖 AI-powered schedule generation with autonomous time blocking
- 📱 Mobile-first design with cross-platform synchronization
- 🔒 Industry-standard encryption and security
- 🎨 AI-generated HD visuals and premium analytics
- 🌐 Progressive Web App with offline functionality
- ☁️ Cloud-native architecture for 24/7 operation
- 📊 Advanced analytics with interactive charts
- 🔔 Intelligent reminders with conversational tones

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker and Docker Compose
- AWS CLI (for cloud deployment)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/visionary.git
   cd visionary
   ```

2. **Start infrastructure services**
   ```bash
   cd infrastructure
   docker-compose up -d postgres mongodb redis
   ```

3. **Set up cloud backend**
   ```bash
   cd cloud_backend
   cp .env.example .env
   # Edit .env with your configuration
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

4. **Set up mobile app**
   ```bash
   cd mobile_app
   npm install
   npx expo start
   ```

5. **Set up web app**
   ```bash
   cd web_app
   npm install
   npm start
   ```

### Docker Development

```bash
cd infrastructure
docker-compose up
```

This starts all services:
- Backend API: http://localhost:8000
- Web App: http://localhost:3000
- PostgreSQL: localhost:5432
- MongoDB: localhost:27017
- Redis: localhost:6379

## Project Structure

```
visionary/
├── cloud_backend/          # Python FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Core services (auth, database, cache)
│   │   └── models/         # Data models
│   ├── tests/              # Backend tests
│   └── requirements.txt
├── mobile_app/             # React Native mobile app
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── screens/        # App screens
│   │   ├── services/       # API services
│   │   └── store/          # Redux store
│   └── package.json
├── web_app/                # Progressive Web App
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # App pages
│   │   └── utils/          # Utilities and service worker
│   └── package.json
└── infrastructure/         # Deployment configuration
    ├── docker-compose.yml
    ├── kubernetes/
    ├── aws/terraform/
    └── ci-cd/
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

### Backend Tests
```bash
cd cloud_backend
pytest tests/ -v --cov=app
```

### Mobile App Tests
```bash
cd mobile_app
npm test
```

### Web App Tests
```bash
cd web_app
npm test
```

## Deployment

### AWS Cloud Deployment

1. **Configure AWS credentials**
   ```bash
   aws configure
   ```

2. **Deploy infrastructure**
   ```bash
   cd infrastructure/aws/terraform
   terraform init
   terraform plan
   terraform apply
   ```

3. **Deploy applications**
   ```bash
   # Backend deployment via GitHub Actions
   git push origin main
   
   # Mobile app build
   cd mobile_app
   eas build --platform all
   ```

### Kubernetes Deployment

```bash
cd infrastructure/kubernetes
kubectl apply -f backend-deployment.yaml
```

## Environment Variables

### Backend (.env)
- `POSTGRES_URL`: PostgreSQL connection string
- `MONGODB_URL`: MongoDB connection string
- `REDIS_URL`: Redis connection string
- `AWS_ACCESS_KEY_ID`: AWS access key
- `AWS_SECRET_ACCESS_KEY`: AWS secret key
- `S3_BUCKET_NAME`: S3 bucket for file storage
- `SECRET_KEY`: JWT secret key
- `ENCRYPTION_KEY`: File encryption key
- `OPENAI_API_KEY`: OpenAI API key for AI features

### Mobile App
- `EXPO_PUBLIC_API_URL`: Backend API URL

### Web App
- `REACT_APP_API_URL`: Backend API URL

## Security Features

- 🔐 End-to-end encryption for sensitive data
- 🛡️ Industry-standard authentication with JWT
- 🔒 Encrypted file storage in AWS S3
- 🚫 Secure data deletion and cleanup
- 🔑 Minimal permissions for external integrations
- 🛡️ Rate limiting and DDoS protection

## AI Features

- 📝 Document parsing and content categorization
- 🎤 Voice input processing with speech-to-text
- 🧠 Pattern recognition and habit defense
- 📅 Autonomous time blocking and conflict resolution
- 🎨 AI-generated HD visuals (DALL-E, Midjourney, Stable Diffusion)
- 📊 Premium visual analytics and insights
- 🔔 Conversational reminder tones

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, email support@visionary.ai or join our Slack channel.

## Roadmap

- [ ] Advanced AI model integration
- [ ] Multi-language support
- [ ] Calendar integrations (Google, Outlook, Apple)
- [ ] Wearable device integration
- [ ] Team collaboration features
- [ ] Advanced analytics dashboard