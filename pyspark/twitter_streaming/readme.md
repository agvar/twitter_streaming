The project uses the twitter streaming api to pull tweeets related to topics of interest. The tweets are pushed into an AWS kineses data stream. A pyspark job analyses tweets and stores into an S3 location