import tweepy
import parameters

last_page_quota = 1 # Change this value if the quota limit was triggered on the last execution

def oauth_login(consumer_key, consumer_secret):
    """Authenticate with twitter using OAuth"""

    auth = tweepy.OAuthHandler(parameters.consumer_key, parameters.consumer_secret)
    auth_url = auth.get_authorization_url()

    verify_code = raw_input("Authenticate at %s and then enter you verification code here > " % auth_url)
    auth.get_access_token(verify_code)

    return tweepy.API(auth)


def batch(api):

    end_while = False

    while end_while is False:

        try:
            favorites = api.favorites(page = 1)

            if len(favorites) > 0:

                for favorite in favorites:

                    api.destroy_favorite(favorite.id_str)

            else:
                end_while = True

        except tweepy.error.RateLimitError:
            print('Rate limit exceded.')
            end_while = True

if __name__ == "__main__":
    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(parameters.consumer_key, parameters.consumer_secret)
    auth.set_access_token(parameters.access_key, parameters.access_secret)
    api = tweepy.API(auth)
    print "Authenticated as: %s" % api.me().screen_name

    batch(api)