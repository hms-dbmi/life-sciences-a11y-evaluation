# %%
import pandas as pd
import urllib.request
import json
# %%
FILTER_TOP = 2 # select the top N portals
# %%
with open('api.key', 'r') as f:
    apiKey = f.read()
# %%
dbs = pd.read_json('./database-commons.json') # already sorted by impact scores
dbs = pd.DataFrame.from_dict(dbs.data.to_dict(), orient='index')
dbs = dbs[0:FILTER_TOP]
dbs
# %%
"""
Load existing reports
"""
with open('./a11y-reports.json', 'r') as f:
    reports = json.load(f)
reports
# print(reports)

"""
Iterate to add more reports
"""
for index, row in dbs.iterrows():
    dbId = row.dbId
    shortName = row.shortName
    url = row.url

    reportExist = any(report['dbId'] == dbId for report in reports)
    if not reportExist:
        print('Loading... ' + dbId, shortName, url)
        apiUrl = f'https://wave.webaim.org/api/request?key={apiKey}&reporttype=2&url={url}'
        # apiUrl = 'https://raw.githubusercontent.com/gosling-lang/gosling.js/master/tsconfig.json'
        with urllib.request.urlopen(apiUrl) as f:
            newReport = json.load(f)
            newData = {}
            newData['dbId'] = dbId
            newData['shortName'] = shortName
            newData['url'] = url
            newData['report'] = newReport
            reports.append(newData)
            # print(reports)

with open('./a11y-reports.json', 'w') as f:
    json.dump(reports, f)
    
# %%
