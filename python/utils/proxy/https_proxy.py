
import logging
import argparse
import requests
import pandas as pd


url = 'https://us-proxy.org/'

r = requests.get(url)
html = r.content

df_list = pd.read_html(html)

print(df_list)
ips = df_list[0]

