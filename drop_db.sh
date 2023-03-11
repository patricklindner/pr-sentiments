#!/bin/bash

filename=resources/project-list.txt
username=root
password=s3cert

# Check if the file exists and is readable
if [ ! -r "$filename" ]; then
	echo "Error: $filename does not exist or is not readable"
	exit 1
fi

echo "Dropping collections in mongoDB container..."

while read -r line; do
	# Extract the repo from the line using the '/' delimiter
	repo=$(echo "$line" | cut -d "/" -f2)
    
	# Dump the collection into a json file
	echo -e "\tDropping collection $repo..."
    jscommand=$(echo "db.$repo.drop()")
    docker exec pr_sentiment_mongo mongo pull-requests-raw -u $username -p $password --authenticationDatabase admin --eval $jscommand

done < "$filename"

echo "done."
