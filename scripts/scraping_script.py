# from bs4 import BeautifulSoup
# import requests

import numpy as np
import pandas as pd
import os
import time
from IPython.display import display, HTML
import sqlite3

import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException


# Linking drivers
os.environ['PATH'] += "C:\\Users\\user\\Desktop\\Selenium Drivers\\chromedriver.exe"

def scrape_daraz_reviews(url):
    driver = webdriver.Chrome()

    driver.get(url)

    driver.implicitly_wait(35)

    reviews = []

    driver.execute_script("window.scrollTo(0, 500);")
    # driver.implicitly_wait(35)
    time.sleep(3)

    driver.execute_script("window.scrollTo(500, 800);")
    # driver.implicitly_wait(35)
    time.sleep(3)

    driver.execute_script("window.scrollTo(800, 1000);")
    # driver.implicitly_wait(35)
    time.sleep(3)

    driver.execute_script("window.scrollTo(1000, 1300);")
    # driver.implicitly_wait(35)
    time.sleep(3)

    driver.execute_script("window.scrollTo(1300, 1600);")
    # driver.implicitly_wait(35)
    time.sleep(3)

    try:
        reviews_container=WebDriverWait(driver, 35, ignored_exceptions=(StaleElementReferenceException, NoSuchElementException, TimeoutException,)).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div[9]/div[1]/div[1]/div/div/div/div[3]'))
        )

        # # Alternate approach
        # reviews_container = driver.find_element(By.XPATH, '/html/body/div[4]/div/div[9]/div[1]/div[1]/div/div/div/div[3]') # For, testing

        reviews_element = reviews_container.find_elements(By.CLASS_NAME, 'review-item')

        # print(len(reviews_element))

        # print(reviews_element[0].find_element(By.CLASS_NAME, "review-content-sl").text)
        for review in reviews_element:
            # print(review.find_element(By.CLASS_NAME, "review-content-sl").text)

            if (review.find_element(By.CLASS_NAME, "review-content-sl").text) != '':
                reviews.append(review.find_element(By.CLASS_NAME, "review-content-sl").text)

        # print(reviews)
    except (StaleElementReferenceException, NoSuchElementException, TimeoutException) as e:
        reviews.append('No Reviews')

    return reviews

