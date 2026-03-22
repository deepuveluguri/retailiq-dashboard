# 🛒 RetailIQ – Retail Analytics Dashboard

A full-stack ML-powered retail analytics and revenue forecasting web application built with Flask, Bootstrap 5, jQuery, Chart.js and Scikit-learn.

---

## 📌 Project Description

RetailIQ is a Retail Analytics Dashboard that allows users to:
- View live KPIs: total revenue, units sold, average discount, top-performing category
- Visualise sales trends through interactive charts (monthly revenue, category breakdown, units sold)
- Submit new sales records via a validated form
- Get **ML-predicted revenue** for any product category, pricing, and discount combination

---

## 🛠 Technologies Used

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12, Flask 3.0 |
| ML | Scikit-learn (Linear Regression), NumPy, Pandas, Joblib |
| Frontend | HTML5, Bootstrap 5, jQuery 3.7 |
| Charts | Chart.js 4 |
| Fonts | Google Fonts (Syne + DM Sans) |
| Icons | Bootstrap Icons |
| Storage | In-memory (session + list) |

---

## 📁 Project Structure

```
project/
├── app.py                  # Flask routes & application logic
├── requirements.txt        # Python dependencies
├── model/
│   ├── train_model.py      # Trains & saves the ML model
│   ├── predict.py          # Loads model.pkl & exposes predict_revenue()
│   └── model.pkl           # Trained LinearRegression model (auto-generated)
├── templates/
│   └── index.html          # Jinja2 template – full dashboard UI
└── static/
    ├── css/
    │   └── style.css       # Custom dark-theme styles
    ├── js/
    │   └── script.js       # jQuery validation + Chart.js rendering
    └── images/
        └── logo.png        # App logo
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/retailiq-dashboard.git
cd retailiq-dashboard
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Train the ML model
```bash
python model/train_model.py
```
> This generates `model/model.pkl` – required before running the app.

### 5. Run the Flask application
```bash
python app.py
```

### 6. Open in browser
```
http://127.0.0.1:5000
```

---

## 🚀 Flask Routes

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | Dashboard home – KPIs, charts, recent records |
| POST | `/submit` | Form submission, ML prediction, save record |
| GET | `/success` | Show prediction result (redirected from `/submit`) |
| GET | `/api/chart-data` | JSON API for Chart.js frontend |

---

## 📊 ML Model Details

- **Algorithm**: Linear Regression (Scikit-learn)
- **Features**: Category (label-encoded), Units Sold, Discount %, Price
- **Target**: Predicted Revenue
- **Training R²**: ~0.78 on held-out test set
- **Training data**: 500 synthetic retail samples

---

## 🖼 Screenshots

> Add screenshots of your running dashboard here after setup.

---

## 📝 License

For educational purposes – Full Stack Development Course Project.
