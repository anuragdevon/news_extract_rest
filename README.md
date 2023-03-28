# Web Scraper API

This is a Python-based web scraper designed to extract and store information about articles from website. The application uses Flask and PostgreSQL to store the scraped data.

## Features

- Parse Url and Store
- Retrieve Details
- 

## Requirements

- Flask
- Flask-CORS
- psycopg2
- python-dotenv
- requests
- beautifulsoup4

## Installation

1. Clone the repository to your local machine:

```
git clone https://github.com/anuragdevon/news_extract_rest
```


2. Navigate to the project directory:


```
cd news_extract_rest
```

3. Add your database variables to a .env file in the root directory of the project

```
database=<database-name>
user=<database-user>
password=<database-password>
host=<database-host>
port=<database-port>
```

3. Run the server using `python scape.py`


The application should now be accessible at http://localhost:5000.

## API Documentation

The API documentation is available at https://documenter.getpostman.com/view/16992854/2s93RRvDFF


## Usage
news_extract_rest provides a RESTful API that can be tested with scripts or Postman.

### Parse URL
`POST /parse_url`
This endpoint takes a JSON object containing a URL as input, extracts data from the article at the given URL, and stores it in both a CSV file and a PostgreSQL database. If the article already exists in the database, it updates the existing entry. The response contains information about the parsed data and any errors that occurred.

Example request body:
```
{
    "url": "https://www.theverge.com/2023/3/28/22342131/tesla-rental-car-program-new-jersey-law"
}

```

Example response body:
```
{
    "message": "Data parsed and stored successfully!",
    "error": "",
    "output": {
        "title": "Tesla will launch a rental car program to comply with new New Jersey law",
        "url": "https://www.theverge.com/2023/3/28/22342131/tesla-rental-car-program-new-jersey-law",
        "author": "Sean O'Kane",
        "published_date": "2023-03-28T10:00:00-04:00"
    }
}
```


### GET Details
`GET /get_articles/<int:id>`
This endpoint retrieves a previously parsed article from the PostgreSQL database based on the ID provided in the URL parameter. If the article is found, the response contains information about the article. If the article is not found, the response contains an error message.

Example request:
```
{
GET /get_articles/1 HTTP/1.1
Host: localhost:5000


```

Example response body:
```
{
    "id": 1,
    "url": "https://www.theverge.com/2023/3/28/22342131/tesla-rental-car-program-new-jersey-law",
    "title": "Tesla will launch a rental car program to comply with new New Jersey law",
    "author": "Sean O'Kane",
    "published_date": "2023-03-28T10:00:00-04:00"
}

```
