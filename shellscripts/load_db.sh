#!/bin/bash

filename=resources/project-list.txt
username=admin
password=password

# Check if the file exists and is readable
if [ ! -r "$filename" ]; then
	echo "Error: $filename does not exist or is not readable"
	exit 1
fi

echo "Loading collections in mongoDB container..."

while read -r line; do
	# Extract the repo from the line using the '/' delimiter
	repo=$(echo "$line" | cut -d "/" -f2)

	# Dump the collection into a json file
	echo -e "\tLoading collection $repo..."
    jscommand=$(echo "db.$repo.drop()")
    docker exec pr_sentiment_mongo mongoimport --username="$username" --password="$password" --authenticationDatabase=admin --db=pull-requests-raw --collection="$repo" --file="/tmp/dumps/raw/$repo.json"
    docker exec pr_sentiment_mongo mongoimport --username="$username" --password="$password" --authenticationDatabase=admin --db=pull-requests-clear --collection="$repo" --file="/tmp/dumps/enriched/$repo.json"

done < "$filename"

echo "done."