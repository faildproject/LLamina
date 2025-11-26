# Changelog
Alle relevanten Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format orientiert sich an [Keep a Changelog](https://keepachangelog.com/de/1.1.0/)
und das Projekt nutzt [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
- Konfiguration via config.yaml

## [0.1.0] – 2025-11-25
Initialer stabiler Release des Proxys.

### Added
- Erster Release des LLamina Gateways
- Vollständige Unterstützung für LM Studio REST API (`/api/v0/...`)
- Unterstützung der OpenAI-kompatiblen API (`/v1/...`)
- Generische Proxy-Logik (GET/POST, Query-Parameter, Header)
- Konfigurierbares Backend via `.env`
- Projektstruktur mit FastAPI, Poetry und lokalem venv
- 1:1 Response-Durchleitung

### Changed
- –

### Fixed
- –

### Removed
- –

## Link-Referenzen
[Unreleased]: https://github.com/faildproject/llamina/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/faildproject/llamina/releases/tag/v0.1.0