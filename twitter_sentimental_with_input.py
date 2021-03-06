import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob


class TwitterClient( object ):
    '''
    Generic Twitter Class for sentiment analysis.
    '''

    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = 'put yours'
        consumer_secret = 'put yours'
        access_token = 'put yours'
        access_token_secret = 'put yours'

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler( consumer_key, consumer_secret )
            # set access token and secret
            self.auth.set_access_token( access_token, access_token_secret )
            # create tweepy API object to fetch tweets
            self.api = tweepy.API( self.auth )
        except:
            print( "Error: Authentication Failed" )

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join( re.sub( "(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w+:\ / \ / \S+) ", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob( self.clean_tweet( tweet ) )
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=10):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []

        try:


            # call twitter api to fetch tweets
            fetched_tweets = self.api.search( q=query, count=count )

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment( tweet.text )

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append( parsed_tweet )
                else:
                    tweets.append( parsed_tweet )

            # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print( "Error : " + str( e ) )


def main():
    # creating object of TwitterClient Class
    api = TwitterClient()

    # added by me
    # Choice = None
    #
    # while Choice != 0:
    #     #define questions of my query
    #     queryqu = []
    #     # define properties of my query
    #     properties = [
    #         ("query", str),
    #         ("count", int),
    #     ]
    #     for prop, p_type in properties:
    #         correct_input = False
    #
    #         while not correct_input:
    #             try:  # try exception
    #                 #queryqu[prop] = p_type( input( "Please enter your %s: " % prop ) )
    #                  query1 = input( "What you want to query about?: " )
    #                 # print (query1)
    #                  count1 = input( "How many tweets you want to compare?: " )
    #                 # print( count1 )
    #             except ValueError:  # if error happened this will be raised
    #                 print( 'Please enter valid value for %s  field.it should be:%s type' % (prop, p_type) )
    #             else:  # if no error happened display this
    #                 correct_input = True

    # if len( query1 ) == 0:
    #     print( '\033[31m' + '\033[01m' + 'Invalid query: %d' % query1 )
    #     #continue
    #
    # if len( count1 ) == 0:
    #     print( "Invalid number of tweets" )
    #     #continue
    #
    # if query1 == 0:
    #     print( "Thank you for using my system" )
    #     #continue

    # added by me

    query1 = input( "What you want to query about?: " )
    # print (query1)
    count1 = input( "How many tweets you want to compare?: " )
    # print( count1 )

    # calling function to get tweets
    tweets = api.get_tweets( query=query1, count=count1 )

    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
    print( "Positive tweets percentage: {} %".format( 100 * len( ptweets ) / len( tweets ) ) )
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # percentage of negative tweets
    print( "Negative tweets percentage: {} %".format( 100 * len( ntweets ) / len( tweets ) ) )
    # percentage of neutral tweets
    #print("Neutral tweets percentage: {} % ".format( 100 * len( tweets - ntweets - ptweets ) / len( tweets)))

    # percentage of neutral tweets
    #print("Neutral tweets percentage: {} % ".format( 100 * len(ntweets) / len( tweets)))

    # printing first 5 positive tweets
    if len(query1) != 0:

        print( "\n\nPositive tweets:" )
        for tweet in ptweets[:10]:
            print( tweet['text'] )

        # printing first 5 negative tweets
        print( "\n\nNegative tweets:" )
        for tweet in ntweets[:10]:
            print( tweet['text'] )


if __name__ == "__main__":
    # calling main function
    main()