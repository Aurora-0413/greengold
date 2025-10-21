# Copilot / AI Agent Instructions — GreenGold

This is a **full-stack web project** showcasing Anji County's ecological transformation story ("两山理论" / "Green Mountains are Golden Mountains"). The repo contains a **Vue 3 frontend** (`green-gold/`) and a **FastAPI backend** (`server/`) for an AI-powered quiz system.

## Architecture Overview

**Frontend** (`green-gold/`): Vue 3 SPA with Vue Router, built with Vite  
**Backend** (`server/`): FastAPI REST API serving quiz questions from a static JSON bank  
**Data Flow**: Frontend fetches questions via HTTP → Backend randomly selects from `questions_data.json` → Frontend displays and validates answers

### Key Routes & Components
- `/` → `StartPage.vue`: Landing page with "开始探索" button (uses background image from `src/assets/images/1.png`)
- `/main` → `MainPage.vue`: Navigation hub linking to three sections (Anji timeline, knowledge, quiz)
- `/anji-timeline` → `AnjiTimeline.vue`: Interactive timeline with video modals for 2003/2005/2010s/2021 milestones
- `/quiz` → `QuizPage.vue`: Two-mode quiz system
  - **Practice mode**: Single question with instant feedback
  - **Challenge mode**: 10 questions with answer sheet card showing progress (light green = answered, light gray = unanswered)
    - Answer sheet in top-right (desktop only, hidden on mobile) allows jumping between questions
    - Warns if submitting with unanswered questions (treats blank answers as incorrect)
    - Fully responsive design optimized for mobile devices

### Critical Static Asset Convention
- **Videos**: Store in `green-gold/public/videos/` and reference as `/videos/<name>.mp4` (absolute path)  
  Example: `AnjiTimeline.vue` uses `videoData[].src: '/videos/2003.mp4'`
- **Images**: Import from `green-gold/src/assets/images/` using relative imports  
  Example: `StartPage.vue` uses `background-image: url('../assets/images/1.png')`

## Developer Workflows

### Frontend Development
```powershell
cd green-gold
npm install          # First time only
npm run dev          # Start Vite dev server on http://localhost:5173
npm run build        # Production build to green-gold/dist/
npm run preview      # Preview production build locally
```

### Backend Development
```powershell
cd server
pip install -r requirements.txt  # First time only
uvicorn main:app --reload        # Start FastAPI on http://localhost:8000
```
**CORS Configuration**: Backend allows `http://localhost:5173` (Vite default). Update `main.py` if frontend port changes.

### Environment Setup for Backend
Create `server/.env` with:
```env
DASHSCOPE_API_KEY=your_api_key_here  # Required for AI features (currently unused, questions come from JSON)
```
**Note**: Current implementation (`ai_service.py`) reads from `questions_data.json` instead of calling external AI APIs.

## Project-Specific Patterns

### Vue Component Style
- Use **Options API** (`data()`, `methods`) not Composition API or `<script setup>`
- All components use `<style scoped>` for encapsulation
- Global styles go in `green-gold/src/style.css` (imported in `main.js`)

### Router Navigation Pattern
```javascript
// Programmatic navigation (used throughout)
this.$router.push('/main')
this.$router.push({ path: '/anji-timeline' })
```

### Quiz Question Format (Backend → Frontend)
Questions in `server/questions_data.json` are stored as **plain text with embedded options**:
```json
{
  "question": "题干内容？\nA. 选项A\nB. 选项B\nC. 选项C\nD. 选项D",
  "correct_answer": "B",
  "explanation": "解释文本"
}
```
Frontend (`QuizPage.vue`) parses this using `parseQuestion()` method to extract title and options array.

### API Endpoints (Backend)
- `GET /api/practice/question` → Returns single question for practice mode
- `POST /api/practice/check` → Validates answer (body: `{question_id, user_answer}`)
- `GET /api/quiz/start` → Returns 10 questions for challenge mode (answers hidden)
- `POST /api/quiz/submit` → Submits quiz answers and returns score

## Common Tasks

### Adding a New Route
1. Create component in `green-gold/src/components/NewPage.vue`
2. Import and register in `green-gold/src/router.js`:
   ```javascript
   import NewPage from './components/NewPage.vue'
   const routes = [
     // ... existing routes
     { path: '/new-path', component: NewPage }
   ]
   ```
3. Link from navigation (e.g., in `MainPage.vue`):
   ```javascript
   goToSection(section) {
     if (section === 'new') this.$router.push('/new-path')
   }
   ```

### Adding Videos to Timeline
1. Place video file in `green-gold/public/videos/<year>.mp4`
2. Update `AnjiTimeline.vue` → `videoData` array:
   ```javascript
   videoData: [
     { title: 'YYYY年 - 标题', description: '描述', src: '/videos/<year>.mp4' }
   ]
   ```
3. Add corresponding timeline item in template section

### Modifying Quiz Questions
Edit `server/questions_data.json` directly (array of question objects). Server will randomly select from this pool on each `/api/practice/question` request.

## Known Limitations & Notes

- **No TypeScript**: Pure JavaScript codebase
- **No Tests**: No test files or test commands exist
- **Hardcoded API URL**: `QuizPage.vue` uses `const API_BASE = 'http://localhost:8000/api'` (update for production)
- **AI Service Not Active**: `ai_service.py` currently bypasses AI and reads from JSON; `config.py` has unused AI model settings
- **Video Files Not Committed**: `green-gold/public/videos/README.md` exists but actual `.mp4` files must be added manually

## File Structure Reference
```
greengold/
├── green-gold/                  # Frontend (Vue 3 + Vite)
│   ├── public/
│   │   └── videos/              # *.mp4 files (referenced as /videos/*)
│   ├── src/
│   │   ├── assets/images/       # Images imported in components
│   │   ├── components/          # All page components (*.vue)
│   │   ├── App.vue              # Root component
│   │   ├── main.js              # Vue app entry (imports router + style.css)
│   │   ├── router.js            # Route definitions
│   │   └── style.css            # Global styles
│   ├── index.html               # SPA entry point (<div id="app">)
│   ├── package.json             # Frontend dependencies (vue, vue-router, vite)
│   └── vite.config.js           # Vite build config
├── server/                      # Backend (FastAPI)
│   ├── main.py                  # FastAPI app + CORS + endpoints
│   ├── models.py                # Pydantic models (Question, QuizResponse, etc.)
│   ├── ai_service.py            # Question generation (reads from JSON)
│   ├── config.py                # Pydantic settings (env vars, unused AI config)
│   ├── questions_data.json      # Static question bank (867 lines)
│   └── requirements.txt         # Backend dependencies (fastapi, uvicorn, pydantic v2)
└── README.md                    # Project concept document (not technical)
```

## Troubleshooting

**Frontend not connecting to backend?**  
→ Check CORS settings in `server/main.py` match your frontend URL  
→ Verify backend is running on port 8000 and frontend on 5173

**Videos not playing?**  
→ Ensure `.mp4` files exist in `green-gold/public/videos/`  
→ Check browser console for 404 errors (path must be `/videos/filename.mp4`)

**Question parsing errors?**  
→ Verify question format in `questions_data.json` matches `题干\nA. ...\nB. ...\nC. ...\nD. ...` pattern 
