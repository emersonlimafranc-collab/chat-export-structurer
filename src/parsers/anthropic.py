# anthropic.py
# Parser for Anthropic Claude conversation exports
# Returns normalized Message dictionaries

import json
from typing import List, Dict, Iterator
from datetime import datetime

def parse(input_path: str) -> Iterator[Dict]:
    """
    Parse Anthropic export and yield normalized messages.
    
    Returns Iterator of dicts with:
    - thread_id: str
    - thread_title: str
    - role: str (user, assistant, system)
    - content: str
    - created_at: float (epoch timestamp)
    """
    with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
        try:
            data = json.load(f)
        except Exception as e:
            raise SystemExit(f"[ERROR] Invalid JSON: {e}")
    
    # Anthropic exports are an array of conversations
    if not isinstance(data, list):
        raise SystemExit("[ERROR] Anthropic export should be a JSON array")
    
    for convo in data:
        yield from _parse_conversation(convo)

def _parse_conversation(convo: Dict) -> Iterator[Dict]:
    """Parse a single Anthropic conversation."""
    thread_id = convo.get("uuid", "")
    title = convo.get("name", "")
    chat_messages = convo.get("chat_messages", [])
    
    for msg in chat_messages:
        sender = msg.get("sender", "").lower()
        
        # Map sender to standard roles
        if sender == "human":
            role = "user"
        elif sender == "assistant":
            role = "assistant"
        else:
            role = sender or "unknown"
        
        # Content can be in 'text' or 'content' field
        content_list = msg.get("content", [])
        text = msg.get("text", "")
        
        # If content is a list of dicts (with type: text), extract text
        if isinstance(content_list, list) and content_list:
            content = "\n".join([
                item.get("text", "") 
                for item in content_list 
                if isinstance(item, dict) and item.get("type") == "text"
            ])
        else:
            content = text
        
        # Parse timestamp
        created_at_str = msg.get("created_at", "")
        try:
            # Anthropic uses ISO format like "2025-10-17T06:49:48.665364Z"
            dt = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
            created_at = dt.timestamp()
        except (ValueError, TypeError, AttributeError):
            created_at = 0.0
        
        yield {
            "thread_id": thread_id,
            "thread_title": title,
            "role": role,
            "content": content,
            "created_at": created_at
        }

