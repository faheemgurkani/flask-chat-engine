import numpy as np
import pandas as pd
import nltk
from nltk import word_tokenize
import re


# # for page in range(0, 5):
# #     print(f'/html/body/div[3]/div/div[3]/div/div/div[1]/div[3]/div[2]/div/ul/li[{str(page+3)}]')
#
#
# # Assume df is your existing DataFrame
# # For illustration purposes, let's create a sample DataFrame
# data = {'Name': ['Alice', 'Bob', 'Charlie'],
#         'Age': [25, 30, 22],
#         'City': ['New York', 'San Francisco', 'Los Angeles']}
# df = pd.DataFrame(data)
#
# # Display the original DataFrame
# print("Original DataFrame:")
# print(df)
#
# # Specify the columns you want to include in the new DataFrame
# selected_columns = ['Name', 'City']
#
# # Create a new DataFrame with the selected columns
# new_df = df[selected_columns]
#
# # Display the new DataFrame
# print("\nNew DataFrame with Selected Columns:")
# print(new_df)


# df = pd.read_csv("Ball_by_Ball.csv")
#
# print(df.columns)
#
# df.columns = [col.strip() for col in df.columns]  # For removing leading/trailing whitespaces
#
# print(df.columns)
#
# for index, row in df.iterrows():
#         print(row['Match_Id'])

#
# # Sample DataFrame creation (replace this with your actual scraping logic)
# data = {
#     'Product Titles': ['Product A', 'Product B', 'Product C'],
#     'Brands': ['Brand X', 'Brand Y', 'Brand Z'],
#     'Prices': [100, 150, 200],
#     'Ratings': [4.5, 3.8, 4.0],
#     'Specifications': ['Spec1', 'Spec2', 'Spec3'],
#     'reviews': ['Good product', 'Average', 'Excellent']
# }
# daraz_df = pd.DataFrame(data)
#
# # Inserting a unique identifier column
# daraz_df.insert(loc=0, column="referenceColumnID", value=list(np.arange(0, len(daraz_df))))
#
# # Splitting the data
# specification_df = daraz_df[["referenceColumnID", "Product Titles", "Brands", "Prices", "Ratings", "Specifications"]]
# review_df = daraz_df[["referenceColumnID", "reviews"]]
#
# # Print the DataFrames for testing
# print("Original DataFrame:")
# print(daraz_df)
#
# print("\nSpecification DataFrame:")
# print(specification_df)
#
# print("\nReview DataFrame:")
# print(review_df)


# my_list = [42, 1, 2]
#
# for _ in my_list:
#     # Code to be executed for each element in the list
#     print(_)


# # Example DataFrame
# data = {
#     "Product-Titles": ["Product1", "Product2", "Product3"],
#     "Brands": ["Brand1", "Brand2", "Brand3"],
#     "Prices": [10.99, 20.49, 15.99],
#     "Ratings": [4.5, 3.8, 4.2],
#     "Ratings-Count": [100, 80, 120],
#     "Question-Count": [10, 5, 8],  # Assuming this column contains the total number of questions
#     "Specifications": ["Spec1", "Spec2", "Spec3"],
#     "Reviews": [50, 30, 45],
#     "URLs": ["url1", "url2", "url3"]
# }
#
# df = pd.DataFrame(data)
#
# # Calculate the sum of the "Question-Count" column
# total_number_of_questions = df["Question-Count"].sum()
#
# print(f"Total Number of Questions: {total_number_of_questions}")


# # Example DataFrame
# data = {
#     "Product-Titles": ["Laptop", "Smartphone", "Camera", "Headphones", "Tablet"],
#     "Ratings": [4.5, 3.8, 4.2, 4.8, 4.0],
#     # Other columns...
# }
#
# df = pd.DataFrame(data)
#
# # Get the top five products based on ratings
# top_five_products = df.nlargest(5, "Ratings")
#
# # Extract product titles into a list
# top_five_product_titles = top_five_products["Product-Titles"]
#
# print("Top Five Product Titles:")
# print(top_five_product_titles)


# # Download NLTK resources (if not already downloaded)
# nltk.download('punkt')
#
# # Sample user input
# user_input = "Hello, how can I help you today?"
#
# print(user_input.lower())
#
# # Tokenize the user input
# tokens = word_tokenize(user_input.lower())
#
# # Remove punctuation from tokens
# tokens_without_punctuation = [token for token in tokens if token.isalpha()]
#
# # Print the result
# print(tokens)
# print(tokens_without_punctuation)


