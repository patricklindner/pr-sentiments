docker exec pr_sentiment_mongo mongoexport --username=root --password=s3cret --authenticationDatabase=admin --db=pull-requests-raw --collection=tensorflow --out=/tmp/dumps/raw/tensorflow.json
# add more collections here


#docker exec pr_sentiment_mongo mongoexport --username=root --password=s3cret --authenticationDatabase=admin --db=pull-requests-raw --collection=processed --out=/tmp/dumps/processed/tensorflow.json