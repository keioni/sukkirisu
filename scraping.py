import json
import urllib.parse
import urllib.request
from typing import Dict, Optional

from bs4 import BeautifulSoup


def print_result(items):
  for month in items:
    print('{} {} : {}月 {}。ラッキーカラーは{}。'.format(
        items[month]['rank']['num'],
        items[month]['rank']['string'],
        month,
        items[month]['message'],
        items[month]['color']
    ))


def normalize_rank(rank: str) -> Dict[str, str]:
  result: Dict[str, str] = dict()
  if rank == 'type1':
    result['num'] = '1位'
    result['string'] = '超スッキリす！'
  elif rank == 'type4':
    result['num'] = '12位'
    result['string'] = 'ガッカリす...'
  else:
    result['num'] = ''
    if rank == 'type2':
      result['string'] = 'スッキリす'
    elif rank == 'type3':
      result['string'] = 'まあまあスッキリす'
  return result



def get_sukkirisu(soup):
  items = dict()
  for div_body in soup.find_all("div", class_='flTxt'):
    part = div_body.find_all('p')
    item = {
      'month': part[0].string,
      'color': div_body.find(id='color').string,
      'rank': normalize_rank(div_body.attrs['class'][0])
    }
    if len(part) == 3:
      item['rank']['num'] = part[1].string
      item['message'] = part[2].string
    elif len(part) == 2:
      item['message'] = part[1].string
    month = div_body.find("p", class_="monthTxt").string
    items[month] = item
  return items


def scraping():
  url = "http://www.ntv.co.jp/sukkiri/sukkirisu/index.html"
  html = urllib.request.urlopen(url)
  soup = BeautifulSoup(html, "html.parser")
  # soup = BeautifulSoup(
  #     open("tmp/sukkirisu.html", encoding='utf8'), features='html.parser')
  items = get_sukkirisu(soup)
  print_result(items)


def lambda_handler(event, context):
  print('event: ' + json.dumps(event))
  params = urllib.parse.parse_qs(event.get('body-json'), '')
  print('params: ' + json.dumps(params))
  scraping()
  result = {
    "response_type": "in_channel",
    "text": "It's 80 degrees right now.",
    "attachments": [
      {
          "text": "Partly cloudy today and tomorrow"
      }
    ]
  }
  return result


if __name__ == "__main__":
  event = dict()
  lambda_handler(event, None)
