
# Truck Tracking

A Django application for managing food truck schedules and locations.

## Description

This application helps track and manage daily food truck schedules, including their locations and cuisine types.

## Setup

1. Create and activate a virtual environment:
    In the project root directory, run the following commands:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
2. Install Python dependencies:
    
    ```bash
    pip install -r requirements.txt
    ```
3. Install Node.js dependencies:
    
    ```bash
    pnpm install // or npm install
    ```
4. Run Django migrations:
    
    ```bash
    python manage.py migrate
    ```
5. Start the Django development server:
    
    ```bash
    python manage.py runserver
    ```
6. Watch for CSS changes:
    Open a new terminal and run:
    ```bash
    pnpm dev // or npm run dev
    ```
