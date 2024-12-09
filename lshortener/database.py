import os
import psycopg2
import urllib.parse


def connect():
    url = os.environ["DATABASE_URL"]
    url = urllib.parse.urlparse(url)
    return psycopg2.connect(
        dbname=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname
    )

