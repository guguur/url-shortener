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

   - `INTERNAL_DB_PASSWORD`
   - `INTERNAL_DB_USER`
   - `INTERNAL_DB`
   - `INTERNAL_DB_PORT`
   - `INTERNAL_DB_HOST`
   - `DB_STORAGE`: the path where to store the database files
   - `APP_STORAGE`: the path to the project directory (e.g: /path/to/url-shortener)
   - `PROJECT_NAME`: used for Docker to regroup containers under the same project

   You have to use a `.env` file.

2. **Build image and run containers**

    Run the following command to run the API:
    ```bash
    make init
    ```
    The API will run on `localhost:8000`
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
    # curl -X 'POST' 'http://localhost:8000/shorten?url=https%3A%2F%2Fwww.twitch.tv%2Fzevent'                                          
    {"shorten_url":"http://localhost:8000/jxz4Xv"}
    ```