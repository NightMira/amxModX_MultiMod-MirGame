#!/bin/bash
echo "Setting up git hooks..."
git config core.hooksPath .githooks
echo "✅ Git hooks configured to use .githooks/"
chmod +x .githooks/*
echo "✅ Hooks made executable"
