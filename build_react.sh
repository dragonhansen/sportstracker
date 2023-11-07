#!/bin/bash
# Script that both builds the React frontend with Vite and launches the Flask server afterwards
echo "Building React app and launching Flask server"
cd frontend/
npx vite build
cd ..
python3 app.py

exit 0
