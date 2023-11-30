# %%
import pandas as pd
import urllib
import requests

FILENAME = 'database-commons'

dbs = pd.read_json(f'../input/{FILENAME}.json') # already sorted by impact scores
dbs = pd.DataFrame.from_dict(dbs.data.to_dict(), orient='index')

# see if the site still works
# dbs = dbs[79:82]
def connection_status(x):
    try:
        return requests.get(x).status_code
    except requests.exceptions.ConnectionError:
        return -1
    
def check_site(url):
    try:
        # https://stackoverflow.com/questions/51972160/python-check-if-website-exists-for-a-list-of-websites
        conn = urllib.request.urlopen(url, timeout=1)
    except urllib.error.HTTPError as e:
        return e.code
    except urllib.error.URLError as e:
        return e.reason
    except Exception:
        return -1
    else:
        return 200

dbs['connection'] = None
dbs['connection'] = dbs['url'].apply(lambda x: check_site(x))

dbs.to_json(f'../input/{FILENAME}-with-status.json', orient="records")

dbs