# Changelog

All notable changes to Chat Export Structurer will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-11

### Added
- Multi-platform parser support (ChatGPT, Anthropic Claude, Grok)
- Unified CLI interface with `--format` flag
- Streaming JSON ingestion with `ijson`
- SQLite FTS5 full-text search support
- SHA1-based stable message and thread IDs
- Test mode (`--test`) for preview without database writes
- Modular parser architecture in `src/parsers/`
- Example files for all supported formats
- Comprehensive README with usage examples
- MIT License for maximum adoption and flexibility

### Technical Details
- Parser modules: `chatgpt.py`, `anthropic.py`, `grok.py`
- Normalized message format across all platforms
- Automatic deduplication on re-import
- WAL mode for optimal SQLite performance
- Batch commits every 2000 messages

[0.1.0]: https://github.com/1ch1n/chat-export-structurer/releases/tag/v0.1.0

