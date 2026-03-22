"""
app.py  –  Retail Analytics Dashboard
Flask backend with routes:
  GET  /            → Home / Dashboard
  POST /submit      → Accept sales entry, run ML prediction
  GET  /success     → Show prediction result
  GET  /analytics   → Aggregated analytics page
  GET  /api/chart-data → JSON chart data for JS charts
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "model"))

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from predict import predict_revenue
import random, datetime

app = Flask(__name__)
app.secret_key = "retail_dashboard_secret_2024"

# ── In-memory store (no DB required per guidelines) ──────────────
sales_records = []

CATEGORIES = ["Electronics", "Clothing", "Groceries", "Furniture", "Sports"]

# Pre-populate with demo data so charts aren't empty on first load
def _seed_demo_data():
    random.seed(7)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    for i, month in enumerate(months):
        for cat in CATEGORIES:
            units    = random.randint(50, 400)
            price    = random.uniform(200, 3000)
            discount = random.uniform(0, 30)
            rev      = predict_revenue(cat, units, discount, price)
            sales_records.append({
                "id":           i * len(CATEGORIES) + CATEGORIES.index(cat) + 1,
                "month":        month,
                "category":     cat,
                "units_sold":   units,
                "price":        round(price, 2),
                "discount_pct": round(discount, 1),
                "revenue":      rev,
                "timestamp":    datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            })

_seed_demo_data()

# ─────────────────────────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────────────────────────

@app.route("/")
def home():
    """Dashboard home – summary KPIs + recent records."""
    total_revenue = sum(r["revenue"] for r in sales_records)
    total_units   = sum(r["units_sold"] for r in sales_records)
    avg_discount  = (sum(r["discount_pct"] for r in sales_records) /
                     len(sales_records)) if sales_records else 0
    top_category  = _top_category()
    recent        = sales_records[-8:][::-1]          # last 8, newest first

    return render_template("index.html",
        total_revenue = f"{total_revenue:,.2f}",
        total_units   = f"{total_units:,}",
        avg_discount  = f"{avg_discount:.1f}",
        top_category  = top_category,
        recent_sales  = recent,
        categories    = CATEGORIES,
    )


@app.route("/submit", methods=["POST"])
def submit():
    """Validate form, predict revenue, save record, redirect to /success."""
    errors = []

    category     = request.form.get("category", "").strip()
    units_str    = request.form.get("units_sold", "").strip()
    price_str    = request.form.get("price", "").strip()
    discount_str = request.form.get("discount_pct", "").strip()
    month        = request.form.get("month", "").strip()

    # ── Validation ────────────────────────────────────────────────
    if not category or category not in CATEGORIES:
        errors.append("Please select a valid product category.")
    if not units_str or not units_str.isdigit() or int(units_str) <= 0:
        errors.append("Units sold must be a positive whole number.")
    if not price_str:
        errors.append("Price is required.")
    else:
        try:
            price = float(price_str)
            if price <= 0:
                raise ValueError
        except ValueError:
            errors.append("Price must be a positive number.")
            price = 0.0
    if not discount_str:
        errors.append("Discount % is required.")
    else:
        try:
            discount = float(discount_str)
            if not (0 <= discount <= 100):
                raise ValueError
        except ValueError:
            errors.append("Discount must be between 0 and 100.")
            discount = 0.0
    if not month:
        errors.append("Month is required.")

    if errors:
        # Re-render form with errors
        total_revenue = sum(r["revenue"] for r in sales_records)
        total_units   = sum(r["units_sold"] for r in sales_records)
        avg_discount  = (sum(r["discount_pct"] for r in sales_records) /
                         len(sales_records)) if sales_records else 0
        return render_template("index.html",
            errors        = errors,
            categories    = CATEGORIES,
            total_revenue = f"{total_revenue:,.2f}",
            total_units   = f"{total_units:,}",
            avg_discount  = f"{avg_discount:.1f}",
            top_category  = _top_category(),
            recent_sales  = sales_records[-8:][::-1],
            form_data     = request.form,
        ), 400

    # ── Prediction & save ─────────────────────────────────────────
    units   = int(units_str)
    revenue = predict_revenue(category, units, discount, price)

    record = {
        "id":           len(sales_records) + 1,
        "month":        month,
        "category":     category,
        "units_sold":   units,
        "price":        round(price, 2),
        "discount_pct": round(discount, 1),
        "revenue":      revenue,
        "timestamp":    datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    sales_records.append(record)

    # Pass result through session to /success
    session["last_result"] = record
    return redirect(url_for("success"))


@app.route("/success")
def success():
    """Show prediction result card."""
    result = session.pop("last_result", None)
    if not result:
        return redirect(url_for("home"))
    return render_template("index.html",
        success_result = result,
        categories     = CATEGORIES,
        total_revenue  = f"{sum(r['revenue'] for r in sales_records):,.2f}",
        total_units    = f"{sum(r['units_sold'] for r in sales_records):,}",
        avg_discount   = f"{(sum(r['discount_pct'] for r in sales_records)/len(sales_records)):.1f}",
        top_category   = _top_category(),
        recent_sales   = sales_records[-8:][::-1],
    )


@app.route("/api/chart-data")
def chart_data():
    """Return JSON for JS charts on the frontend."""
    # Revenue by category
    cat_rev = {c: 0 for c in CATEGORIES}
    for r in sales_records:
        cat_rev[r["category"]] += r["revenue"]

    # Revenue by month (last 6 months in order)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    month_rev = {m: 0 for m in months}
    for r in sales_records:
        if r["month"] in month_rev:
            month_rev[r["month"]] += r["revenue"]

    # Units by category
    cat_units = {c: 0 for c in CATEGORIES}
    for r in sales_records:
        cat_units[r["category"]] += r["units_sold"]

    return jsonify({
        "category_labels":  list(cat_rev.keys()),
        "category_revenue": [round(v, 2) for v in cat_rev.values()],
        "category_units":   [cat_units[c] for c in CATEGORIES],
        "month_labels":     months,
        "month_revenue":    [round(month_rev[m], 2) for m in months],
    })


# ── Helpers ───────────────────────────────────────────────────────
def _top_category():
    cat_rev = {c: 0 for c in CATEGORIES}
    for r in sales_records:
        cat_rev[r["category"]] += r["revenue"]
    return max(cat_rev, key=cat_rev.get) if cat_rev else "N/A"


if __name__ == "__main__":
    app.run(debug=True)
