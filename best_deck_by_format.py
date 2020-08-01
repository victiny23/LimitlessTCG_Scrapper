from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from plotnine import ggplot, aes,  geom_bar, geom_col

limitless_url = 'https://limitlesstcg.com/decks/?time=all&format='
play_formats = ['SUM-CES','SUM-LOT','SUM-TEU','SUM-UNB','UPR-UNM','UPR-CEC','UPR-SSH','UPR-RCL']#,,]

deck_tables = {}
for play_format in play_formats:
    url = limitless_url + play_format
    req = Request(url=url, headers={'user-agent': 'my-app'})
    response = urlopen(req)

    html = BeautifulSoup(response,'html')
    deck_table = html.find('table')
    deck_tables[play_format] = deck_table


deck_list = []
point_list = []
for play_format, deck_table in deck_tables.items():
    for index, row in enumerate(deck_table.findAll('td')):
        if index % 5 == 1:
            deck = row.find('a')
            deck = deck.contents[0]
        elif index % 5 == 4:
            share = row.contents[0]
            share = float(share[:-1])
            deck_list.append([play_format, deck, share])

    for row2 in enumerate(deck_table.find_all('span')):
        point = int(row2[1].contents[0])
        point_list.append(point)

for idx, deck in enumerate(deck_list):
    deck_list[idx].append(point_list[idx])

deck_result = pd.DataFrame(deck_list, columns=['format','deck','share','point'])
print(deck_result)

plt.figure(figsize=(10, 8))
fig = sns.barplot(x='format', y='point',
            hue='deck',data=deck_result)
plt.show()
"""
fig = ggplot(data=deck_result) + geom_col(aes(x="format", y="share", fill="deck"))
print(fig)
"""



