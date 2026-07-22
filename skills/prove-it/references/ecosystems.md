# Project-native command discovery

Use this reference only when repository documentation, CI configuration, and task runners do not already provide the verification commands. Never assume a tool is installed solely because a file is present.

## JavaScript and TypeScript

Inspect `package.json`, the active lockfile, workspace configuration, and CI workflows. Use the package manager selected by the lockfile. Prefer declared scripts such as `test`, `lint`, `typecheck`, `check`, and `build`.

Useful signals:

- `package-lock.json`: npm
- `pnpm-lock.yaml`: pnpm
- `yarn.lock`: Yarn
- `bun.lock` or `bun.lockb`: Bun
- `playwright.config.*`: browser checks
- `vitest.config.*`: Vitest
- `jest.config.*`: Jest

Do not invent a script that is absent from `package.json`.

## Python

Inspect `pyproject.toml`, `tox.ini`, `noxfile.py`, `pytest.ini`, `setup.cfg`, `requirements*.txt`, and CI workflows.

Common project-native entry points include:

- `python -m pytest`
- `python -m unittest`
- `tox`
- `nox`
- `python -m ruff check .`
- `python -m mypy <paths>`
- `python -m build`

Use the project's environment and documented dependency workflow. Do not create or update an environment unless authorized.

## Go

Inspect `go.mod`, `Makefile`, task configuration, and CI workflows.

Common checks include:

- `go test ./...`
- `go test -race ./...`
- `go vet ./...`
- `go build ./...`

Use race detection for concurrency-sensitive work when the environment supports it.

## Rust

Inspect `Cargo.toml`, workspace configuration, `rust-toolchain.toml`, `Makefile`, and CI workflows.

Common checks include:

- `cargo test`
- `cargo check --all-targets`
- `cargo clippy --all-targets --all-features -- -D warnings`
- `cargo build --release`

Respect feature flags and workspace boundaries used by CI.

## Java and Kotlin

Prefer checked-in wrappers and repository tasks:

- `./mvnw test`
- `./mvnw verify`
- `./gradlew test`
- `./gradlew check`
- `./gradlew build`

Inspect module selection and integration-test profiles before running an unbounded suite.

## .NET

Inspect solution files, project files, `global.json`, build scripts, and CI workflows.

Common checks include:

- `dotnet test`
- `dotnet build --no-restore`
- `dotnet format --verify-no-changes`
- `dotnet publish`

Do not assume restore or network access is authorized.

## Ruby

Inspect `Gemfile`, `Rakefile`, `.rspec`, and CI workflows. Prefer `bundle exec` with declared tasks such as `bundle exec rspec`, `bundle exec rake test`, and `bundle exec rubocop`.

## PHP

Inspect `composer.json`, `phpunit.xml*`, static-analysis configuration, and CI workflows. Prefer declared Composer scripts, `vendor/bin/phpunit`, `vendor/bin/phpstan`, or `vendor/bin/psalm` when dependencies already exist.

## Native and multi-language projects

Treat `Makefile`, `Justfile`, `Taskfile.yml`, Bazel, Buck, CMake, Meson, and repository scripts as the primary interface. Match CI flags, generated-code checks, and platform matrices where relevant.

## Frontend and visual work

Combine automated checks with rendered inspection. Exercise relevant viewport sizes, interaction states, loading, empty, error, keyboard, and responsive behavior. Use screenshots as visible-state evidence, not as proof of data or authorization behavior.

## Services and integrations

Prefer local emulators, disposable test environments, contract fixtures, or documented sandboxes. Do not contact production services, send messages, charge payments, mutate shared data, or expose credentials merely to increase verification coverage.
