# grok.py
# Parser for Grok (X.AI) conversation exports
# Returns normalized Message dictionaries

import json
from typing import List, Dict, Iterator
from datetime import datetime

def parse(input_path: str) -> Iterator[Dict]:
    """
    Parse Grok export and yield normalized messages.
    
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
    
    # Grok exports have a 'conversations' key
    if not isinstance(data, dict) or "conversations" not in data:
        raise SystemExit("[ERROR] Grok export should have 'conversations' key")
    
    conversations = data["conversations"]
    
    for conv_wrapper in conversations:
        yield from _parse_conversation(conv_wrapper)

def _parse_conversation(conv_wrapper: Dict) -> Iterator[Dict]:
    """Parse a single Grok conversation wrapper."""
    conversation = conv_wrapper.get("conversation", {})
    responses = conv_wrapper.get("responses", [])
    
    thread_id = conversation.get("id", "")
    title = conversation.get("title", "")
    
    for resp_wrapper in responses:
        resp = resp_wrapper.get("response", {})
        
        if not resp:
            continue
        
        sender = resp.get("sender", "").lower()
        
        # Map sender to standard roles
        if sender == "human":
            role = "user"
        elif sender == "assistant":
            role = "assistant"
        else:
            role = sender or "unknown"
        
        # Content is in 'message' field
        content = resp.get("message", "")
        
        # Parse timestamp - Grok uses MongoDB-style date format
        create_time = resp.get("create_time", {})
        
        if isinstance(create_time, dict):
            # MongoDB format: {"$date": {"$numberLong": "1754341171713"}}
            date_val = create_time.get("$date", {})
            if isinstance(date_val, dict):
                number_long = date_val.get("$numberLong", "0")
                created_at = float(number_long) / 1000.0  # Convert ms to seconds
            elif isinstance(date_val, str):
                # ISO format
                try:
                    dt = datetime.fromisoformat(date_val.replace("Z", "+00:00"))
                    created_at = dt.timestamp()
                except (ValueError, TypeError, AttributeError):
                    created_at = 0.0
            else:
                created_at = 0.0
        elif isinstance(create_time, (int, float)):
            created_at = float(create_time)
        else:
            created_at = 0.0
        
        yield {
            "thread_id": thread_id,
            "thread_title": title,
            "role": role,
            "content": content,
            "created_at": created_at
        }

