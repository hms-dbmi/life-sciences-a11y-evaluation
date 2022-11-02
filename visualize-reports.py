# %%
import pandas as pd
import altair as alt
import json
from theme import apply_theme
# %%
data = []
with open('./a11y-reports.json', 'r') as f:
    reports = json.load(f)
    for report in reports:
        categories = report['report']['categories']

        row = {}
        row['dbId'] = report['dbId']
        row['shortName'] = report['shortName']
        row['url'] = report['url']
        row['error'] = categories['error']['count']
        row['contrast'] = categories['contrast']['count']
        row['alert'] = categories['alert']['count']
        data.append(row)
data = pd.DataFrame.from_records(data)
data.head()
# %%
"""
Overview
"""
metric = [
    ('errors', 'error', '#CC7DAA'),
    ('contrast issues', 'contrast', '#D6641E'),
    ('alerts', 'alert', '#E6A01B'),
]

for (name, field, hex) in metric:
    plot_alert = alt.Chart(data).mark_bar().encode(
        x=alt.X(f'{field}:Q', scale=alt.Scale(type='log'), title=f'The number of {name}'),
        y=alt.Y('shortName:N', sort='-x', title='Data portals'),
        color=alt.value(hex)
    ).transform_filter(
        alt.datum[field] > 0  
    ).properties(
        title=f'The Number of "{name.capitalize()}" By Data Portals'
    )

    plot_alert = apply_theme(plot_alert)
    # plot_alert.save('report-error.png') # does not work
    plot_alert.display()
# %%
"""
Detailed issues
"""
details = []
with open('./a11y-reports.json', 'r') as f:
    reports = json.load(f)
    for report in reports:
        metrics = ['error', 'contrast', 'alert']
        for m in metrics:
            stats = report['report']['categories'][m]['items']

            row = {}
            row['dbId'] = report['dbId']
            row['shortName'] = report['shortName']
            row['url'] = report['url']
            row['type'] = m

            for e in stats:
                name = stats[e]['id']
                count = stats[e]['count']
                row_copy = row.copy()
                row_copy['name'] = name
                row_copy['count'] = count
                
                details.append(row_copy)

details = pd.DataFrame.from_records(details)
details
# %%
plot = alt.Chart(details).mark_rect(
    stroke='white',
    opacity=1
).encode(
    # x=alt.X('count', scale=alt.Scale(type='linear'), title='The number of issues'),
    x=alt.X('shortName:N', sort='-color', axis=alt.Axis(labelAngle=270, grid=True, zindex=0)),
    y=alt.Y('name:N', title=None, axis=alt.Axis(grid=True, zindex=0)),
    color=alt.Color(
        'count:Q',
        scale=alt.Scale(type='log', domain=[1, 100], clamp=True),   
        legend=alt.Legend(gradientLength=300)
    ),
    row=alt.Row('type:N', header=alt.Header(labelOrient='left', title=None), sort=['error', 'contrast', 'alert'])
    # row=alt.Row('name:N', title=None, header=alt.Header(
    #     labelOrient='left', labelAngle=0, labelAnchor='middle', labelAlign='left'
    # ), spacing=0)
).transform_filter(
    alt.datum['count'] > 0
).resolve_scale(y='independent').properties(
    # height=40,
    # width=600
)
plot = apply_theme(plot)
plot
# %%
