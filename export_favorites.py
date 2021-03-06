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
    stored_file = open(parameters.favourites_file_name, 'a')

    for storedFavorite in stored_favorites:
        stored_file.write(storedFavorite + '\n')

    stored_file.close()


if __name__ == "__main__":
    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(parameters.consumer_key, parameters.consumer_secret)
    auth.set_access_token(parameters.access_key, parameters.access_secret)
    api = tweepy.API(auth)
    print "Authenticated as: %s" % api.me().screen_name

    batch(api)