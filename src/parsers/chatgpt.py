# chatgpt.py
# Parser for ChatGPT conversation exports
# Returns normalized Message dictionaries

import ijson
import json
from typing import List, Dict, Iterator

def extract_text_from_content(content):
    """Extract text from ChatGPT's content structure."""
    if not isinstance(content, dict):
        return ""
    parts = content.get("parts", [])
    if not isinstance(parts, list):
        return ""
    out = []
    for p in parts:
        if isinstance(p, str):
            out.append(p)
    return "\n".join([t for t in out if t])

def parse(input_path: str) -> Iterator[Dict]:
    """
    Parse ChatGPT export and yield normalized messages.
    
    Returns Iterator of dicts with:
    - thread_id: str
    - thread_title: str
    - role: str (user, assistant, system)
    - content: str
    - created_at: float (epoch timestamp)
    """
    # Check if array or single object
    with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
        first = f.read(4096)
    start = first.lstrip()[:1]
    
    if start == "[":
        # Stream array items
        with open(input_path, "rb") as f:
            for convo in ijson.items(f, "item"):
                if isinstance(convo, dict):
                    yield from _parse_conversation(convo)
    elif start == "{":
        # Single object
        with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
            try:
                obj = json.load(f)
            except Exception as e:
                raise SystemExit(f"[ERROR] Invalid JSON: {e}")
        if isinstance(obj, dict):
            yield from _parse_conversation(obj)
        else:
            raise SystemExit("[ERROR] Unexpected JSON structure")
    else:
        raise SystemExit("[ERROR] File doesn't look like JSON")

def _parse_conversation(convo: Dict) -> Iterator[Dict]:
    """Parse a single ChatGPT conversation."""
    thread_id = convo.get("id") or convo.get("conversation_id", "")
    title = convo.get("title", "")
    mapping = convo.get("mapping", {})
    
    messages = []
    for node_id, node in mapping.items():
        m = node.get("message")
        if not m:
            continue
        
        role = (m.get("author") or {}).get("role") or ""
        content_obj = m.get("content") or {}
        content = extract_text_from_content(content_obj)
        
        ts = m.get("create_time") or m.get("update_time")
        if not ts:
            continue
        
        messages.append({
            "thread_id": thread_id,
            "thread_title": title,
            "role": role,
            "content": content,
            "created_at": float(ts)
        })
    
    # Sort by timestamp
    messages.sort(key=lambda x: x["created_at"])
    
    for msg in messages:
        yield msg

