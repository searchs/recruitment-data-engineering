# Data Analytics Recruitment Showcase

## Purpose
This repository serves as a sample data stack for candidates to demonstrate their understanding of databases, data processing, and problem-solving.

There are several stages to this review:
1. Preparing and analysing the environment at home before the technical interview.
2. Presenting an overview of the given selected objective.

The objective review aims to give an insight into your approaches to the defined competencies required for this role.

## Prerequisites
- Understanding of relational databases, including how to create tables, insert data, and query data. For the purpose of this test, we are using PostgreSQL.
- Proficiency in the Python programming language, including how to read and write files, process data, and access a PostgreSQL database.
- Familiarity with Docker for container management, utilised through Docker Compose tool. Docker and Docker Compose need to be installed on your development machine. While knowledge of Docker is not a requirement for this role, an understanding of DevOps is crucial.
- Familiarity with Git for source control, and a github.com account which will be used for sharing your code.

We have included example data and program code. The example schema creates simple tables, with Python example code to load data from a CSV file and insert it into a database table. Instructions on how to use the Docker containers, start the database, and use the examples are located towards the end of this document.

## Background
We have provided a GitHub repository containing:

- A `docker-compose.yml` file that configures a container for the PostgreSQL database, a Jupyter notebook service to run Python code, and MinIO as an object store for the downloaded raw files.
- An `init.sql` file that creates the tables in the database and populates some data prior to the objectives.
- A Python script called `load-data.py` that pulls some web data to assist with the initial data load.
- `requirements.txt` that lists the Python packages required for the load data code during setup.
- A notebook folder containing `update-circuits.ipynb`, a Jupyter notebook that retrieves a file called `circuits.csv` from the object store and looks for new `circuits` not currently listed in the PostgreSQL table `circuits`.

## Problem
We would like you to complete a sequence of steps. We anticipate this will take no more than a couple of hours of your time.
1. Fork the git repo to your own GitHub account.
2. Analyse the existing `update-circuits.ipynb` notebook. It has some issues with the data it is inserting into the database. Can you describe what the problem is and suggest some approaches to prevent the issue?
3. Create a Jupyter notebook Python script to insert the results from 2021 onwards within the `results.csv` into the `results` table.
4. Share a link to your cloned git repo with us so we can review your approach during the technical interview.

Instructions on how to run the services and connect are given below.

## Notes on Completing These Tasks
- There is no 'right' way to do this. We are interested in the choices you make, how you justify them, and your development process.
- Consider what kind of error handling and testing is appropriate.
- All data input, storage, and output should be in UTF-8. Expect multi-byte characters in the data.

## Technical Review at Your Interview
During your interview, we will spend 45 minutes reviewing this problem with you. This will include:
- Examining any code developed and the solution.
- Discussing your thought process on approaching a solution to the problem.
- Considering future development prospects.

## Setup Notes:
### Requirements
Ensure you have recent versions of Docker and Docker Compose installed.

### Building the Images
This will build all the images referenced in the Docker Compose file. You will need to re-run this command after making any code changes (you can also specify individual services to build if more convenient).
```
docker-compose build
```

### Starting the Services
To run the services. It may take a short while to run the start-up scripts.

```
docker-compose up
```


### Cleaning Up
To tidy up, bring down the containers and delete them.
```
docker-compose down
```