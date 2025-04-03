# app/services/data_service.py
import pandas as pd
import re

def extract_prices(prices_column):
    """Extract price values from the price column"""
    extracted_prices = prices_column.str.extract(r'(\bRs\.\s\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?)', expand=False)
    return extracted_prices

def clean_dataframe(df):
    """Clean the dataframe"""
    # Droping duplicate rows
    df.drop_duplicates(inplace=True)

    # Handling missing values
    df.dropna(subset=["Product-Titles", "Prices", "Ratings", "Reviews"], inplace=True)

    # Converting data types if needed
    df["Prices"] = extract_prices(df["Prices"])
    df["Ratings"] = pd.to_numeric(df["Ratings"], errors='coerce')
    df["Ratings-Count"] = pd.to_numeric(df["Ratings-Count"], errors='coerce')
    df["Question-Count"] = pd.to_numeric(df["Question-Count"], errors='coerce')

    # Removing special characters from Reviews column
    df["Reviews"] = df["Reviews"].str.replace('[^a-zA-Z0-9\s]', '', regex=True)

    # Reseting index after cleaning
    df.reset_index(drop=True, inplace=True)

    return df

def extract_numeric(column, df):
    """Extract numeric values from a column"""
    def process_value(x):
        try:
            return round(float(re.sub('[^0-9.]', '', str(x))), 3)
        except ValueError:
            return None

    return df[column].apply(process_value)

def extract_numeric_prices(prices_column, df):
    """Extract numeric price values"""
    def process_value(x):
        try:
            # Extracting numeric values using regular expression
            numeric_values = re.findall(r'\d+\.\d+|\d+,\d+|\d+', str(x))

            if numeric_values:
                # Replacing comma with an empty string and convert to float
                return float(numeric_values[0].replace(',', ''))
            else:
                return None
        except ValueError:
            return None

    return df[prices_column].apply(process_value)

def data_filteration(df):
    """Process and filter data for dashboard display"""
    # Extracting numeric values from specified columns
    df["Prices"] = extract_numeric_prices("Prices", df)
    df["Ratings"] = extract_numeric("Ratings", df)
    df["Ratings-Count"] = extract_numeric("Ratings-Count", df)
    df["Question-Count"] = extract_numeric("Question-Count", df)

    total_number_of_listings = len(df)
    average_product_price = df["Prices"].mean()
    average_product_ratings = df["Ratings"].mean()
    average_product_review_count = df["Ratings-Count"].mean()
    total_number_of_questions = df["Question-Count"].sum()

    top_five_products = df.nlargest(5, "Ratings")
    top_five_product_titles = top_five_products["Product-Titles"].tolist()

    top_five_product_urls = dict(zip(top_five_products["Product-Titles"], top_five_products["URLs"]))

    return (
        total_number_of_listings,
        average_product_price,
        average_product_ratings,
        average_product_review_count,
        total_number_of_questions,
        top_five_product_titles,
        top_five_product_urls
    )