import tweepy
import requests
import datetime
import boto3
import json
from twitter_credentials  import API_key,API_secret_key,Access_token,Acess_token_secret

#Streaming class override
class TwitterStreamListener(tweepy.StreamListener):
    def on_status(self,status):
       if status.retweeted:
           return
       try:
           print(f"status is:{status.id},user name:{status.user.screen_name}")
           kinesis_client.put_record(StreamName='tweet_stream',Data=status.text,PartitionKey='partition_key')
       except Exception as e:
           print(f"Failed writing to stream:{e}")

    def on_error(self,status_code):
       print(f"Error status code is{status_code}")
       if status_code==420:
            return False

#main function
#main function		
if __name__=='__main__':
    # Authentication and creation of an api object
    auth = tweepy.OAuthHandler(API_key, API_secret_key)
    auth.set_access_token(Access_token, Acess_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
        print("Twitter Authentication OK")
    except Exception as e:
        print(f"Error during authentication{e}")

    #creating kinesis client
    kinesis_client=boto3.client('kinesis',region_name='us-east-2')

    #creating a stream to the twitter api
    twitterstreamlistener=TwitterStreamListener()
    twitter_stream=tweepy.Stream(auth=api.auth,listener=twitterstreamlistener)
    twitter_stream.filter(track=['covid'],languages=["en"])



