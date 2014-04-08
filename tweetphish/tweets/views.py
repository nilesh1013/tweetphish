from django.shortcuts import render
from django.conf import settings
from django.core.cache import cache

from twython import Twython, TwythonError
from tweetphish.utils.twitter_parser import Parser

def search(request):
    """
        Gets latest tweet from the Twitter user specified in settings.
        Caches latest tweet for 10 minutes to reduce API calls
    """
    #import ipdb;ipdb.set_trace()
    query_param = request.GET.get('query')
    user_name = request.GET.get('user')
    parser = Parser()
    search_results = []

    twitter = Twython(settings.TWITTER_CONSUMER_KEY,
                      settings.TWITTER_CONSUMER_SECRET,
                      settings.TWITTER_OAUTH_TOKEN,
                      settings.TWITTER_OAUTH_TOKEN_SECRET)
    if query_param:
        try:
            search_tweets = twitter.search(q=query_param, lang="en", count="50")
        except TwythonError as e:
            return {"exception happened :)": e}
        else:
            for tweet in search_tweets['statuses']:
                search_results.append(parser.parse(tweet['text']))
    elif user_name:
        try:
            search_tweets = twitter.get_user_timeline(screen_name=user_name , count="50")
        except TwythonError as e:
            return {"exception happened :)": e}
        else:
            #import ipdb;ipdb.set_trace()
            print len(search_tweets)
            for tweet in search_tweets:
                try:
                    search_results.append(parser.parse(tweet['text']))
                except:
                    pass


    #for tweet in search_tweets['statuses']:
    #   search_results.append(parser.parse(tweet['text']))
    ##latest_tweet = user_timeline[0]
    #latest_tweet['text'] = parser.parse(latest_tweet['text']).html
    #cache.set('latest_tweet', latest_tweet, settings.TWITTER_TIMEOUT)
    template_dict = {'search_results': search_results}
    #import ipdb;ipdb.set_trace()
    #print 'search_results', search_results
    return render(request, "search.html", template_dict)


# Create your views here.
def index(request):
    return render(request, "index.html")
