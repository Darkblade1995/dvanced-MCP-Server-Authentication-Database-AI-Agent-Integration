Advanced MCP Server — Authentication, Database & AI Agent Integration

A production-ready Model Context Protocol (MCP) Server built with Python and FastMCP, featuring JWT authentication via Stytch, SQLAlchemy ORM, and full integration with AI agents like Cline.



📌 Overview
This project implements an advanced MCP server that goes beyond the basics — it includes real user authentication, per-user data isolation, and a React frontend for login. The server exposes tools that AI agents can call to manage notes, with every operation authenticated and scoped to the logged-in user.
Built as a learning project following Tech With Tim's MCP tutorial, but extended with additional architectural patterns and problem-solving.

✨ Features

🔐 Authentication — Stytch session tokens (24h) validated server-side via Stytch SDK
🗄️ Database — SQLAlchemy ORM with SQLite, per-user data isolation
🧩 MCP Protocol — HTTP Streamable transport with 2 tools: add_note and get_my_notes
🌐 Public Exposure — ngrok tunnel for external agent access
⚛️ React Frontend — Login UI with Stytch SDK, session token display
🤖 AI Agent Ready — Tested with Cline + Gemini 2.5 Flash
🏗️ Clean Architecture — Repository pattern separating DB logic from MCP tools


🏛️ Architecture
User → React Frontend (localhost:5173)
         ↓  login with Stytch (email + password)
         ↓  obtains session_token (24h opaque token)
         ↓
AI Agent (Cline) → MCP Server (127.0.0.1:8000/mcp)
         ↓  validates session_token via Stytch API
         ↓  retrieves user_id of authenticated user
         ↓
SQLAlchemy → SQLite (database.db) ← notes filtered by user_id

🗂️ Project Structure
mcpserverproject/
├── backend/
│   ├── main.py          # MCP server, tools, CORS middleware
│   ├── database.py      # SQLAlchemy models + NoteRepository
│   ├── database.db      # SQLite database (auto-created)
│   └── .env             # Environment variables
├── frontend/
│   ├── src/
│   │   ├── App.jsx      # Login UI + token display
│   │   └── main.jsx     # StytchProvider setup
│   └── package.json
└── .venv/               # Python virtual environment

🔧 Tech Stack
LayerTechnologyMCP FrameworkFastMCP 3.1.1LanguagePython 3.11AuthenticationStytch (session_token)ORM / DatabaseSQLAlchemy + SQLitePublic Tunnelngrok 3.37.2FrontendReact 18 + Vite + Stytch SDKAI AgentCline + Gemini 2.5 Flash

🚀 Getting Started
Prerequisites

Python 3.11+
Node.js 18+
Stytch account (free)
ngrok (free)

1. Clone the repository
bashgit clone https://github.com/Darkblade1995/mcpserverproject.git
cd mcpserverproject
2. Set up the backend
bash# Create and activate virtual environment
python -m venv .venv
& .venv\Scripts\Activate.ps1   # Windows PowerShell
# source .venv/bin/activate    # macOS/Linux

# Install dependencies
pip install fastmcp stytch sqlalchemy python-dotenv uvicorn starlette
3. Configure environment variables
Create backend/.env:
envSTYTCH_PROJECT_ID=project-test-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
STYTCH_SECRET=secret-test-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
STYTCH_DOMAIN=https://your-project.customers.stytch.dev
4. Set up the frontend
bashcd frontend
npm install
Create frontend/.env:
envVITE_STYTCH_PUBLIC_TOKEN=public-token-test-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

▶️ Running the Project
Open 3 separate terminals:
Terminal 1 — Backend:
bashcd mcpserverproject
& .venv\Scripts\Activate.ps1
cd backend
python main.py
Terminal 2 — ngrok:
bashngrok http 8000
Terminal 3 — Frontend:
bashcd frontend
npm run dev
Then open http://localhost:5173, log in, and copy your session token.

🔌 MCP Tools
add_note
Adds a new note for the authenticated user.
json{
  "content": "My note content",
  "session_token": "your-stytch-session-token"
}
get_my_notes
Returns all notes belonging to the authenticated user.
json{
  "session_token": "your-stytch-session-token"
}

🤖 Connecting to an AI Agent (Cline)

Install Cline in VS Code
Add your API key (Gemini, OpenAI, Anthropic, etc.)
Configure the MCP server in cline_mcp_settings.json:

json{
  "mcpServers": {
    "notes": {
      "url": "http://127.0.0.1:8000/mcp",
      "type": "streamableHttp"
    }
  }
}

In Cline chat, use natural language:

"Use the add_note tool with content 'hello world' and session_token YOUR_TOKEN"




🔐 Authentication Flow

User logs in via React frontend (Stytch email + password)
Stytch returns an opaque session_token valid for 24 hours
Token is passed as a parameter to each MCP tool call
Server validates token via stytch_client.sessions.authenticate()
Stytch returns the user_id of the authenticated user
All DB operations are scoped to that user_id


Why session_token instead of session_jwt?
Stytch's session_jwt expires every 5 minutes for security reasons. The opaque session_token lasts 24 hours and is validated directly against Stytch's API, making it practical for agent use cases.


🛠️ Key Implementation Decisions
DecisionRationalesession_token over session_jwtJWT expires in 5 min; session_token lasts 24hRepository patternSeparates DB logic from MCP tools for maintainabilitySQLAlchemy over raw SQLiteEasier migration to PostgreSQL for productionStytch SDK for validationMore reliable than manual JWT verificationCORS middlewareEnables cross-origin requests from frontend and agents

🚢 Deployment (Production Roadmap)
ComponentServiceNotesBackendRailway / RenderChange host to 0.0.0.0, add PostgreSQLFrontendVercel / Netlifynpm run build, update Stytch redirect URLsDatabasePostgreSQL (Railway)Replace SQLite connection stringTunnelNone neededUse the deployment URL directly

📚 Lessons Learned

FastMCP 3.1.1 changed its auth API (BearerAuthProvider → JWTVerifier)
Stytch session_jwt is designed to expire frequently — use session_token for agents
Cline Free plan supports MCP tools in Auto mode
ngrok free tier generates a new URL on every restart — update configs accordingly
Always use __tablename__ (not __table__) in SQLAlchemy models


👤 Author
Luis Fernando Agamez
