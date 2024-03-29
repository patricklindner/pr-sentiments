#!/bin/bash

filename=resources/project-list.txt
username=admin
password=password

# Check if the file exists and is readable
if [ ! -r "$filename" ]; then
	echo "Error: $filename does not exist or is not readable"
	exit 1
fi

echo "Dumping data from MongoDB to json files..."

while read -r line; do
	# Extract the repo from the line using the '/' delimiter
	repo=$(echo "$line" | cut -d "/" -f2)
    
	# Dump the collection into a json file
	echo -e "\tDumping $repo..."
	docker exec pr_sentiment_mongo mongoexport --username="$username" --password="$password" --authenticationDatabase=admin --db=pull-requests-raw --collection="$repo" --out="/tmp/dumps/raw/$repo.json"
	docker exec pr_sentiment_mongo mongoexport --username="$username" --password="$password" --authenticationDatabase=admin --db=pull-requests-clean --collection="$repo" --out="/tmp/dumps/enriched/$repo.json"
	docker exec pr_sentiment_mongo mongoexport --username="$username" --password="$password" --authenticationDatabase=admin --db=pull-requests-sentiment --collection="$repo" --out="/tmp/dumps/sentiment/$repo.json"

done < "$filename"

echo "done."
