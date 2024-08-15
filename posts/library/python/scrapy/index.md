# Scrapy


# Introduction

학부 시절 Django를 처음 배울 때를 제외하고 간만에 웹 크롤링을 경험할 기회가 생겼다. Beautifulsoup | Selenium을 사용할 수도 있지만 찾아보니 빅데이터 혹은 딥러닝에서 데이터 크롤링을 할 때 Scrapy를 많이 사용한다는 것을 발견하고 이번 기회에 사용해 보기로 마음 먹고 간단한 데이터 크롤링을 구축해봤다.

## 설치 및 시작

```bash
pip install scrapy
```

```bash
scrapy startproject arxiv_crawling
```

`startproject` 명령어를 입력하면 다음과 같이 scrapy가 자동으로 템플릿 폴더를 생성해준다.

<img src="/images/library/python/scrapy/1.png" />

생성된 프로젝트 디렉토리로 이동해서 target url에 맞는 프로젝트를 생성해준다.

```bash
cd src/crawler/arxiv_crawling/arxiv_crawling/spiders

scrapy genspider arxiv {TARGET_URL}
```

실행 명령어는 다음과 같다.

```bash
scrapy crawl arxiv
```

## 크롤링 코드 작성

`start_requests`: 이 함수는 target url에 사용자 요청으로 들어온 **query**를 붙여준다.

`parse`: 데이터 크롤링을 수행하는 핵심 함수이다. 크롤링을 위해서는 웹 사이트의 구조를 뜯으어보고 어떤 div | li | ol | p 의 **classname**을 찾아서 지정해줘야 한다. 간만에 웹 개발을 하다보니 html 뜯어보고 **xpath**를 찾는 과정에 시간이 소모됐다.

arxiv 사이트에서 찾고자 하는 query = machinelearning 페이지 구조는 다음과 같다. 이에 맞춰 **xpath**를 지정해준다.

이어서 title, abstract 데이터를 긁어와서 분리해준다. 마지막으로 title로 데이터 파일을 저장해준다.

<img src="/images/library/python/scrapy/2.png" />

arxiv.py 파일에 이제 크롤링을 위한 코드를 작성해준다.

```python
import scrapy
from pathlib import Path


class ArxivSpider(scrapy.Spider):
    name = "arxiv"

    custom_settings = {"REQUEST_FINGERPRINTER_IMPLEMENTATION": "2.7"}

    def __init__(self, queries=[], *args, **kwargs):
        super(ArxivSpider, self).__init__(*args, **kwargs)
        self.queries = queries

    def start_requests(self):
        for query in self.queries:
            url = (
                f"https://arxiv.org/search/?query={query}&searchtype=all&source=header"
            )
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        articles = response.xpath('//li[contains(@class, "arxiv-result")]')
        for article in articles:
            title = article.xpath('.//p[contains(@class, "title")]/text()').getall()
            abstract = article.xpath(
                './/span[contains(@class, "abstract-short")]/text()'
            ).getall()

            title = " ".join([t.strip() for t in title]).strip()
            abstract = " ".join([t.strip() for t in abstract]).strip()

            safe_title = "".join(
                [c if c.isalnum() or c.isspace() else "_" for c in title]
            )
            file_path = Path(f"./data/raw/{safe_title}.csv")

            try:
                file_path.parent.mkdir(parents=True, exist_ok=True)

                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(f"Title: {title}\n")
                    file.write(f"Abstract: {abstract}\n")
            except Exception as error:
                print(f"Failed to save file {file_path}: {error}")

            yield {
                "title": title,
                "abstract": abstract,
            }
```

하지만 현재는 main.py에서 class를 call해서 사용할 수 있는 것이 아니라 직접 command를 입력해서 사용하고 있다. 처음에는 root 디렉토리에서 shell script를 사용하려고 했으나, 생각해보니 사용자 입력에 따른 데이터를 가져와야 하니 수정해야 했다. 처음 작성한 shell script는 다음과 같다.

```shell
#!/bin/bash

echo "Wikipedia data crawling completed. Results saved to $OUTPUT_DIR"

cd "$(dirname "$0")"

OUTPUT_DIR="data/raw"

SPIDER_DIR="src/arxiv_crawling/arxiv_crawling/spiders"

mkdir -p "$OUTPUT_DIR"

cd "$SPIDER_DIR" || { echo "Failed to change directory to $SPIDER_DIR"; exit 1; }

scrapy crawl arxiv -o "../../../../$OUTPUT_DIR/result.csv"

echo "Arxiv data crawling completed. Results saved to $OUTPUT_DIR"
```

## main 클래스에서 사용하도록 수정

공식 문서를 찾아보니 `CrawlerProcess`를 발견할 수 있었다. 이어서 공식 문서에 따라 다음과 같이 수정해 주었다.

```python
from src.arxiv_crawling.arxiv_crawling.spiders.arxiv import ArxivSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def crawler(source) -> list:
    # test 용 쿼리
    # 추후에 이론 목록들 정의되는 대로 수정
    queries = ["machinelearning", "deeplearning"]

    # Arxiv 크롤러
    process = CrawlerProcess(get_project_settings())
    process.crawl(ArxivSpider, queries)
    process.start()
```
