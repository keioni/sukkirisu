import json
import urllib
from bs4 import BeautifulSoup


def print_result(items):
  for month in items:
    if items[month]['rank_level'] == 'type1':
      rank = '超スッキリす！'
    elif items[month]['rank_level'] == 'type4':
      rank = 'ガッカリす...'
    else:
      if items[month]['rank_level'] == 'type2':
        rank = 'スッキリす'
      elif items[month]['rank_level'] == 'type3':
        rank = 'まあまあスッキリす'
      rank = '{} {}'.format(items[month]['rank'], rank)
    print('{} : {}月 {}。ラッキーカラーは{}。'.format(
        rank,
        month,
        items[month]['text'],
        items[month]['color']
    ))


def normalize_rank_level(rank_level):
  if rank_level == 'type1':
    result = '超スッキリす！'
  elif rank_level == 'type4':
    result = 'ガッカリす...'
  else:
    if rank_level == 'type2':
      result = 'スッキリす'
    elif rank_level == 'type3':
      result = 'まあまあスッキリす'
  return result


def get_sukkirisu(soup):
  items = dict()
  for div_body in soup.find_all("div", class_='flTxt'):
    part = div_body.find_all('p')
    item = {
      'month': part[0].string,
      'color': div_body.find(id='color').string,
      'rank_level': normalize_rank_level(div_body.attrs['class'][0])
    }
    if len(part) == 3:
      item['rank'] = part[1].string
      item['message'] = part[2].string
    elif len(part) == 2:
      item['rank'] = ''
      item['message'] = part[1].string
    month = div_body.find("p", class_="monthTxt").string
    items[month] = item
  return items


def scraping():
  # url = "http://www.ntv.co.jp/sukkiri/sukkirisu/index.html"
  # html = request.urlopen(url)
  # soup = BeautifulSoup(html, "html.parser")
  soup = BeautifulSoup(
      open("tmp/sukkirisu.html", encoding='utf8'), features='html.parser')
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
