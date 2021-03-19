
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
/usr/bin/spark-submit --jars /home/ec2-user/my_apps/venv/jars/spark-streaming-kinesis-asl_2.11-2.4.7.jar,/home/ec2-user/my_apps/venv/jars/aws-java-sdk-1.11.939.jar,/home/ec2-user/my_apps/venv/jars/amazon-kinesis-client-1.14.0.jar,/home/ec2-user/my_apps/venv/jars/jackson-dataformat-cbor-2.12.1.jar \
pyspark_read_kineses.py \
twitter_streaming_app tweet_stream https://kinesis.us-east-2.amazonaws.com us-east-2

"""
import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kinesis import KinesisUtils, InitialPositionInStream

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(
            "Usage: kinesis_wordcount_asl.py <app-name> <stream-name> <endpoint-url> <region-name>",
            file=sys.stderr)
        sys.exit(-1)

    sc = SparkContext(appName="PythonStreamingKinesisWordCountAsl")
    ssc = StreamingContext(sc, 1)
    appName, streamName, endpointUrl, regionName = sys.argv[1:]
    lines = KinesisUtils.createStream(ssc, appName, streamName, endpointUrl, regionName, InitialPositionInStream.LATEST, 2)
    counts = lines.flatMap(lambda line: line.split(" ")) \
        .map(lambda word: (word, 1)) \
        .reduceByKey(lambda a, b: a+b)
    counts.pprint()

    ssc.start()
    ssc.awaitTermination()

