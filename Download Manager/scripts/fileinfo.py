import requests


def get_file_size(u):
    try:
        return int(requests.head(u).headers["Content-Length"])
    except:
        return False


def get_file_name(u):
    return u.split("/")[-1]


def get_shorted_url(u):
    if len(u) > 60:
        return u[:32]+"...."+u[-32:]
    else:
        return u
