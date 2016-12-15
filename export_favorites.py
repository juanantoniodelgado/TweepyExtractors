import tweepy

"""
This is script will export the favorite tweets of your Twitter account.

You will need to get a consumer key and consumer secret token to use this
script, you can do so by registering a twitter application at https://dev.twitter.com/apps

Part of this code was extracted from:
Dave Jeffery's Github: https://gist.github.com/davej/113241
JohnTroony's Github: https://gist.github.com/JohnTroony/489ccc8e476b9377ae47

@requirements: Python 2.5+, Tweepy (http://pypi.python.org/pypi/tweepy/1.7.1)
@author: Juan Antonio Delgado López
"""

consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""
file_name = 'favorites.txt' # Output file name
last_page_quota = 1 # Change this value if the quota limit was triggered on the last execution

def oauth_login(consumer_key, consumer_secret):
    """Authenticate with twitter using OAuth"""

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth_url = auth.get_authorization_url()

    verify_code = raw_input("Authenticate at %s and then enter you verification code here > " % auth_url)
    auth.get_access_token(verify_code)

    return tweepy.API(auth)


def batch(api):

    end_while = False
    favorite_page = last_page_quota # Incremental variable for pagination
    stored_favorites = [] # Array to store favorites

    while end_while is False:

        try:
            favorites = api.favorites(page = favorite_page) # Fetch the current page

            if len(favorites) > 0:

                for favorite in favorites:

                    # Add the favorite URL to the array
                    stored_favorites.append(
                        'https://twitter.com/' + favorite.author.screen_name + '/status/' + favorite.id_str
                    )

                favorite_page += 1

            else:
                end_while = True

        except tweepy.error.RateLimitError:
            print('Rate limit exceded. Last page fetched: ' + str(favorite_page))
            end_while = True


    # Save the favorites into a file
    stored_file = open(file_name, 'a')

    for storedFavorite in stored_favorites:
        stored_file.write(storedFavorite + '\n')

    stored_file.close()


if __name__ == "__main__":
    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    print "Authenticated as: %s" % api.me().screen_name

    batch(api)