# # Using any with a list
# my_list = [False, True, False, False]
# result = any(my_list)
# print(result)  # Output: True
#
# # Using any with a generator expression
# my_generator = (x > 5 for x in range(3))
# result = any(my_generator)
# print(result)  # Output: True
#
# # Using any with an empty iterable
# empty_list = []
# result = any(empty_list)
# print(result)  # Output: False


# # Using next with a list
# my_list = [1, 2, 3]
# my_iterator = iter(my_list)
#
# # Get the next item
# item = next(my_iterator)
# print(item)  # Output: 1
#
# # Get the next item with a default value
# item = next(my_iterator, "No more items")
# print(item)  # Output: 2
#
# # Exhaust the iterator
# item = next(my_iterator, "No more items")
# print(item)  # Output: "No more items"


# # Sample DataFrame
# data = {
#     "Product-Titles": ["Product A", "Product B", "Product C"],
#     "Prices": ["$100.50", "$75.25", "$120.75"],
#     "Ratings": ["4.5", "3.8", "4.2"],
#     "Reviews": ["15", "10", "20"],
#     "Question-Count": [5, 3, 7],
# }
#
# df = pd.DataFrame(data)
#
# def extract_numeric(column):
#     return df[column].apply(lambda x: re.sub('[^0-9.]', '', str(x)) if pd.notnull(x) else x).astype(float)
#
# def data_filteration(df):
#     # Extract numeric values from specified columns
#     df["Prices"] = extract_numeric("Prices")
#     df["Ratings"] = extract_numeric("Ratings")
#     df["Reviews"] = extract_numeric("Reviews")
#
#     total_number_of_listings = len(df)
#     average_product_price = df["Prices"].mean()
#     average_product_ratings = df["Ratings"].mean()
#     average_product_review_count = df["Reviews"].mean()
#     total_number_of_questions = df["Question-Count"].sum()
#
#     return (
#         total_number_of_listings,
#         average_product_price,
#         average_product_ratings,
#         average_product_review_count,
#         total_number_of_questions
#     )
#
# result = data_filteration(df)
#
# print("Total Number of Listings:", result[0])
# print("Average Product Price:", result[1])
# print("Average Product Ratings:", result[2])
# print("Average Product Review Count:", result[3])
# print("Total Number of Questions:", result[4])


# # Sample DataFrame
# data = {
#     "Product-Titles": ["Product A", "Product B", "Product C"],
#     "Prices": ["Rs. 106,999\nRs. 119,000-10%", "Rs. 150,000", "Rs. 120,755"],
#     "Ratings": ["4.565", "3.899", "4.257"],
#     "Reviews": ["15.234", "10.123", "20.456"],
#     "Question-Count": [5, 3, 7],
# }
#
# df = pd.DataFrame(data)
#
#
# def extract_numeric_prices(prices_column):
#     def process_value(x):
#         try:
#             # Extract the first part before the newline character
#             first_part = x.split('\n')[0]
#
#             # Remove non-numeric characters and convert to float
#             return float(re.sub('[^0-9.]', '', first_part))
#         except ValueError:
#             # Handle the case where conversion fails
#             return None
#
#     return df[prices_column].apply(process_value)
#
#
# # Extract numeric values from the "Prices" column
# df["Prices"] = extract_numeric_prices("Prices")
#
# # Calculate the average of the extracted prices
# average_price = df["Prices"].mean()
#
# # Display the modified DataFrame and average price
# print(df)
# print(f"Average Price: {average_price:.03f}")


def extract_numeric_prices(prices_column, df):
    def process_value(x):
        try:
            # Extract numeric values using regular expression
            numeric_values = re.findall(r'\d+\.\d+|\d+,\d+|\d+', str(x))

            if numeric_values:
                # Replace comma with an empty string and convert to float
                return float(numeric_values[0].replace(',', ''))
            else:
                return None
        except ValueError:
            # Handle the case where conversion fails
            return None

    return df[prices_column].apply(process_value)

# Example usage
data = {
    "Product-Titles": ["Product A", "Product B", "Product C", "Product D", "Product E"],
    "Prices": ["Rs. 34,999", "Rs. 106,999", "Rs. 49,999", "Rs. 19,399", "Rs. 64,499"]
}

df = pd.DataFrame(data)

# Call the modified function
df["Prices"] = extract_numeric_prices("Prices", df)

# Display the DataFrame
print(df)