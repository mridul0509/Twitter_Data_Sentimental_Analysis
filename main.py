# tweepy is used to access twitter api
# csv is comma separated values
# re is regex
# plt is used for graphs charts matlab etc(plot)
import tweepy
import csv
import re
from textblob import TextBlob
import matplotlib.pyplot as plt


class SentimentAnalysis:

    # build in function acts like a constructor
    def __init__(self):
        self.tweets = []
        self.tweetText = []
        self.i = 0

    def download_data(self):
        # authenticating twitter developer account using consumer key,Access keys and tokens
        # use your token keys
        # API keys are your consumer key
        
        consumer_key = 'xxxxxx'
        consumer_secret = 'xxxxxx'
        access_token = 'xxxxxxxxxxxx'
        access_token_secret = 'xxxxxxxxxx'
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        count = 0

        # input for term to be searched and how many tweets to search. We have assigned 20 to number of tweets
        search_term = input("Enter Keyword you want to search about: ")
        no_of_terms = 20

        # searching for tweets
        self.tweets = tweepy.Cursor(api.search_tweets, q=search_term, lang="en").items(no_of_terms)

        # Open/create a file to write data to
        csv_file = open('tweets.csv', 'w')

        # Use csv writer
        csv_writer = csv.writer(csv_file)

        # creating some variables to store info
        polarity = 0
        positive = 0
        semi_positive = 0
        negative = 0
        semi_negative = 0
        neutral = 0

        # iterating through tweets fetched
        for tweet in self.tweets:

            # Append to tweetText[] so we can store in csv later.Use encode UTF-8
            self.tweetText.append(self.clean_tweet(tweet.text).encode('utf-8'))
            analysis = TextBlob(tweet.text)
            polarity += analysis.sentiment.polarity  # adding up polarities to find the average later
            count = count + 1
            if analysis.sentiment.polarity == 0:  # adding reaction of how people are reacting to find average later
                neutral += 1
                self.tweetText.append('---> neutral')
            elif 0 < analysis.sentiment.polarity <= 0.5:
                semi_positive += 1
                self.tweetText.append('---> semi_positive')
            elif 0.5 < analysis.sentiment.polarity <= 1:
                positive += 1
                self.tweetText.append('---> positive')
            elif -0.5 < analysis.sentiment.polarity <= 0:
                semi_negative += 1
                self.tweetText.append('---> semi_negative')
            elif -1 < analysis.sentiment.polarity <= -0.5:
                negative += 1
                self.tweetText.append('---> negative')

        # Exit from the program if no tweet is found
        if count == 0:
            print("There is no tweets about the given keyword.")
            exit()
        # Writing to csv and closing csv file
        # print(self.tweetText)
        csv_writer.writerow(self.tweetText)
        csv_file.close()

        f = open('tweets.csv')
        csv_f = csv.reader(f)
        # to print the data extracted in tweets.csv file
        for row in csv_f:
            for element in row:
                print(element)

        # finding average of how people are reacting
        positive = self.percentage(positive, count)
        semi_positive = self.percentage(semi_positive, count)
        negative = self.percentage(negative, count)
        semi_negative = self.percentage(semi_negative, count)
        neutral = self.percentage(neutral, count)

        # finding average reaction
        polarity = polarity / count

        if polarity == 0:
            sentiment = "Neutral"
        elif 0 < polarity <= 0.5:
            sentiment = "Positive"
        elif 0.5 < polarity <= 1:
            sentiment = "Strongly Positive"
        elif -0.5 < polarity <= 0.0:
            sentiment = "Negative"
        elif -1 < polarity <= -0.5:
            sentiment = "Strongly Negative"

            # printing out obtained data
        print("General reaction of people on " + search_term + " by analyzing " + str(count) + " tweets is " + sentiment)

        self.plot_pie_chart(positive, semi_positive, negative, semi_negative, neutral, search_term, count)

    def clean_tweet(self, tweet):
        # To remove Special Characters,Username from tweet
        # The first parameter pattern is searched in the third parameter string and is replaced by the second parameter
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    # function to calculate percentage

    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return temp

    def plot_pie_chart(self, positive, semi_positive, negative, semi_negative, neutral, search_term, no_of_search_terms):
        labels = ['Strongly Positive [' + str(positive) + '%]', 'Positive [' + str(semi_positive) + '%]',
                  'Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(semi_negative) + '%]', 'Strongly Negative [' + str(negative) + '%]']
        sizes = [semi_positive, positive, neutral, semi_negative, negative]
        colors = ['gold', 'yellow', 'green', 'red', 'black']
        patches, texts = plt.pie(sizes, colors=colors, startangle=0)
        plt.legend(patches, labels, loc="best")
        plt.title("People's reaction on " + search_term + ' by analyzing twitter data' + str(no_of_search_terms) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    sa = SentimentAnalysis()
    sa.download_data()
