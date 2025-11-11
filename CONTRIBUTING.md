# Contributing to Chat Export Structurer

Thanks for your interest! This tool uses a modular parser architecture that makes adding new platforms straightforward.

## Adding a New Parser

### 1. Create Parser Module

Create `src/parsers/your_platform.py`:

```python
from typing import Iterator, Dict

def parse(input_path: str) -> Iterator[Dict]:
    """
    Yield normalized messages with:
    - thread_id: str
    - thread_title: str
    - role: str ("user", "assistant", or "system")
    - content: str
    - created_at: float (Unix epoch timestamp)
    """
    # Your parsing logic here
    pass
```

### 2. Register Parser

Add to `src/ingest.py`:

```python
from parsers import chatgpt, anthropic, grok, your_platform

PARSERS = {
    "chatgpt": chatgpt,
    "anthropic": anthropic,
    "grok": grok,
    "your_platform": your_platform
}
```

### 3. Test It

```bash
python src/ingest.py --in export.json --format your_platform --test
```

### 4. Add Example

Include a sanitized sample in `examples/example_your_platform.json` (< 5KB).

## Pull Request Guidelines

**All pull requests require review and approval before merging.**

Before submitting:

- ✅ Test with real exports from the platform
- ✅ Include sanitized example file (remove personal data!)
- ✅ Update README's "Supported Formats" section
- ✅ No external API dependencies
- ✅ Follow existing code style
- ✅ All parsers must handle large files gracefully
- ✅ Fork the repository and create a feature branch
- ✅ Write clear commit messages

### Submission Process

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/new-parser`)
3. Make your changes and test thoroughly
4. Commit with clear messages
5. Push to your fork
6. Open a Pull Request with detailed description

The maintainer will review and provide feedback. Changes may be requested before approval.

## Code Style

- Use type hints where helpful
- Keep functions small and focused
- Handle edge cases gracefully
- Add docstrings to public functions

## Testing

Always test both modes:

```bash
# Dry run
python src/ingest.py --in examples/your_export.json --format your_platform --test

# Full import
python src/ingest.py --in examples/your_export.json --db test.sqlite --format your_platform
```

## Questions?

Open an issue: https://github.com/1ch1n/chat-export-structurer/issues

---

We appreciate all contributions! 🎉

