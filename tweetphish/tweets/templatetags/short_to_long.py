from django import template
import requests
import json

register = template.Library()

@register.filter(name="short_to_long")
def short_to_long(url):
    long_url_json = requests.get('http://api.longurl.org/v2/expand?url=%s&format=json' % url)
    try:
        json_data = json.loads(long_url_json.content)
        long_url = json_data['long-url']
    except:
        long_url = url

    return long_url