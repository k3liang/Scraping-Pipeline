# Scraping Pipeline Project

## Setup Instructions

1. **Clone the Repository:**
    ```sh
    git clone https://github.com/k3liang/Scraping-Pipeline
    cd Scraping-Pipeline/
    ```

2. **Create a folder called data with your json files:**
    ```sh
    mkdir data
    mv /path/to/json/s01.json data/
    mv /path/to/json/s02.json data/
    ```

3. **Build Services:** (assuming Docker and Docker Compose is installed on your system)
    ```sh
    docker compose build
    ```

4. **Run Services:** 
    ```sh
    docker compose up
    ```

5. **Query the Database:**
    ```sh
    docker compose run scrapy python ../query.py
    ```

6. **Terminate everything when finished**
    ```sh
    docker compose down
    ```

## Pipeline Process

- **Scrapy Spider:** Reads JSON files, iterating over the `jobs` array, representing each data element of that array as a scrapy Item with multiple Fields, which then will be passed to the three pipelines below for processing.
- **Redis Pipeline:** Items first go here, which checks the cache to see if the item was already processed. If it is indeed a duplicate, then this pipeline prevents the item from continuing down to the other pipelines. Otherwise, if it's a new item, then it caches it and passes it along to the other pipelines.
- **PostgreSQL Pipeline:** Connects to a PostgreSQL database, where the item will be used to fill a row of the table.
- **MongoDB Pipeline:** Connects to a MongoDB database, where the item is stored as a JSON-like document.
