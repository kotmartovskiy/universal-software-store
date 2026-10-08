# Catalog

The catalog stores software families, releases, packages, platforms and device profiles. Compatibility is evaluated by a deterministic rule engine.

## Compatibility model

A result is not just yes/no. The engine can return:

- **native** — package matches the target platform directly;
- **partial** — some constraints are unknown or conditional;
- **assisted** — emulator or compatibility layer is required;
- **unsupported** — a hard constraint prevents execution.

Rules currently consider OS family/version range, CPU architecture, ABI, RAM, runtime availability and compatibility mechanisms. The engine deliberately treats uncertain historical compatibility as uncertain instead of silently upgrading it to "native".
