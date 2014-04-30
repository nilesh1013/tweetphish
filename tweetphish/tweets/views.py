from django.shortcuts import render, render_to_response
from django.conf import settings
from django.core.cache import cache
from django.template import RequestContext

from twython import Twython, TwythonError
from tweetphish.utils.twitter_parser import Parser
from tweets.models import TweetUrls
from endless_pagination.decorators import page_template

@page_template('entry_index_page.html')
def search(request, template = "search.html", extra_context=None):
    """
        Gets latest tweet from the Twitter user specified in settings.
        Caches latest tweet for 10 minutes to reduce API calls
    """
    query_param = request.GET.get('query')
    user_name = request.GET.get('user')
    cache_name = None
    page_template= "entry_index_page.html"

    if query_param:
        cache_name = "search_results_%s" % query_param
    elif user_name:
        cache_name = "search_results_%s" % user_name

    search_results = cache.get(cache_name)
    if not search_results:
        parser = Parser()
        search_results = []

        twitter = Twython(settings.TWITTER_CONSUMER_KEY,
                          settings.TWITTER_CONSUMER_SECRET,
                          settings.TWITTER_OAUTH_TOKEN,
                          settings.TWITTER_OAUTH_TOKEN_SECRET)
        if query_param:
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
        elif user_name:
            try:
                search_tweets = twitter.get_user_timeline(screen_name=user_name , count="100", exclude_replies=True)
            except TwythonError as e:
                return {"exception happened :)": e}
            else:
                for tweet in search_tweets:
                    try:
                        search_results.append(parser.parse(tweet['text']))
                    except:
                        pass
        cache.set(cache_name, search_results, settings.TWITTER_TIMEOUT)

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
                    user_keyword=user_name )
            else:
                pass

    if request.is_ajax():
        template = page_template
    template_dict = {"search_results": search_results, "page_template": page_template}
    if extra_context:
        template_dict.update({'extra_context': extra_context})

    return render_to_response(template, template_dict, context_instance=RequestContext(request))


# Create your views here.
def index(request):
    return render(request, "index.html")
