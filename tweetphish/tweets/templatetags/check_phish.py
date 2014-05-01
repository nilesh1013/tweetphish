from urlparse import urlparse
import requests
import json
import phishtank

from django import template
from django.core.cache import cache

from tweets.models import TweetUrls

register = template.Library()

MYWOT_CATEGORIES = {
    '101': 'Malware or viruses',
    '102': 'Poor customer experience',
    '103': 'Phishing',
    '104': 'Scam',
    '105': 'Potentially illegal',
    '201': 'Misleading claims or unethical',
    '202': 'Privacy risks',
    '203': 'Suspicious',
    '204': 'Hate, discrimination',
    '205': 'Spam',
    '206': 'Potentially unwanted programs',
    '207': 'Ads / pop-ups'
}

MYWOT_API_KEY = 'ba90e1b5fe8ec144048e63c38b2ea18f4fc93776'
MYWOT_API_URL = 'http://api.mywot.com/0.4/public_link_json2?hosts=%s/&key=%s'
GOOGLE_SAFE_BROWSING_KEY = 'ABQIAAAA_BMMl3XOHEx1HS2JGl_VDxQ_VGe9tIQpsNOPN3slh1YtY4Qlvw'
GOOGLE_SAFE_BROWSING_URL = 'https://sb-ssl.google.com/safebrowsing/api/lookup?client=api&apikey=%s&appver=1.0&pver=3.0&url=%s'

@register.filter(name="check_phish")
def check_phish(original_url):
    """
    checking url is phishing or not
    """
    phish_url = cache.get(original_url)

    if phish_url is None:
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

            cache.set(original_url, phish_url, 86400)
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