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
- Sample SQLite database (`examples/sample_archive.sqlite`) with demo data from all platforms
- Mermaid entity-relationship diagram in README documenting schema

### Technical Details
- Parser modules: `chatgpt.py`, `anthropic.py`, `grok.py`
- Normalized message format across all platforms
- Automatic deduplication on re-import
- WAL mode for optimal SQLite performance
- Batch commits every 2000 messages

### Documentation
- Enhanced Quick Start guide with sample database reference
- Added visual schema diagram showing message→FTS relationship
- Improved example queries section with practical use cases
- Updated footer with author attribution

### Repository Cleanup
- Removed all `__pycache__` directories
- Updated `.gitignore` to preserve sample database while excluding user-generated files
- Verified clean imports with no external project references
- Confirmed CLI executes successfully from repository root

[0.1.0]: https://github.com/1ch1n/chat-export-structurer/releases/tag/v0.1.0

