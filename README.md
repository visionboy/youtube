# YouTube Analytics Application

A full-stack YouTube video search and analytics platform built with **Nuxt 3** (frontend) and **FastAPI** (backend), featuring a **Visual Studio Code-inspired design**.

## Features

### 🎥 Video Search & Discovery
- Real-time YouTube video search
- Advanced filtering (relevance, date, view count, rating)
- Client-side sorting by views, likes, and date
- Adjustable result limits (10, 25, 50)

### 📊 Video Analytics
- View count, like count, and comment count display
- Publication date tracking
- Channel information

### 🎬 Video Playback
- In-app video player modal
- YouTube iframe integration
- Click-to-play functionality

### ⚙️ Settings Management
- YouTube API key configuration
- Secure key storage
- API key status monitoring

### 🎨 VS Code Design Theme
- Dark theme with VS Code color palette
- Activity bar-style navigation
- Status bar footer
- Smooth animations and transitions

## Tech Stack

**Frontend:**
- Nuxt 3
- Vue 3 Composition API
- Tailwind CSS
- Axios

**Backend:**
- FastAPI
- Python 3.8+
- YouTube Data API v3
- Pydantic

## Prerequisites

- Node.js 18+ and npm
- Python 3.8+
- YouTube Data API v3 key ([Get one here](https://console.cloud.google.com/))

## Installation

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env
# Edit .env and add your YouTube API key (optional - can be set via UI)
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

## Running the Application

### Start Backend Server

```bash
cd backend
uvicorn main:app --reload
```

Backend will run at: `http://localhost:8000`
API docs available at: `http://localhost:8000/docs`

### Start Frontend Server

```bash
cd frontend
npm run dev
```

Frontend will run at: `http://localhost:3000`

## Usage

1. **Configure API Key** (First Time)
   - Navigate to Settings page
   - Enter your YouTube Data API v3 key
   - Click "Save API Key"

2. **Search Videos**
   - Go to the Videos page (home)
   - Enter search query
   - Adjust filters (order by, max results)
   - Click "Search"

3. **Sort Results**
   - Use sort buttons (Views, Likes, Date)
   - Toggle sort direction with arrow button

4. **Play Videos**
   - Click on any video card
   - Video player modal will open
   - Close with X button or click outside

## API Endpoints

### Videos
- `GET /api/videos/search` - Search videos
  - Query params: `q`, `maxResults`, `order`
- `GET /api/videos/{video_id}` - Get video details

### Settings
- `GET /api/settings/api-key` - Check API key status
- `POST /api/settings/api-key` - Save API key
- `DELETE /api/settings/api-key` - Delete API key

## Project Structure

```
youtube/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── config.py            # Configuration
│   ├── requirements.txt     # Python dependencies
│   ├── routes/
│   │   ├── youtube.py       # Video endpoints
│   │   └── settings.py      # Settings endpoints
│   └── services/
│       ├── youtube_service.py    # YouTube API integration
│       └── settings_service.py   # Settings management
└── frontend/
    ├── nuxt.config.ts       # Nuxt configuration
    ├── package.json         # Node dependencies
    ├── tailwind.config.js   # Tailwind config
    ├── app.vue              # Root component
    ├── assets/
    │   └── css/
    │       └── main.css     # Global styles (VS Code theme)
    ├── components/
    │   ├── VideoCard.vue    # Video card component
    │   ├── VideoPlayer.vue  # Video player modal
    │   ├── SearchBar.vue    # Search input
    │   └── FilterControls.vue  # Filter/sort controls
    ├── composables/
    │   ├── useYouTubeApi.ts    # YouTube API composable
    │   └── useSettings.ts      # Settings composable
    ├── layouts/
    │   └── default.vue      # Default layout
    └── pages/
        ├── index.vue        # Videos page
        └── settings.vue     # Settings page
```

## Design System

The application uses a **Visual Studio Code-inspired design**:

- **Colors:**
  - Background: `#1e1e1e`
  - Sidebar: `#252526`
  - Accent: `#007acc` (blue)
  - Highlight: `#f9826c` (orange)
  - Text: `#cccccc`

- **Typography:** Inter, Segoe UI
- **Components:** Cards, buttons, inputs styled like VS Code
- **Navigation:** Activity bar-style with icons

## YouTube API Quota

The free tier has a daily quota of **10,000 units**:
- Search request: ~100 units
- Video details: ~1 unit

Approximately **100 searches per day** on free tier.

## License

MIT

## Author

Built with Nuxt 3 and FastAPI
