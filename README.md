# Sentiments of Pull-Requests
This repo is for a project for the course Software Analytics.
The goal of the project is to analysis 10 (large) GitHub repositiories' pull requsets to find out if sentiment of poll requests effect the time to merge of these PRs.
This repo contains the code and data used in the project.
The code is sturctured according to a pipeline pattern with 6 steps.
```
fetch PRs -> clean data -> enrich data -> sentiment analysis -> clean data
-> statistical analysis
```
At each step the data can be found in `./mongodump/`.
To load and dump this data use the following `sh` scripts.

```
./shellscripts/load_data.sh
./shellscripts/dump_db.sh
```

## Running Code
### Authentication
In order to access the GitHub API with more speed and fewer timeouts, the user should be authenticated.
Therefor, create the file `token.txt` in the folder resources and paste your personal GitHub access token into the file.
This file will be ignored by git and thus not pushed to the repository.

### Requirements
Next the python requirements should be installed
```
pip install -r requirements.txt
```
We use mongoDB to keep the data to run mongoDB simply use `docker-compose up`

### Python Scripts
To fetch PRs:
```
python3 -m src.pull_and_persist
```
To clean data:
```
python3 -m src.clean.main
```
To enrich data:
```
python3 -m src.enrichment.main
```
To perform sentiments analysis
```
python3 -m src.sentiment.main
```
To perform statstics analysis
```
python3 -m src.statistics.main
```

### project-list.txt

This file contains all projects which should be analyzed. Every line contains a single project in the format
`<owner_name>/<project_name>`


### Logserver
Before running the pulling script, run the log server by invoking `flask --app log-server run` from the `src` directory. 
You can monitor the progress on `http://localhost:5000/progress`

