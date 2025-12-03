#!/bin/bash

# Load NVM and start the development server
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Use the installed Node version
export PATH="$HOME/.nvm/versions/node/v20.19.5/bin:$PATH"

# Run the dev server
npm run dev
