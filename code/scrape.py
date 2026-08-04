import requests
import codecs
import datetime
import os
from pyquery import PyQuery as pq


def createMarkdown(date, filename):
    with open(filename, "w") as f:
        f.write("# "+ date + "Github Trending\n")

def scrape(filename):
    url = "https://github.com/trending"
    HEADER = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language' : 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
    }

    r = requests.get(url, headers=HEADER)
    assert r.status_code == 200

    d = pq(r.content)
    items = d('div.Box article.Box-row')

    with codecs.open(filename, 'a', encoding = 'utf-8') as f:
        for item in items:
            i = pq(item)
            raw_title = i(".lh-condensed a").text()
            title = " ".join(raw_title.split())
            description = i("p.col-9").text().strip()
            language = i("span[itemprop='programmingLanguage']").text().strip()
            if not language:
                language = "Unknown"
            stars_today = i("span.float-sm-right").text().strip()
            url = "https://github.com" + i(".lh-condensed a").attr("href")

            f.write(f'### [{title}]({url})\n')
            f.write(f'- **主要语言**: {language}\n')
            f.write(f'- **今日 Star**:{stars_today}\n')
            f.write(f'- **项目简介**:{description}\n\n')

def job():
    strdate = datetime.datetime.now().strftime('%Y-%m-%d')
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_dir = os.path.join(project_root, 'TrendingLog')
    os.makedirs(log_dir, exist_ok=True)
    filename = os.path.join(log_dir, f'{strdate}.md')
    createMarkdown(strdate, filename)
    scrape(filename)

if __name__ == '__main__':
    job()