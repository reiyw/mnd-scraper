from urllib.parse import parse_qs, urlencode, urlparse

import scrapy

from model import Response


class MndSpider(scrapy.Spider):
    name = "minutes"
    start_urls = [
        f"https://kokkai.ndl.go.jp/api/meeting?sessionFrom={i}&issueFrom=1&recordPacking=json"
        for i in range(1, 201)
    ]
    custom_settings = {"DOWNLOAD_DELAY": 2}

    def parse(self, response: scrapy.http.Response):
        resp: Response = Response.from_json(response.text)
        if resp.meeting_record is not None:
            yield resp.to_dict()
            yield response.follow(_next_issue(response.url), self.parse)


def _next_issue(url):
    query = parse_qs(urlparse(url).query)
    session = query["sessionFrom"][0]
    issue = query["issueFrom"][0]
    next_query = {
        "sessionFrom": session,
        "issueFrom": int(issue) + 1,
        "recordPacking": "json",
    }
    return "https://kokkai.ndl.go.jp/api/meeting?" + urlencode(next_query)
