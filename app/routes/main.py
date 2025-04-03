# app/routes/main.py
from flask import Blueprint, render_template, request, jsonify
from app.services.data_service import data_filteration
import pandas as pd

main_bp = Blueprint('main', __name__)

# Load data once when the application starts
try:
    csv_file_path = 'data/daraz.csv'
    df = pd.read_csv(csv_file_path)
except Exception as e:
    print(f"Error loading data: {e}")
    df = pd.DataFrame()  # Empty dataframe as fallback

@main_bp.route("/")
def dashboard():
    """Main dashboard route"""
    if df.empty:
        return render_template("error.html", message="Data not available")
    
    (
        total_number_of_listings,
        average_product_price,
        average_product_ratings,
        average_product_review_count,
        total_number_of_questions,
        top_five_product_titles,
        top_five_product_urls
    ) = data_filteration(df)
    
    return render_template(
        "HTML.html",  # You might want to rename this to something more descriptive like dashboard.html
        total_number_of_listings=total_number_of_listings,
        average_product_price=average_product_price,
        average_product_ratings=average_product_ratings,
        average_product_review_count=average_product_review_count,
        total_number_of_questions=total_number_of_questions,
        top_five_product_titles=top_five_product_titles,
        top_five_product_urls=top_five_product_urls
    )