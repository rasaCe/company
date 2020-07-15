import requests
import pandas as pd
from scapy.all import IP, ICMP, sr1

url = 'https://us-proxy.org/'


def fetch_list(src_url, port=8080, https='no', head_count=20):
    r = requests.get(src_url)
    html = r.content
    df_list = pd.read_html(html, parse_dates=True)
    ips = df_list[0].dropna()
    ips = ips.drop(columns=['Google'])

    ips = ips.rename(columns={'Last Checked': 'last_checked', 'IP Address': 'ip'})
    new_cols = [e.lower() for e in list(ips.columns)]
    old_cols = list(ips.columns)
    columns = dict(zip(old_cols, new_cols))
    ips = ips.rename(columns=columns)  
    ips['port'] = ips['port'].astype(int)
    
    http_only = ips['https'] == 'no'
    ips = ips[http_only].drop(columns=['https'])
    http_only_port = ips['port'] == port
    ips = ips[http_only_port].drop(columns=['port'])
    
    ips = ips[['ip']].head(head_count)
    return ips.reset_index().drop(columns=['index'])


proxy_list = fetch_list(url, port=80, https='yes')


"""
import imaplib

IMAP_SERVER='imap.gmail.com'
IMAP_PORT=993

try:
 M = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
 rc, resp = M.login('email address', 'password')
 print rc, resp
 M.logout()
except Exception, e:
 print e
"""


def ping(ip):
    """
    :param ip: destination ip address.
    :return: True/False whether the target is alive/dead.
    """
    try:
        p = sr1(IP(dst=ip)/ICMP())
        print('Response: ', p)
        if p is not None:
            p.show()
            return True
        return False
    except OSError as e:
        print(e)
        print('ip: ', ip)
    return False


def get_active_proxies(source_proxy_list):
    active_proxies = []
    for idx, row in source_proxy_list.iterrows():
        ip = row['ip']
        print('pinging: ', ip)
        if ping(ip):
            active_proxies.append(ip)
    return active_proxies


ping('10.0.0.6')
quit()


active_proxies = get_active_proxies(proxy_list)
print('number of active proxies: ', len(active_proxies))

