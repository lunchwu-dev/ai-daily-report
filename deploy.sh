#!/bin/bash
export CLOUDFLARE_API_TOKEN=zObKBHBOkVJCVlICs4w7AYQyw-HWz3SWnys84fJB
echo "Deploying to ai-daily-report..."
wrangler pages deploy . --project-name=ai-daily-report --branch=main --commit-dirty=true 2>&1
echo "Exit code: $?"
