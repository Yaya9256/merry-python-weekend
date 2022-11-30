# merry-python-weekend
This application idea comes from Kiwi (www.kiwi.com) Christmas workshop held in Prague


Purpose of this application is to gather the journey information from the 
Student Agency web page, which is using client side rendering of all their 
bus train and plain journeys. 

The data is scraped from the web page, cached using Redis and saved into the 
PostgreSQL database. Json file with journeys can be returned when GET API 
method is called with your journey specification: 
# Example usage
### Run API call to get journeys
http://127.0.0.1:8000/search?source=Brno?destination=Praha?day=2022-12-03

# General set up & configuration
### PostgreSQL database set up:
1. Run PostgreSQL database
2. Create the new table in new Postgre SQL database <br>`database/create_journeys_table `
3. Connection is handled in `database/get_connection` by context manager, 
4. Table() model is called from `database/table_model` for initial table creation <br> and each API call to update journey data 

### Redis caching
- install redis https://redis.io/docs/getting-started/
### Update config file 
- with your specific set up of database and caching access <br>
`config/conf.yml`

### Run web server 
uvicorn api_test_journeys:app --reload
