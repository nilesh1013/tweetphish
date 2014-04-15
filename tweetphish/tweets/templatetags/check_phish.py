from django import template
from urlparse import urlparse
import requests
import json
import phishtank

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
def check_phish(url):
    """
    checking url is phishing or not
    """
    long_url_json = requests.get('http://api.longurl.org/v2/expand?url=%s&format=json' % url)

    try:
        json_data = json.loads(long_url_json.content)
        url = json_data['long-url']
    except:
        pass

    phish_url = None

    try:
        phishtank_api = phishtank.Phishtank()
        phish_url = phishtank_api.check(url).unsafe
    except:
        pass

    if phish_url:
        phish_url = 'Phishtank detection'
    else:
        mywot_result = requests.get(MYWOT_API_URL % (url, MYWOT_API_KEY))

        try:
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

    if not phish_url:
        try:
            google_safe_result = requests.get(GOOGLE_SAFE_BROWSING_URL % (GOOGLE_SAFE_BROWSING_KEY, url)).text
        except:
            google_safe_result = None

        if google_safe_result in ('malware', 'phishing'):
            phish_url = 'googlesafebrowsing detection'

    if phish_url:
        return True
