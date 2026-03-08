# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-03-08

### Added
- Initial release of `eg4-monitor` library.
- Synchronous `EG4Client` using `requests`.
- Asynchronous `AsyncEG4Client` using `httpx`.
- Pydantic v2 models for `InverterData` and `BatteryInfo`.
- Automated session persistence to file to minimize login requests.
- Unit conversion properties for Voltage (V), Current (A), and Power (W).
- Command-line interface (CLI) for quick monitoring.
- GitHub Actions workflow for automated PyPI releases.
- Unit tests with `pytest` and request mocking.
- Example scripts for sync and async usage.
