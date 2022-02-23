# DROP TABLES
review_drop = "DROP TABLE IF EXISTS review"
calendar_drop = "DROP TABLE IF EXISTS calendar"
listings_drop = "DROP TABLE IF EXISTS listings"
reviewer_drop = "DROP TABLE IF EXISTS reviewer"
time_drop = "DROP TABLE IF EXISTS dim_date"

# CREATE TABLES
review_create = ("""
    CREATE TABLE IF NOT EXISTS review (
        listings_id int,
        review_id int,
        date timestamp,
        comment varchar
    )
""")

calendar_create = ("""
    CREATE TABLE IF NOT EXISTS calendar (
        listing_id int,
        date timestamp,
        available char (1),
        price numeric
    )
""")

listings_create = ("""
    CREATE TABLE IF NOT EXISTS listings(
        id PRIMARY KEY,
        name varchar,
        room_type varchar,
        number_of_reviews int,
        host_id int,
        host_name varchar,
        host_is_superhost char (1),
        host_listings_count numeric,
        neighbourhood varchar,
        property_type varchar,
        accommodates int,
        availability_30 int,
        bedrooms numeric,
        price numeric,
        minimum_nights int,
        maximum_nights int
    )
""")

reviewer_create = ("""
    CREATE TABLE IF NOT EXISTS reviewer (
        reviewer_id int PRIMARY KEY,
        reviewer_name varchar
    )
""")

time_create = ("""
    CREATE TABLE IF NOT EXISTS time (
        date_time TIMESTAMP PRIMARY KEY,
        day int,
        month int,
        year int,
        week int,
        dayofweek int
    )
""")

# INSERT RECORDS
review_insert = ("""
    INSERT INTO review 
    (listings_id, review_id, date_time, comment)
    VALUES (%s, %s, %s, %s)
""")

calendar_insert = ("""
    INSERT INTO calendar 
    (listing_id, date_time, available, price)
    VALUES (%s, %s, %s, %s)
""")

listings_insert = ("""
    INSERT INTO listings 
    (listing_id, name, room_type, number_of_reviews, host_id, host_name, host_is_superhost, host_listings_count, neighbourhood, property_type, accommodates, availability_30, bedrooms, price, minimum_nights, maximum_nights)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (listing_id) DO NOTHING
""")

reviewer_insert = ("""
    INSERT INTO reviewer 
    (reviewer_id, reviewer_name)
    VALUES (%s, %s)
    ON CONFLICT (review_id) DO NOTHING
""")

time_insert = ("""
    INSERT INTO time 
    (date_time, day, month, year, week, dayofweek)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (date_time) DO NOTHING
""")


# CHECK RECORDS

review_check = ("""
    SELECT * FROM review LIMIT 5
""")

calendar_check = ("""
    SELECT * FROM calendar LIMIT 5
""")

listings_check = ("""
    SELECT * FROM listings LIMIT 5
""")

reviewer_check = ("""
    SELECT * FROM reviewer LIMIT 5
""")

time_check = ("""
    SELECT * FROM time LIMIT 5
""")

# FIND INSIGHT


# QUERY LISTS
create_table_queries = [
    review_create,
    calendar_create,
    listings_create,
    reviewer_create,
    time_create 
]

drop_table_queries = [
    review_drop,
    calendar_drop,
    listings_drop,
    reviewer_drop,
    time_drop     
]