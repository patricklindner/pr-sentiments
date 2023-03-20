# Sentiments of Pull-Requests

## Loading and dumping the database

The data is stored in a mongo db. It is persisted in json files in the folder mongodump. In order to load the data from
the dump files, execute the `load_data.sh` script. In order to dump the stored collections to the dump files, execute
the
`dump_db.sh` bash script.

## Authentication

In order to access the GitHub API with more speed and fewer timeouts, the user should be authenticated. Therefor, create
the file `token.txt` in the folder resources and paste your personal GitHub access token into the file. This file will
be ignored by git and thus not pushed to the repository.

### project-list.txt

This file contains all projects which should be analyzed. Every line contains a single project in the format
`<owner_name>/<project_name>`


# Logserver

Before running the pulling script, run the log server by invoking `flask --app log-server run` from the `src` directory. 
You can monitor the progress on `http://localhost:5000/progress`

