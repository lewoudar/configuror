# Changelog

The changelog format is based on a subset of [Keep a changelog](https://keepachangelog.com/en/1.0.0/).

## Version 0.2.0

Released in 2020-07-12

### Fixed

- Fixed a package version error.

## Version 0.1.3

Released in 2020-07-12

### Added

- Added utility functions to convert environment variables

### Changed

- Updated documentation on `Config.load_from_yaml` usage.
- Updated method `Config.getenv` to accept two additional parameters: `default` and `converter`.


## Version 0.1.2

Released on 2020-01-05

### Added

- Added usage of nox package for test automation.

### Changed

- Changed .travis.yml and appveyor.yml to take in account nox.
- Replaced pipenv by poetry to better manage package dependencies.

## Version 0.1.1

Released on 2019-05-15

### Added

- Added the link to the documentation in README.md.

### Fixed

- Changed the deploy phase in .travis.yml.

## Version 0.1.0

Released on 2019-05-14

### Added

- First version of the package.
