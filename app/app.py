import pandas as pd
import nltk
from nltk import word_tokenize
import re
import random

from flask import Flask, render_template, request, jsonify


app=Flask(__name__)

def extract_prices(prices_column):
    # Extracting the first price in each row
    extracted_prices = prices_column.str.extract(r'(\bRs\.\s\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?)', expand=False)

    return extracted_prices

def clean_dataframe(df):
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

def extract_numeric(column):

    def process_value(x):

        try:
            return round(float(re.sub('[^0-9.]', '', str(x))), 3)
        except ValueError:
            return None

    return df[column].apply(process_value)

def extract_numeric_prices(prices_column, df):

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

csv_file_path = 'daraz.csv'
df = pd.read_csv(csv_file_path)

# Cleaning the data frame
df = clean_dataframe(df)

df["Prices"] = extract_numeric_prices("Prices", df)
df["Ratings"] = extract_numeric("Ratings")
df["Ratings-Count"] = extract_numeric("Ratings-Count")
df["Question-Count"] = extract_numeric("Question-Count")

data=pd.DataFrame(df)

def data_filteration(df):
    # Extracting numeric values from specified columns
    df["Prices"] = extract_numeric_prices("Prices", df)
    df["Ratings"] = extract_numeric("Ratings")
    df["Ratings-Count"] = extract_numeric("Ratings-Count")
    df["Question-Count"] = extract_numeric("Question-Count")

    total_number_of_listings=len(df)
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

@app.route("/")
def dashboard():
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
        "HTML.html",
        total_number_of_listings=total_number_of_listings,
        average_product_price=average_product_price,
        average_product_ratings=average_product_ratings,
        average_product_review_count=average_product_review_count,
        total_number_of_questions=total_number_of_questions,
        top_five_product_titles=top_five_product_titles,
        top_five_product_urls=top_five_product_urls
    )

# Keyword and sentence based corpora for the greetings and salutations
greetings_corpus = [
    "Hello", "Hi", "Hey", "Good morning", "Good afternoon", "Good evening", "Greetings", "Salutations",
    "Howdy", "What's up?", "Hey there", "Hi there", "Hello there", "Hiya", "Yo", "Hi folks", "Morning",
    "Afternoon", "Evening", "Hi everyone", "Hello everyone", "Good day", "How's it going?", "How are you doing?",
    "How are you?", "Nice to see you", "Nice to meet you", "Pleasure to meet you", "Welcome", "Hi friends",
    "Hey friend", "Hi buddy", "Hey buddy", "Hi pal", "Hey pal", "Greetings and salutations", "Long time no see",
    "It's been a while", "What's happening?", "How's everything?", "How's life treating you?", "Hi team", "Hello team",
    "Hey team", "Hi squad", "Hello squad", "Hey squad", "Howdy partner", "How's your day?", "How's your day going?",
    "Hi y'all", "Hello y'all", "Hey y'all", "Hi there, stranger", "Hello from the other side"
]

# Keyword corporas for the scraped data
product_titles_keywords = [
    "product",
    "item",
    "title",
    "goods",
    "merchandise",
    "inventory",
    "name",
    "description",
    "model",
    "catalog",
    "listing",
    "identification",
    "SKU",
]
brands_keywords = [
    "brand",
    "brands",
    "manufacturer",
    "maker",
    "producer",
    "company",
    "label",
    "trademark",
    "logo",
    "origin",
    "source",
]
prices_keywords = [
    "price",
    "cost",
    "value",
    "amount",
    "expense",
    "fee",
    "charge",
    "worth",
    "rate",
    "payment",
]
ratings_keywords = [
    "rating",
    "average rating",
    "customer rating",
    "star rating",
    "user rating",
    "client rating",
    "feedback",
    "evaluation",
]
ratings_count_keywords = [
    "number of ratings",
    "ratings count",
    "customer ratings",
    "total ratings",
    "quantity of ratings",
]
question_count_keywords = [
    "question count",
    "questions",
    "inquiries",
    "query count",
    "interrogations",
]
specifications_keywords = [
    "specifications",
    "specs",
    "details",
    "features",
    "attributes",
    "characteristics",
    "specs",
]
reviews_keywords = [
    "reviews",
    "customer reviews",
    "user reviews",
    "client reviews",
    "feedback",
    "evaluations",
]
urls_keywords = [
    "url",
    "link",
    "website",
    "web address",
    "hyperlink",
    "internet address",
    "uniform resource locator",
]

