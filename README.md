# Museum DB example app

This app is an example that shows usage of Docker in combination with Python and some visualization libraries.

## Pre-requisites

You need to have Docker service running in your environment. 
If running a desktop system you can download Docker Desktop:
https://www.docker.com/products/docker-desktop

You will also need Docker compose which has different ways of installation depending on your system and preferences:
https://docs.docker.com/compose/install/

Before proceeding to build step, make sure that Docker service is running.

## Build

Once you clone the repository you need to build the Docker images (make sure to cd into the cloned repo):
```
docker-compose build
```
Some images are larger so it can take few minutes for them to download and build.

## Run

Once the images are built, you can proceed by bringing up the containers:
```
docker-compose up
```

In the on-screen log you can see the components starting, including **backend**, **db** and **notebook**.
Make sure to copy the Jupyter notebook link and open it in browser.

Once the data are completely pulled and DB is created you should see something like:
```
backend_1   | Prepared data:
backend_1   |                                                Museum  ... Art/culture museum
backend_1   | 0                                              Louvre  ...               True
backend_1   | [69 rows x 16 columns]
museumdb_backend_1 exited with code 0
```

Open the notebook and try the provided examples.

Once you are done, you can put the containers down by running:
```
docker-compose down
```

## Sources
- Base table used for creating example DB - https://en.wikipedia.org/wiki/List_of_most-visited_museums
- Blogpost used for most of the code structure - https://www.docker.com/blog/tag/python-env-series/
- WikiData was used as a data source for building the example DB - https://www.wikidata.org/wiki/Wikidata:Main_Page
