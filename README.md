# Sentiments of Pull-Requests

## Loading and dumping the database

The data is stored in a mongo db. It is persisted in json files in the folder mongodump. In order to load the data from
the dump files, execute the `load_data.sh` script. In order to dump the stored collections to the dump files, execute the
`dump_db.sh` bash script.

### project-list.txt

This file contains all projects which should be analyzed. Every line contains a single project in the format
`<owner_name>/<project_name>`