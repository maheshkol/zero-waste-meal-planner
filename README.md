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
=================================================================================================

---

# **📦 Zero-Waste Meal Planner — Agentic AI Capstone Project**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green.svg)
![React](https://img.shields.io/badge/React-Frontend-blue.svg)

---

## 🌱 **Overview**

The **Zero-Waste Meal Planner** is an **Agentic AI Concierge System** that helps households **reduce food waste**, **optimize meal planning**, and **minimize grocery costs**.
It works by intelligently understanding what food you already have and generating weekly meal plans that use up leftovers and soon-to-expire items.

This project is built as a **full-stack AI capstone**, featuring:

* Pantry image recognition (OCR + barcode scanning)
* Recipe retrieval using sentence-transformers + FAISS
* Meal planning optimization (Greedy + ILP)
* Optional LLM-powered recipe adaptation
* React-based frontend demo
* Dockerized deployment

---

## ⭐ **Key Features**

### 🥫 **Pantry Intelligence**

* Upload a photo of pantry/fridge items
* OCR (Tesseract) + Barcode scanning (zbar/pyzbar)
* Manual ingredient entry support

### 🍽️ **Smart Meal Planning**

* Recommends recipes based on:

  * What you already have
  * Expiry dates
  * Dietary preferences
* 7-day weekly meal planner (prototype)

### 🧮 **Optimized Grocery List**

* Generates a minimal shopping list
* Avoids duplicate items
* Shows exactly what’s missing for your chosen recipes

### 🤖 **AI Recipe Adaptation (LLM Optional)**

* Suggests substitutions
* Adjusts ingredient quantities
* Removes unavailable ingredients

### 💻 **Frontend (React)**

* Simple UI to upload images
* View pantry items
* Generate weekly plans
* View grocery list

---

## 🏗️ **Architecture**

```
┌────────────────────────┐       ┌──────────────────────────────┐
│      React Frontend     │ <───> │        FastAPI Backend       │
└────────────────────────┘       └──────────────────────────────┘
                                        │
                                        │
             ┌─────────────────────────────────────────────────────────┐
             │                 Backend Components                      │
             ├─────────────────────────────────────────────────────────┤
             │  • Image Processing: Tesseract OCR + pyzbar             │
             │  • Recipe Matcher: SentenceTransformers + FAISS        │
             │  • Optimizer: Greedy + ILP (pulp)                      │
             │  • LLM Adapter: recipe rewriting (OpenAI optional)     │
             └─────────────────────────────────────────────────────────┘
```

---

## 🚀 **Getting Started**

### **1. Clone the Repository**

```bash
git clone https://github.com/your-username/zero-waste-meal-planner.git
cd zero-waste-meal-planner
```

---

## ⚙️ **Backend Setup (FastAPI)**

### **Install system dependencies**

```bash
sudo apt install tesseract-ocr
sudo apt install libzbar0
```

### **Create virtual environment**

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### **Run FastAPI server**

```bash
uvicorn app.main:app --reload --port 8000
```

Server runs at:

👉 [http://localhost:8000](http://localhost:8000)

---

## 🖥️ **Frontend Setup (React)**

```bash
cd frontend
npm install
npm start
```

Frontend runs at:

👉 [http://localhost:3000](http://localhost:3000)

---

## 🐳 **Docker Setup (Optional)**

```bash
docker-compose up --build
```

Runs both frontend + backend in containers.

---

## 🔑 **Environment Variables**

Create `backend/.env`:

```
OPENAI_API_KEY=your_key_here
```

Leave blank if not using LLM-based recipe rewriting.

---

## 🔍 **API Examples**

### Upload Pantry Photo

```bash
curl -X POST "http://localhost:8000/api/pantry/upload-photo?user_id=test_user" \
  -F "file=@fridge_photo.jpg"
```

### Generate Weekly Plan

```bash
curl -X POST "http://localhost:8000/api/plan/generate" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test_user"}'
```

### Adapt a Recipe (LLM)

```bash
curl -X POST "http://localhost:8000/api/recipes/adjust" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test_user","recipe_id":"r1"}'
```

---

## 🧪 **Testing**

Recommended tests:

* Image parsing
* Recipe similarity ranking
* Meal plan output shape
* Grocery list minimization

You can extend with pytest test suite.

---

## 📈 **Future Enhancements**

* Full mobile app (React Native)
* Voice-based planning agent
* Integration with grocery delivery APIs
* Smart expiry prediction model
* User personalization (calories, cuisine)

---

## 🤝 **Contributing**

1. Fork this repo
2. Create `feature/your-feature-name`
3. Submit a pull request

---

## 📜 **License**

MIT License — free to use and modify.

---



