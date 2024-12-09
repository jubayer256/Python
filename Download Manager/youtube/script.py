from urllib.parse import parse_qs, parse_qsl, urlparse, urlencode, quote
import requests
import json
from youtube.formats import get_formatted_data
from collections import OrderedDict
from tkinter import messagebox

headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36"}


class YouTube:
    def __init__(self, u):
        self.size = None
        self.url = u
        self._get_details()

    def _get_details(self):
        info_url = self._get_video_url()
        content = requests.get(info_url, headers=headers)
        info_data = dict(parse_qsl(content.content.decode("utf8")))
        if "player_response" not in info_data.keys():
            messagebox.showinfo(message="file can't be downloaded")
            return False
        details = json.loads(info_data["player_response"])["videoDetails"]
        streaming_data = json.loads(info_data["player_response"])["streamingData"]
        formats = streaming_data["formats"] + streaming_data["adaptiveFormats"]
        self.title = details["title"]
        self.length = details["lengthSeconds"]
        self.formats = get_formatted_data(formats)

    def _get_video_url(self):
        video_id = parse_qs(urlparse(self.url).query)["v"][0]
        params = OrderedDict(
            [
                ("video_id", video_id),
                ("ps", "default"),
                ("eurl", quote(self.url)),
                ("hl", "en_US"),
                ("html5", "1"),
            ]
        )
        return "https://youtube.com/get_video_info?" + urlencode(params)


# y = YouTube("https://www.youtube.com/watch?v=rfscVS0vtbw&t=112s")

