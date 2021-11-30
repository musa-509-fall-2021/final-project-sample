# Philadelphia Commercial Corridors

## Data preparation

All data necessary to generate the reports gets loaded as part of the data pipeline, **except for the SafeGraph data**. To prepare the SafeGraph data:
1. Download the SafeGraph Patterns data from https://shop.safegraph.com/?countries=US&states=PA&cities=Philadelphia&poi=ALL&tab=datasets. You should end up with a zip file that has a bunch of other zip files inside of it named something like `PA-CORE_POI-PATTERNS-YYYY_MM.zip`.
2. Upload that file to a `safegraph_patterns/` folder inside of your data bucket on Google Cloud Storage.

## Local setup

1.  **Build the docker image** -- Navigate to the _airflow/_ folder and run:
    ```bash
    docker build . -f Dockerfile --tag final-project-airflow:0.0.1
    ```
2.  **Set up your environment** -- In the _docker-compose.yml_ file, under `x-airflow-common` **->** `volumes`, change the value for `/opt/google-app-creds.json` to the path to an appropriate service account key.

3. **Run Airflow** -- From the _airflow/_ folder, first run `docker-compose up airflow_init`, then run `docker-compose up`.
