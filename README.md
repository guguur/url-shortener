# URL Shortener Service

A simple URL shortener service built with **FastAPI** and **PostgreSQL**.

## Features

- Shorten long URLs to short, unique slugs
- Expiration for shortened URLs
- Click counting for each shortened URL
- RESTful API endpoints
- Launchable with Docker
- Some Unit Tests
- Configuration via environment variables


## Run the API with Docker
1. **Configure environment variables:**

   The following environment variables are used for the internal database:

   - `DB_PASSWORD`
   - `DB_USER`
   - `DB_NAME`
   - `DB_PORT`
   - `DB_HOST`
   - `DB_STORAGE`: the path where to store the database files (e.g: `/path/to/url-shortener/tmp/db`)
   - `APP_STORAGE`: the path to the project directory (e.g: `/path/to/url-shortener`)
   - `PROJECT_NAME`: used for Docker to regroup containers under the same project
   - `APP_PORT`: the port where the app will be located on `localhost`

   You have to use a `.env` file. You can find a `.env` example in the `.env.example` file.

2. **Build image and run containers**

    Run the following command to run the API:
    ```bash
    make init
    ```
    The API will run on `localhost`
3. **Test the API**
    The API has three endpoints:
    - `[GET] /{slug}`
    - `[GET] /stats/{slug}`
    - `[POST] /shorten`

    3.1 **`[GET] /{slug}`**
    ```
    # curl -X GET -i http://localhost:8000/aY2Pv8
    HTTP/1.1 307 Temporary Redirect
    date: Fri, 05 Sep 2025 17:54:41 GMT
    server: uvicorn
    content-length: 0
    location: https://www.google.com/
    ```

    3.2 **`[GET] /stats/{slug}`**
    ```
    # curl -X GET -i http://localhost:8000/stats/aY2Pv8
    HTTP/1.1 200 OK
    date: Fri, 05 Sep 2025 17:56:16 GMT
    server: uvicorn
    content-length: 1
    content-type: application/json

    2
    ```

    3.3 **`[POST] /shorten`**
    ```
    # curl -X 'POST' \
    'http://0.0.0.0:8000/shorten' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "url": "https://www.twitch.tv/zevent"
    }'
    {"shorten_url":"http://localhost:8000/FGKGfZ"}
    ```