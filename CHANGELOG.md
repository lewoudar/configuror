# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

## [0.3.0] - 2023-11-28

### Changed

- Upgraded libraries to the latest versions.

### Removed

- Dropped support for python 3.6 and python 3.7

## [0.2.0] - 2020-07-12

### Fixed

- Fixed a package version error.

## [0.1.3] - 2020-07-12

### Added

- Added utility functions to convert environment variables

### Changed

- Updated documentation on `Config.load_from_yaml` usage.
- Updated method `Config.getenv` to accept two additional parameters: `default` and `converter`.


## [0.1.2] - 2020-01-05

### Added

- Added usage of nox package for test automation.

### Changed

- Changed .travis.yml and appveyor.yml to take in account nox.
- Replaced pipenv by poetry to better manage package dependencies.

## [0.1.1] - 2019-05-15

### Added

- Added the link to the documentation in README.md.

### Fixed

- Changed the deploy phase in .travis.yml.

## [ 0.1.0] - 2019-05-14

### Added

- First version of the package.
