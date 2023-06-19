#!/bin/bash

# Find the process ID (PID) of the process running on port 5000
PID=$(sudo lsof -t -i :5000)

if [ -z "$PID" ]; then
  echo "No process found running on port 5000"
else
  # Terminate the process
  sudo kill "$PID"
  echo "Flask stopped"
fi
