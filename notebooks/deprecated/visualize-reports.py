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
data['error'] += data['contrast']
data.head()
# %%
"""
Overview
"""
metric = [
    ('errors', 'error', '#CC7DAA'),
    # ('contrast issues', 'contrast', '#D6641E'),
    ('alerts', 'alert', '#E6A01B'),
]

for (name, field, hex) in metric:
    plot_alert = alt.Chart(data).mark_bar().encode(
        y=alt.X(f'{field}:Q', scale=alt.Scale(type='log'), title=f'The number of {name}'),
        x=alt.Y('shortName:N', sort='-y', title='Data portals', axis=alt.Axis(labelAngle=300)),
        color=alt.value(hex)
    ).transform_filter(
        alt.datum[field] > 0  
    ).properties(
        title=f'The Number of "{name.capitalize()}" By Data Portals'
    )

    if name == 'errors':
        # https://webaim.org/projects/million/
        mean = 43.7
        r = alt.Chart().mark_rule(color='black', strokeDash=[10, 10]).encode(y=alt.datum(mean))
        t = alt.Chart().mark_text(color='black', strokeDash=[10, 10], angle=0, dy=-10).encode(y=alt.datum(mean), text=alt.datum('WAVE Average'))
        plot_alert += (r + t)

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
"""
By category
"""
c = [
    ('alt_link_missing', 'lightgrey'),
    ('alt_missing', 'blue'),
    ('alt_spacer_missing', 'lightgrey'),
    ('aria_menu_broken', 'lightgrey'),
    ('aria_reference_broken', 'lightgrey'),
    ('button_empty', 'orange'),
    ('contrast', 'red'),
    ('heading_empty', 'lightgrey'),
    ('label_empty', 'lightgrey'),
    ('label_missing', 'green'),
    ('label_multiple', 'lightgrey'),
    ('language_missing', 'purple'),
    ('link_empty', '#CE5D5C'),
    ('link_skip_broken', 'lightgrey'),
    ('th_empty', 'lightgrey'),
    ('title_invalid', 'lightgrey'),
]
by_category = details.copy()
by_category = by_category[by_category.type != 'alert']
by_category = by_category.groupby(by=['name']).count()
by_category['proportion'] = by_category['count'] / 80
by_category = by_category.reset_index()

plot = alt.Chart(by_category).mark_bar(
    stroke='white',
    opacity=1
).encode(
    x=alt.X('name:N', sort='-y', axis=alt.Axis(labelAngle=300, grid=False, zindex=1)),
    y=alt.Y('proportion:Q', axis=alt.Axis(format='%'), scale=alt.Scale(domain=[0, 1])),
    color=alt.Color('name:N', scale=alt.Scale(domain=[d for (d, r) in c], range=[r for (d, r) in c])),
).resolve_scale(y='independent').properties(
    # height=40,
    width=800
)
plot = apply_theme(plot)
plot
# %%
df = data.copy()
df.error += df.contrast
df['no_errors'] = data.error.apply(lambda x: 'no errors' if x == 0 else 'with errors')
df = df.groupby(by='no_errors').count()
df['percent'] = df.error / 80
df = df.reset_index()

plot = alt.Chart(df).mark_bar().encode(
    x=alt.X('no_errors:N'),
    y=alt.Y('percent:Q', title=None, axis=alt.Axis(format='%')),
    color=alt.Color('no_errors:N', legend=None, scale=alt.Scale(range=['#3275B4', '#CC7DAA']))
).properties(
    title='The % of Homepages with & without Any Errors',
    width=300
)

plot = apply_theme(plot)

plot
df
# %%
