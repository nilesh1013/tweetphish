from django.conf import settings
#from django.core.cache import cache
#from django.template import RequestContext

from twython import Twython, TwythonError
from tweetphish.utils.twitter_parser import Parser
from tweets.models import TweetUrls

def run():
    """
        Gets latest tweet from the Twitter user specified in settings.
        Caches latest tweet for 10 minutes to reduce API calls
    """
    file_words = open('/Users/nileshsharma/webapps/django-tweets/tweetphish/tweets/big_corpora.txt')
    with file_words as f:
        words = f.read().split(',')
    try:
        words.remove('\n')
    except:
        pass
    words = [x.rstrip('\n') for x in words]
    words = list(set(words))
    words = [word for word in words if len(word)>3]
    parser = Parser()
    search_results = []

    twitter = Twython(settings.TWITTER_CONSUMER_KEY,
                      settings.TWITTER_CONSUMER_SECRET,
                      settings.TWITTER_OAUTH_TOKEN,
                      settings.TWITTER_OAUTH_TOKEN_SECRET)
    for query_param in words:
        print query_param
        try:
            search_tweets = twitter.search(q=query_param, lang="en", count="100")
        except TwythonError as e:
            return {"exception happened :)": e}
        else:
            for tweet in search_tweets['statuses']:
                try:
                    search_results.append(parser.parse(tweet['text']))
                except:
                    pass

        for result in search_results:
            for url in result.urls:
                try:
                    TweetUrls.objects.get(url=url)
                except TweetUrls.DoesNotExist:
                    tweet_users = ("|").join(result.users)
                    tweet_tags = ("|").join(result.tags)
                    TweetUrls.objects.create(
                        url=url,users=tweet_users,
                        tags=tweet_tags, query_keyword=query_param,
                        user_keyword=None )
                else:
                    pass
                check_phish(url)


def check_phish(original_url):
    """
    checking url is phishing or not
    """
    #trying to get phish_url from database, if that value if already there
    try:
        url_model_data = TweetUrls.objects.get(url=original_url)
    except TweetUrls.DoesNotExist:
        pass
    else:
        phish_url = url_model_data.phish_url

    if phish_url is None:
        url = original_url
        phish_url = None

        if long_url(original_url):
            url = long_url(original_url)

        phish_url = check_phish_url(url)

        if not phish_url:
            phish_url = check_mywot_url(url)

        if not phish_url:
            phish_url = check_google_safe_browsing(url)

        if not phish_url:
            phish_url = False

        phish_url_field_value = True if phish_url else False
        which_phish_field_value = phish_url if phish_url else ''

        data_update = {
            'which_phish': which_phish_field_value,
            'phish_url': phish_url_field_value,
            'full_url': url
        }

        try:
            user_models = TweetUrls.objects.get(url=original_url)
        except TweetUrls.DoesNotExist:
            user_models = TweetUrls.objects.create(url=original_url)

        if user_models:
            user_models.__dict__.update(data_update)
            user_models.save()

    return phish_url


def long_url(original_url):
    url = None

    try:
        long_url_json = requests.get('http://api.longurl.org/v2/expand?url=%s&format=json' % original_url)
        json_data = json.loads(long_url_json.content)
        url = json_data['long-url']
    except:
        pass

    return url


def check_phish_url(url):
    phish_url = None

    try:
        phishtank_api = phishtank.Phishtank()
        phish_url = phishtank_api.check(url).unsafe
    except:
        pass

    if phish_url:
        phish_url = 'Phishtank detection'

    return phish_url


def check_mywot_url(url):
    phish_url = None

    try:
        mywot_result = requests.get(MYWOT_API_URL % (url, MYWOT_API_KEY))
        json_data = json.loads(mywot_result.content)
    except:
        pass
    else:
        try:
            url_netloc = urlparse(url).netloc
            url_data = json_data[url_netloc]
        except:
            pass
        else:
            if "blacklists" in url_data:
                phish_url="MyWot detection"
            else:
                try:
                    url_code_category = url_data['categories'].keys()
                except (KeyError, AttributeError):
                    pass
                else:
                    for category_code in url_code_category:
                        if category_code in MYWOT_CATEGORIES:
                            phish_url = "MyWot detection"
                            break

    return phish_url


def check_google_safe_browsing(url):
    phish_url = None

    try:
        google_safe_result = requests.get(GOOGLE_SAFE_BROWSING_URL % (GOOGLE_SAFE_BROWSING_KEY, url)).text
    except:
        google_safe_result = None

    if google_safe_result in ('malware', 'phishing'):
        phish_url = 'googlesafebrowsing detection'

    return phish_url

if __name__ == "__main__":
    run()