# Universal Software Store

Universal catalog and compatibility layer for software across computing generations: modern Android, Windows and Linux through Symbian, DOS, classic Mac, Amiga, ZX Spectrum and other historical platforms.

Status: bootstrap architecture prototype.

Core model: Software -> Release -> Package -> Platform/OS -> Device -> Compatibility -> Source/Hash.

Principles:
- Local-first.
- Metadata remains useful when a binary cannot legally or technically be redistributed.
- Compatibility is a spectrum, not a boolean.
- LLMs may search and explain; deterministic compatibility rules remain authoritative.
- Every package should have provenance and integrity metadata.
- Modern and historical software share one data model.

Quick start: Python 3.11+, then `python server/app.py`, then http://127.0.0.1:8090/.

The project code is MIT licensed. Software binaries, trademarks and historical packages remain subject to their respective rights.
