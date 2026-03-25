from fastmcp import FastMCP
from fastmcp.server.dependencies import get_access_token, AccessToken
from fastmcp.server.http import create_sse_app
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.requests import Request as StarletteRequest
from starlette.responses import JSONResponse
from typing import Annotated
from database import NoteRepository
from stytch import Client
import os

load_dotenv()

stytch_client = Client(
    project_id=os.getenv("STYTCH_PROJECT_ID"),
    secret=os.getenv("STYTCH_SECRET")
)

mcp = FastMCP(name="Notes App")

@mcp.tool()
def get_my_notes(session_token: str) -> str:
    """Get all notes for a user"""
    resp = stytch_client.sessions.authenticate(session_token=session_token)
    user_id = resp.session.user_id
    notes = NoteRepository.get_notes_by_user(user_id)
    if not notes:
        return "no notes"
    result = "Your notes:\n"
    for note in notes:
        result += f"- [{note.id}]: {note.content}\n"
    return result

@mcp.tool()
def add_note(content: str, session_token: str) -> str:
    """Add a note for a user"""
    resp = stytch_client.sessions.authenticate(session_token=session_token)
    user_id = resp.session.user_id
    note = NoteRepository.create_note(user_id=user_id, content=content)
    return f"added note: {note.content}"

if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="127.0.0.1",
        port=8000,
        middleware=[
            Middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
        ]
    )