import requests
from youtube.itags import *


def get_formatted_data(dct):
    data = []
    for i in dct:
        x = get_format_profile(int(i["itag"]))
        if "contentLength" in i.keys():
            content_length = int(i["contentLength"])
        else:
            content_length = int(requests.head(i["url"]).headers["Content-Length"])
        if content_length:
            x["contentLength"] = content_length
            data.append(x)
        x["url"] = i["url"]

    videos = []
    audios = []

    print(data)

    for x in data:
        st = False
        if x["resolution"]:
            for p in videos:
                if p["resolution"] == x["resolution"]:
                    if int(p["contentLength"]) <= int(x["contentLength"]):
                        videos[videos.index(p)] = x
                    st = True
            if not st:
                videos.append(x)
        else:
            for p in audios:
                if p["abr"] == x["abr"]:
                    if int(p["contentLength"]) <= int(x["contentLength"]):
                        audios[audios.index(p)] = x
                    st = True
            if not st:
                audios.append(x)

    vv = {}
    aa = {}
    for i in videos:
        vv[int(i["resolution"][:-1])] = i
    for i in audios:
        aa[int(i["abr"][:-4])] = i
    videos, audios = [], []
    for i in sorted(vv.keys(), reverse=True):
        videos.append(vv[i])
    for i in sorted(aa.keys(), reverse=True):
        audios.append(aa[i])

    return videos + audios
