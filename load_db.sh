docker exec pr_sentiment_mongo mongoimport --username=root --password=s3cret --authenticationDatabase=admin --db=pull-requests-raw --collection=tensorflow --file=/tmp/dumps/raw/tensorflow.json
# add more collections here

#docker exec pr_sentiment_mongo mongoimport --username=root --password=s3cret --authenticationDatabase=admin --db=pull-requests --collection=processed --file=/tmp/dumps/processed.json