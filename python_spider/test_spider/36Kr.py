import requests
import json
import re

class Spider36():
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"
        }
        self.start_url = "http://36kr.com/"

    def _parse_url(self, url):
        response = requests.get(url, headers = self.headers, timeout = 5)
        # assert response.status_code == 200
        return response.content.decode()

    def parse_url(self, url):
        try:
            html_str = self._parse_url(url)
        except:
            html_str = None

        return html_str

    def get_content(self, html_str):
        pattern = re.compile(r"<script>var props=(.*?),locationnal")
        cont = pattern.findall(html_str)[0]
        # cont = json.loads(cont)
        return cont

    def save_cont(self, cont):
        with open("36kr.json", "w", encoding="utf-8") as f:
            f.write(cont)

    def run(self):
        html_str = self.parse_url(self.start_url)
        cont = self.get_content(html_str)
        self.save_cont(cont)
        # print(cont)

if __name__ == '__main__':
    Kr = Spider36()
    Kr.run()