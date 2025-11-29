        # Zero-Waste Meal Planner (Scaffold)
        This repository is a scaffolded prototype for the Zero-Waste Meal Planner capstone.
        It contains a simple FastAPI backend and a minimal React frontend.

## Quickstart (backend)
        - Install system deps: `tesseract-ocr`, `libzbar` (for pyzbar)
        - Python:
          ```
          cd backend
          python -m venv venv
          source venv/bin/activate
          pip install -r requirements.txt
          uvicorn app.main:app --reload --port 8000
          ```
        - Frontend:
          ```
          cd frontend
          npm install
          npm start
          ```
