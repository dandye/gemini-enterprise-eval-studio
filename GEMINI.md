# GEMINI.md

This file provides guidance to Gemini Code Assist and AI pair programmers working in this repository.

## Code Style and Communication

**CRITICAL: Never use emojis. Anywhere. Ever.**
- No emojis in code comments
- No emojis in commit messages
- No emojis in pull request descriptions
- No emojis in code review comments
- No emojis in documentation
- Emojis are unprofessional and must not be used in any context

## Shell and Environment Variables

- In code and shell examples, define environment variables first (e.g. `PROJECT_ID="..."`) and then reference them as `$PROJECT_ID`.

## Git Worktree and Path Conventions

- This repository adheres to the `gemini-enterprise-eval-studio__worktrees/` convention.
- Primary clone with `.git/` is located at `gemini-enterprise-eval-studio__worktrees/main`.
- Linked worktrees exist as sibling folders (e.g., `gemini-enterprise-eval-studio__worktrees/<branch_name>`).
- If removing a worktree containing git submodules under `external/`, deinitialize submodules first: `git submodule deinit --all -f` before removing the worktree.

## Project Structure

```text
.
├── .env.example          # Environment variable template
├── .gitignore            # Git ignore configuration
├── GEMINI.md             # AI coding instructions and repo guidelines
├── justfile              # Task runner (setup, install, start, test, build, clean)
├── package.json          # Node.js dependencies and npm scripts
├── angular.json          # Angular CLI workspace configuration
├── tsconfig.json         # TypeScript configuration
├── docs/                 # Technical documentation & architecture notes
├── external/             # Git submodules container
├── scripts/              # Helper & deployment automation scripts
├── src/                  # Application source code (Angular frontend + Express server)
└── tests/                # Automated tests
```

## Common Commands

| Task | Command | Description |
| :--- | :--- | :--- |
| **Setup** | `just setup` | Copy `.env.example` to `.env` and install npm dependencies |
| **Install** | `just install` | Run `npm install` |
| **Start (No-Auth)** | `just start` | Run frontend Angular development server (`npm run start:no-auth`) |
| **Start (Auth)** | `just start-auth` | Run backend + frontend in auth mode (`npm run start:auth`) |
| **Build** | `just build` | Build frontend production bundle |
| **Build (Auth)** | `just build-auth` | Build auth production bundle |
| **Test** | `just test` | Run full test suite (frontend + server) |
| **Test Frontend** | `just test-frontend`| Run frontend Angular unit tests |
| **Test Server** | `just test-server` | Run server Jasmine tests |
| **Clean** | `just clean` | Remove build artifacts, cache directories, and temporary files |