def scrape_daraz_product_info(url):
    driver=webdriver.Chrome()

    # Maximizing the browser window to full screen
    driver.maximize_window()

    driver.get(url)

    driver.implicitly_wait(35)

    product_titles = []
    prices=[]
    brands = []
    reviews=[]
    ratings = []
    ratings_count = []
    number_of_questions = []
    specifications=[]
    urls=[]

    # List for flagging brand names
    mobile_brands=["samsung", "iphone", "infinix", "tecno", "redmi", "itel", "oppo", "vivo", "oneplus"] # List of potential mobile brands

    search_bar = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div/div[2]/div/div[2]/form/div/div[1]/input[1]")
    search_bar.send_keys('Mobile Phones' + Keys.RETURN)

    for page in range(1):
        # print(page)

        time.sleep(3)

        product_element_grid = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div/div/div[1]/div[2]')
        product_elements = product_element_grid.find_elements(By.CLASS_NAME, 'gridItem--Yd0sa')

        product_elements_sample=product_elements[:5]

        flag=False  # Flag check for filtering out the irrelevant listings
        count=0

        # print(len(product_elements))  #For, testing

        # Extracting product listings from the traversed page
        # for product_element in [product_elements[0]]:
        for _ in range(len(product_elements_sample)):
            time.sleep(3)

            product_element_grid = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div/div/div[1]/div[2]')
            product_elements = product_element_grid.find_elements(By.CLASS_NAME, 'gridItem--Yd0sa')

            if(_%4==0):
                driver.execute_script(f"window.scrollTo(0, {100*_});")
                # driver.implicitly_wait(35)
                time.sleep(3)

            product_element = product_elements[_]

            product_element.click()

            count+=1

            urls.append(driver.current_url)

            # print(urls)

            flag_element = WebDriverWait(driver, 35, ignored_exceptions=(
                StaleElementReferenceException, NoSuchElementException, TimeoutException,)).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'breadcrumb'))
                )

            # print(flag_element.text)

            if "Mobiles" in flag_element.text:
                flag=True

            if flag:

                product_title_variable=WebDriverWait(driver, 135, ignored_exceptions=(StaleElementReferenceException, NoSuchElementException, TimeoutException,)).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'pdp-mod-product-badge-title'))
                ).text
                product_titles.append(product_title_variable)

                # print(product_titles)

                price_variable=WebDriverWait(driver, 135, ignored_exceptions=(StaleElementReferenceException, NoSuchElementException, TimeoutException,)).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, 'pdp-product-price'))
                ).text
                prices.append(price_variable)

                # print(prices)

                brand_element=WebDriverWait(driver, 135, ignored_exceptions=(StaleElementReferenceException, NoSuchElementException, TimeoutException,)).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'pdp-product-brand'))
                )
                brand_element_value=brand_element.find_element(By.TAG_NAME, 'a').text

                brand_variable=''
                brand_variable_success = False

                # print(brand_element_value)

                if brand_element_value=="No Brand":

                    for brand in mobile_brands:

                        if brand in (product_title_variable.lower()):
                            brand_variable=brand
                            brand_variable_success=True

                    if brand_variable_success:
                        brands.append(brand_variable)
                    else:
                        brands.append("No Brand")
                else:
                    brand_variable = brand_element_value
                    brands.append(brand_variable)

                # print(brands)

                reviews_variable=scrape_daraz_reviews(driver.current_url)
                reviews.append(reviews_variable)

                # print(reviews)

                driver.execute_script("window.scrollTo(0, 700);")
                # driver.implicitly_wait(35)
                time.sleep(5)

                try:
                    rating_variable=WebDriverWait(driver, 35, ignored_exceptions=(StaleElementReferenceException, NoSuchElementException, TimeoutException,)).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'score'))
                    )
                    ratings.append(rating_variable.text)

                    # print(ratings)
                except (StaleElementReferenceException, NoSuchElementException, TimeoutException) as e:
                    ratings.append('No Ratings')

                try:
                    rating_count = WebDriverWait(driver, 35, ignored_exceptions=(StaleElementReferenceException, NoSuchElementException, TimeoutException,)).until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div[3]/div[2]/div/div[1]/div[4]/div[1]/div/div/a'))
                    ).text
                    ratings_count.append(rating_count.split()[0])

                    # print(ratings_count)
                except (StaleElementReferenceException, NoSuchElementException, TimeoutException) as e:
                    ratings_count('No Ratings Count')

                try:
                    element = WebDriverWait(driver, 35, ignored_exceptions=(
                    StaleElementReferenceException, NoSuchElementException, TimeoutException, TimeoutException,)).until(
                        EC.presence_of_element_located(
                            (By.XPATH, '/html/body/div[4]/div/div[3]/div[2]/div/div[1]/div[4]/div[1]/div/div/a[2]'))
                    )
                    question_count = element.text
                    number_of_questions.append(question_count.split()[0])
                except (StaleElementReferenceException, NoSuchElementException, TimeoutException) as e:
                    number_of_questions.append("No Questions")

                # print(number_of_questions)

                driver.execute_script("window.scrollTo(700, 1300);")
                # driver.implicitly_wait(35)
                time.sleep(3)

                driver.execute_script("window.scrollTo(1300, 1700);")
                # driver.implicitly_wait(35)
                time.sleep(3)

                driver.execute_script("window.scrollTo(1700, 2300);")
                # driver.implicitly_wait(35)
                time.sleep(5)

                try:
                    specification_elements = WebDriverWait(driver, 35, ignored_exceptions=(
                    StaleElementReferenceException, NoSuchElementException, TimeoutException,)).until(
                                EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div[9]/div[1]/div[2]/div/div/div[1]/div[1]'))
                            ).text.splitlines()
                    specifications.append(' '.join(specification_elements))
                except (StaleElementReferenceException, NoSuchElementException, TimeoutException) as e:
                    specifications.append('No Specifications')

                # print(specifications)
            else:
                continue

            # print(count)

            # driver.switch_to.window(driver.window_handles[0])
            driver.back()

        print(count)

        # # Page traversal script
        # try:
        #
        #     if page<=4:
        #         # print(page)
        #
        #         next_button_element=WebDriverWait(driver, 35, ignored_exceptions=(StaleElementReferenceException, NoSuchElementException,)).until(
        #             EC.presence_of_element_located((By.CLASS_NAME, 'ant-pagination '))
        #         )
        #         next_button_elements=next_button_element.find_elements(By.TAG_NAME, 'li')
        #         next_button=next_button_elements[(len(next_button_elements)-1)].find_element(By.TAG_NAME, 'a')
        #
        #         # # For, testing
        #         # print(len(next_button_elements))
        #         # print(next_button)
        #
        #         # # Alternate approach
        #         # next_button=WebDriverWait(driver, 35, ignored_exceptions=(StaleElementReferenceException, NoSuchElementException,)).until(
        #         #     EC.presence_of_element_located((By.XPATH, f'/html/body/div[3]/div/div[3]/div/div/div[1]/div[3]/div[2]/div/ul/li[{str(page+3)}]'))
        #         # )
        #
        #         # if page <=3:
        #         #     next_button=WebDriverWait(driver, 35, ignored_exceptions=(StaleElementReferenceException, NoSuchElementException,)).until(
        #         #         EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div[3]/div/div/div[1]/div[3]/div[2]/div/ul/li[10]/a'))
        #         #     )
        #         # else:
        #         #     next_button = WebDriverWait(driver, 35, ignored_exceptions=(
        #         #     StaleElementReferenceException, NoSuchElementException,)).until(
        #         #         EC.presence_of_element_located(
        #         #             (By.XPATH, '/html/body/div[3]/div/div[3]/div/div/div[1]/div[3]/div[2]/div/ul/li[11]/a'))
        #         #     )
        #
        #         driver.execute_script("arguments[0].click();", next_button)
        #
        #         driver.implicitly_wait(35)
        #         time.sleep(5)
        # except:
        #     print(f"Page Traversal Failed. Try Again")

    data = {
        "Product-Titles": product_titles,
        "Brands": brands,
        "Prices": prices,
        "Ratings": ratings,
        "Ratings-Count": ratings_count,
        "Question-Count": number_of_questions,
        "Specifications": specifications,
        "Reviews": reviews,
        "URLs": urls
    }

    df = pd.DataFrame(data)

    return df


if __name__ == "__main__":
    url = "https://www.daraz.pk/"

    # # Scraping the product details
    # scrape_daraz_product_info(url)  #For, testing
    daraz_df = scrape_daraz_product_info(url)

    # Inserting a unique identifier column
    daraz_df.insert(loc=0, column="referenceColumnID", value=list(np.arange(0, len(daraz_df))))

    # Splitting the data
    specification_df = daraz_df[
        ["referenceColumnID", "Product-Titles", "Brands", "Prices", "Ratings", "Question-Count", "Specifications"]]
    review_df = daraz_df[["referenceColumnID", "Reviews"]]

    # Exporting the processed data
    daraz_df.to_csv('daraz.csv', index=False)
    specification_df.to_csv('specifications.csv', index=False)
    review_df.to_csv('reviews.csv', index=False)

    print(daraz_df)
    print(specification_df)
    print(review_df)