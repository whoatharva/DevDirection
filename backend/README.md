# 🚀 Career Guidance Platform

A comprehensive AI-powered platform for career assessment, roadmap generation, and personalized learning paths.

## 📁 Project Structure

```
SIH25/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py              # Configuration settings
│   ├── models.py              # Pydantic data models
│   ├── utils.py               # Utility functions
│   ├── routers/               # API route handlers
│   │   ├── __init__.py
│   │   ├── quiz.py            # Quiz functionality
│   │   ├── roadmap.py         # Roadmap generation
│   │   └── users.py           # User management
│   └── services/              # Business logic engines
│       ├── __init__.py
│       ├── roadmap_engine.py          # AI roadmap generation
│       ├── hierarchical_roadmap.py    # Hierarchical roadmaps
│       └── user_roadmap_engine.py     # Custom roadmap creation
├── data/                      # JSON data files
│   ├── attempts.json          # Quiz attempts
│   ├── careers.json           # Career mappings
│   ├── questions.json         # Quiz questions
│   └── users.json             # User profiles
├── static/                    # Frontend files
│   └── integrated.html        # Main UI
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## 🚀 Quick Start

**Mac/Linux:** `./run.sh` | **Windows:** `run.bat`

Or run manually:

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Server
```bash
python -m uvicorn app.main:app --reload --port 8000
```

### 3. Access the Application
- **Main UI**: http://localhost:8000/ui
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🎯 Features

### 📝 Career Quiz
- 10-question career assessment
- AI-powered scoring and analysis
- Personalized career recommendations
- Progress tracking

### 🗺️ AI Roadmap Generation
- **AI-Powered Roadmaps**: Generate roadmaps based on quiz results
- **Custom Roadmaps**: Create personalized roadmaps with your own data
- Interactive D3.js visualization
- Milestone tracking and progress monitoring

### 👥 User Management
- User profile creation and management
- Quiz attempt history
- Custom roadmap storage

## 🔧 API Endpoints

### Quiz Endpoints
- `GET /api/v1/quiz/questions` - Get all quiz questions
- `POST /api/v1/quiz/submit` - Submit quiz answers
- `GET /api/v1/quiz/attempts/{user_id}` - Get user's quiz attempts

### Roadmap Endpoints
- `POST /api/v1/roadmap/generate` - Generate AI roadmap
- `POST /api/v1/roadmap/hierarchical` - Generate hierarchical roadmap
- `POST /api/v1/roadmap/create-custom` - Create custom roadmap
- `GET /api/v1/roadmap/custom/{roadmap_id}` - Get custom roadmap
- `GET /api/v1/roadmap/custom/user/{user_id}` - Get user's custom roadmaps
- `PUT /api/v1/roadmap/custom/{roadmap_id}/milestone` - Update milestone
- `GET /api/v1/roadmap/templates` - Get roadmap templates

### User Endpoints
- `GET /api/v1/users` - Get all users
- `GET /api/v1/users/{user_id}` - Get specific user
- `POST /api/v1/users` - Create user
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user

## 🛠️ Development

### Code Structure
- **Models**: Pydantic models for data validation
- **Routers**: FastAPI route handlers
- **Services**: Business logic engines
- **Utils**: Helper functions and utilities
- **Config**: Application configuration

### Adding New Features
1. Add models to `app/models.py`
2. Create service in `app/services/`
3. Add routes to appropriate router in `app/routers/`
4. Update frontend in `static/integrated.html`

## 📊 Data Models

### Core Models
- `UserProfile`: User information and preferences
- `Question`: Quiz questions
- `Answer`: Quiz answers
- `Attempt`: Quiz attempt records
- `RoadmapResponse`: AI-generated roadmap
- `UserGeneratedRoadmap`: Custom roadmap

### Custom Roadmap Models
- `UserRoadmapData`: Roadmap input data
- `UserPhase`: Roadmap phases
- `UserMilestone`: Individual milestones
- `UserResource`: Learning resources

## 🎨 Frontend

The frontend is a single-page application (`static/integrated.html`) with:
- **Career Quiz Tab**: Interactive quiz interface
- **Roadmap Tab**: Unified roadmap generation (AI + Custom)
- **Responsive Design**: Works on desktop and mobile
- **D3.js Visualization**: Interactive roadmap charts

## 🔒 Security

- CORS enabled for cross-origin requests
- Input validation with Pydantic models
- Error handling and logging
- Data sanitization

## 📈 Performance

- Efficient JSON data storage
- Lazy loading of services
- Optimized API responses
- Minimal dependencies

## 🐛 Troubleshooting

### Common Issues
1. **Server won't start**: Check JSON files for syntax errors
2. **Import errors**: Ensure all dependencies are installed
3. **CORS issues**: Check CORS configuration in `app/config.py`

### Debug Mode
Enable debug logging by setting environment variable:
```bash
export DEBUG=true
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Check the API documentation at `/docs`
- Review the code structure in this README
- Check the console for error messages