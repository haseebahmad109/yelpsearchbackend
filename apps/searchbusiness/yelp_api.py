import requests

from django.conf import settings

CLIENT_ID = "hcHRZJw7gIwYaESrEZzrvw"
CLIENT_SECRET = "2J99UhNNiU2aosAJ3ijvyy7pMB3CR4J6dKsgN4ZoOzUisQs8DYpWs0QkFOvdSgOT"
GRANT_TYPE = 'client_credentials'

API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
SEARCH_LIMIT = settings.YELP_SEARCH_LIMIT
TOKEN_PATH = '/oauth2/token'

#TODO: Store Beaere Token so donot required to always get 
# new bearer Token
def obtain_bearer_token(host, path):
    url = '{0}{1}'.format(host, path)
    assert CLIENT_ID, "Please supply your client_id."
    assert CLIENT_SECRET, "Please supply your client_secret."
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': GRANT_TYPE,
    }
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
    }
    response = requests.request('POST', url, data=data, headers=headers)
    bearer_token = response.json()['access_token']
    return bearer_token

def search(term, location, page=1):
    bearer_token = obtain_bearer_token(API_HOST, TOKEN_PATH)

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT,
        'offset': (page-1) * SEARCH_LIMIT
    }

    url = '{0}{1}'.format(API_HOST, SEARCH_PATH)
    headers = {
        'Authorization': 'Bearer %s' % bearer_token,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)
    return response.json()
