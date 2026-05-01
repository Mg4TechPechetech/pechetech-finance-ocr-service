# PecheTech Finance OCR Service

## 📝 Overview
This Python-based machine learning service provides Optical Character Recognition (OCR) capabilities for financial documents. It extracts structured data from receipts, invoices, and other financial documents to automate data entry and processing.

## 🛠 Tech Stack
- **Language:** Python
- **Machine Learning:** PyTorch / OpenCV (Typical OCR stack)
- **Containerization:** Docker

## 📂 Project Structure
- `/src`: Source code
  - `/api`: REST API endpoints
  - `/core`: Core application configurations
  - `/models`: ML model definitions and wrappers
  - `/pipelines`: Data processing pipelines
  - `/services`: Business logic and external service integrations
- `/notebooks`: Jupyter notebooks for data exploration and OCR experiments
- `/data`: Sample datasets and training data
- `/tests`: API and ML pipeline tests
- `/docker`: Dockerfiles for API and background workers
- `/docs`: ML architecture documentation

## ⚙️ Prerequisites
- Python 3.9+
- Docker & Docker Compose

## 🚀 Setup & Installation
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🏃‍♂️ Running the Application
**Local API:**
```bash
python src/main.py
```

**Using Docker:**
```bash
docker build -t pechetech-finance-ocr -f docker/Dockerfile.api .
docker run -p 8000:8000 pechetech-finance-ocr
```

## 🧪 Testing
```bash
pytest tests/
```
