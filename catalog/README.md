# Catalog core

SQLite is the source of truth for the first prototype. `schema.sql` defines software, platforms, devices, releases, packages and compatibility records. `engine/rules.py` contains deterministic compatibility rules.

This is deliberately conservative: incomplete metadata reduces confidence rather than being treated as proof of compatibility.
