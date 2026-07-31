# Changelog

All notable changes to this project will be documented in this file.

The project follows [Semantic Versioning](https://semver.org/).

## [0.1.1] - 2026-07-31

### Added
- Standalone sample checker for Alinma and Al Rajhi SMS templates.
- GitHub Actions workflow that fails on unknown templates or parser errors.
- Separate file for the parser's fixed currency conversion rates.
- GNU Affero General Public License v3.0 only.

### Changed
- Informational sample messages are explicitly ignored instead of reported as unknown.
- Added support for the `مدفوعات سوا` transaction template.
- The parser can now be imported without automatically running `main()`.
- Invalid amount parsing raises a clear error instead of terminating the process directly.
- Updated the README with the correct repository URL, sample-check command, and license information.

### Fixed
- Avoided division by zero when a bank file contains no parsed messages.

## [0.1.0] - 2026-07-01

### Added
- Android SMS fetcher to JSON
- Alinma/Alrajhi bank SMS parser into readable JSON format
- Convert raw JSON transactions to CSV table
- Basic support for merchents & classification