import pathlib

import psycopg2
import pandas as pd
from sql_queries import *



def process_data(cur, conn, directory, func):
    pass


def run_test_queries():
    pass




if __name__ == "__main__":
    # Connect Database
    conn = psycopg2.connect(
        "host=127.0.0.1 dbname=airbnbdb user=airbnb password=airbnb")
    cur = conn.cursor()

    listings_March = pd.read_csv("/content/drive/MyDrive/airbnb/listings.csv")
    listings_June = pd.read_csv("/content/drive/MyDrive/airbnb/listings_1.csv")
    listings_September = pd.read_csv("/content/drive/MyDrive/airbnb/listings_2.csv")
    listings_December = pd.read_csv("/content/drive/MyDrive/airbnb/listings_3.csv")

    calendar_March = pd.read_csv("/content/drive/MyDrive/airbnb/calendar.csv")
    calendar_June = pd.read_csv("/content/drive/MyDrive/airbnb/calendar_1.csv")
    calendar_September = pd.read_csv("/content/drive/MyDrive/airbnb/calendar_2.csv")
    calendar_December = pd.read_csv("/content/drive/MyDrive/airbnb/calendar_3.csv")

    reivew_March = pd.read_csv("/content/drive/MyDrive/airbnb/reviews.csv")
    reivew_June = pd.read_csv("/content/drive/MyDrive/airbnb/reviews_1.csv")
    reivew_September = pd.read_csv("/content/drive/MyDrive/airbnb/reviews_2.csv")
    reivew_December = pd.read_csv("/content/drive/MyDrive/airbnb/reviews_3.csv")


    listings_list = [listings_March, listings_June, listings_September, listings_December]
    calendar_list = [calendar_March, calendar_June, calendar_September, calendar_December]
    review_list = [reivew_March, reivew_June, reivew_September, reivew_December]

    listings = pd.concat(listings_list)
    calendar = pd.concat(calendar_list)
    review = pd.concat(review_list)

    run_test_queries()

    conn.close()