def process_user_input(user_input):
    tokens = word_tokenize(user_input.lower())
    tokens_without_punctuation = [token for token in tokens if token.isalpha()]

    # Flagging if the user input contains greetings
    if any(greeting.lower() in tokens_without_punctuation for greeting in greetings_corpus):
        random_greeting = random.choice(greetings_corpus)
        return f"{random_greeting}! How can I assist you?"

    # Checking if the user is asking about a specific product; based on dataframe-based classifications
    brand_keywords_present = any(keyword in tokens_without_punctuation for keyword in brands_keywords)
    brand_name = next((brand.lower() for brand in data["Brands"].str.lower() if brand.lower() in tokens_without_punctuation), None)

    if brand_name:
        return f"You mentioned {brand_name}. What would you like to know about {brand_name}?"

    mentioned_brand_keyword = next((keyword for keyword in brands_keywords if keyword in tokens_without_punctuation), None)

    if mentioned_brand_keyword:
        return f"You mentioned {mentioned_brand_keyword}. What specific information are you looking for related to {mentioned_brand_keyword}?"

    column_keywords = {
        "price": "Prices",
        "rating": "Ratings",
        "rating count": "Ratings-Count",
        "question count": "Question-Count"
    }

    # Handling top products based on a specific column
    top_keywords = ["top", "best", "highest"]
    for top_keyword in top_keywords:
        for key, column in column_keywords.items():
            if key in tokens_without_punctuation and top_keyword in tokens_without_punctuation:
                top_products = data.nlargest(5, column)
                top_product_titles = [' '.join(title.split()[:3]) for title in top_products["Product-Titles"]]

                return f"Here are the top five products based on {column}:\n {', '.join(top_product_titles)}"



    # # Handling user-specified columns
    # user_columns = [column_keywords[key] for key in column_keywords if key in tokens_without_punctuation]
    #
    # if user_columns:
    #     user_price_mentioned = any(token.isdigit() for token in tokens_without_punctuation)
    #     user_price = next(int(token) for token in tokens_without_punctuation if token.isdigit()) if user_price_mentioned else None
    #
    #     if user_price_mentioned:
    #         return f"You mentioned a {', '.join(user_columns)} of {user_price}. What specific products are you interested in around this {', '.join(user_columns)}?"
    #
    #     return f"What specific {', '.join(user_columns)} are you looking for?"



    # Handling in-between price queries
    if "between" in tokens_without_punctuation and "and" in tokens_without_punctuation:
        between_index = tokens_without_punctuation.index("between")
        and_index = tokens_without_punctuation.index("and")

        try:
            # Extracting numeric values using regular expressions
            lower_limit_match = re.search(r'\b\d+\b', tokens_without_punctuation[between_index + 1])
            upper_limit_match = re.search(r'\b\d+\b', tokens_without_punctuation[and_index + 1])

            # print(lower_limit_match)
            # print(upper_limit_match)

            # Converting the matched values to integers
            lower_limit = int(lower_limit_match.group()) if lower_limit_match else None
            upper_limit = int(upper_limit_match.group()) if upper_limit_match else None

            # Filtering products based on the price range
            if lower_limit is not None and upper_limit is not None:
                products_in_price_range = data[(data["Prices"] >= lower_limit) & (data["Prices"] <= upper_limit)]

                if not products_in_price_range.empty:
                    products_in_price_range_titles = [' '.join(title.split()[:3]) for title in
                                                      products_in_price_range["Product-Titles"]]
                    return f"Here are the products within the price range of Rs. {lower_limit} to Rs. {upper_limit}: {', '.join(products_in_price_range_titles)}"
                else:
                    return f"No products found within the specified price range."

        except (ValueError, IndexError):
            pass

    # Handling under-over price queries
    if "under" in tokens_without_punctuation and "over" in tokens_without_punctuation:
        under_index = tokens_without_punctuation.index("under")
        over_index = tokens_without_punctuation.index("over")
        under_value = int(tokens_without_punctuation[under_index + 1]) if under_index + 1 < len(tokens_without_punctuation) and tokens_without_punctuation[under_index + 1].isdigit() else None
        over_value = int(tokens_without_punctuation[over_index + 1]) if over_index + 1 < len(tokens_without_punctuation) and tokens_without_punctuation[over_index + 1].isdigit() else None

        if under_value is not None and over_value is not None:
            products_in_price_range = data[(data["Prices"] <= under_value) & (data["Prices"] >= over_value)]
            products_in_price_range_titles = [' '.join(title.split()[:3]) for title in products_in_price_range["Product-Titles"]]
            return f"Here are the products under Rs. {under_value} and over Rs. {over_value}: {', '.join(products_in_price_range_titles)}"

    # Handling best products based on a specific column
    ranking_keywords = ["best", "worst", "top", "bottom", "highest", "lowest"]
    for ranking_keyword in ranking_keywords:
        if ranking_keyword in tokens_without_punctuation:
            for column in column_keywords.values():
                if column in tokens_without_punctuation:
                    top_or_bottom_products = data.nsmallest(5, column) if ranking_keyword in ["best", "top", "lowest"] else data.nlargest(5, column)
                    top_or_bottom_product_titles = [' '.join(title.split()[:3]) for title in top_or_bottom_products["Product-Titles"]]
                    return f"Here are the {ranking_keyword} five products based on {column}: {', '.join(top_or_bottom_product_titles)}"

    # Handling specs queries
    if "specs" in tokens_without_punctuation or ("with" in tokens_without_punctuation and "specs" in tokens_without_punctuation):
        specs_keywords_present = any(keyword in tokens_without_punctuation for keyword in specifications_keywords)
        if specs_keywords_present:
            # Extract relevant specs information
            specs_info = {}  # Assuming a dictionary to store specs information

            # Extracting specs information from the user input
            for keyword in specifications_keywords:
                if keyword in tokens_without_punctuation:
                    spec_value = next((value for value in data["Specifications"] if value.lower() in tokens_without_punctuation), None)

                    if spec_value is not None:
                        # Assuming spec information is stored as key-value pairs in specs_info
                        specs_info[keyword] = spec_value

            # Us specs_info to filter products from your main DataFrame (data)
            products_matching_specs = data[data["Specifications"].apply(lambda x: all(spec.lower() in x.lower() for spec in specs_info.values()))]

            if not products_matching_specs.empty:
                products_matching_specs_titles = [' '.join(title.split()[:3]) for title in products_matching_specs["Product-Titles"]]
                return f"Here are the products matching the specifications: {', '.join(products_matching_specs_titles)}"
            else:
                return "I'm sorry, there are no products matching the specified specifications."

    # Handling phone queries
    if any(phone.lower() in tokens_without_punctuation for phone in data["Product-Titles"].str.lower()):
        phone_title = next((phone for phone in data["Product-Titles"] if phone.lower() in tokens_without_punctuation), None)
        return f"What specific information are you looking for regarding {phone_title}?"

    return "I'm sorry, I couldn't understand your request."

@app.route("/get", methods=["POST"])
def get_bot_response():
    user_input = request.form.get("msg")

    bot_response = process_user_input(user_input)

    # # For illustration purposes
    # bot_response = f"Echo: {user_input}"

    return jsonify({"bot_response": bot_response})


if __name__ == '__main__':
    app.run(debug=True, port=2023)
