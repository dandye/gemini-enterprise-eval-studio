set dotenv-load := true

# Default environment file
env_file := ".env"

# Default recipe: list available commands
default:
    @just --list

# ------------------------------------------------------------------------------
# Setup & Dependency Management
# ------------------------------------------------------------------------------

# Setup local environment (.env and npm dependencies)
setup:
    #!/usr/bin/env bash
    set -e
    if [ ! -f "{{ env_file }}" ]; then
        echo "Creating {{ env_file }} from template..."
        cp .env.example "{{ env_file }}"
        echo "Created {{ env_file }} - please update values as needed."
    fi
    just install

# Install project dependencies
install:
    npm install

# ------------------------------------------------------------------------------
# Development Servers
# ------------------------------------------------------------------------------

# Start frontend development server in no-auth mode (default)
start:
    npx ng serve --host 0.0.0.0 --disable-host-check

# Start frontend development server with auth backend
start-auth:
    concurrently "tsx watch src/server/main.ts" "npx ng serve --configuration auth-development --host 0.0.0.0 --disable-host-check"

# ------------------------------------------------------------------------------
# Build & Compilation
# ------------------------------------------------------------------------------

# Build frontend production bundle (no-auth)
build:
    npm run build:no-auth

# Build full production bundle with auth backend
build-auth:
    npm run build:auth

# ------------------------------------------------------------------------------
# Testing
# ------------------------------------------------------------------------------

# Run all test suites (frontend + server)
test:
    npm run test

# Run frontend tests only
test-frontend:
    npm run test:frontend

# Run server tests only
test-server:
    npm run test:server

# ------------------------------------------------------------------------------
# Maintenance & Clean
# ------------------------------------------------------------------------------

# Clean build artifacts and temporary caches
clean:
    rm -rf dist/ out-tsc/ .angular/
