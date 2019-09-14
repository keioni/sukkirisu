from urllib import request
from bs4 import BeautifulSoup

def get_data():
    pass

def print_result(items):
    rank_level_text = {
        'type2': 'スッキリす',
        'type3': 'まあまあスッキリす',
    }
    for month in items:
        if items[month]['rank_level'] == 'type1':
            rank = '超スッキリす！'
        elif items[month]['rank_level'] == 'type4':
            rank = 'ガッカリす...'
        else:
            rank = '{} {}'.format(
                items[month]['rank'],
                rank_level_text[items[month]['rank_level']]
            )
        print('{} : {}月 : {}。ラッキーカラーは{}。'.format(
            rank,
            month,
            items[month]['text'],
            items[month]['color']
        ))

def scraping():
    # url = "http://www.ntv.co.jp/sukkiri/sukkirisu/index.html"
    # html = request.urlopen(url)
    # soup = BeautifulSoup(html, "html.parser")
    soup = BeautifulSoup(open("tmp/sukkirisu.html", encoding='utf8'))

    items = dict()
    for part in soup.find_all("div", class_='flTxt'):
        message_text = part.find_all('p')
        rank_level = part.attrs['class'][0]
        if len(message_text) == 3:
            month = message_text[0].string
            rank = message_text[1].string
            message = message_text[2].string
        elif len(message_text) == 2:
            month = message_text[0].string
            rank = ''
            message = message_text[1].string
        item = {
            'rank': rank,
            'rank_level': rank_level,
            'text': message,
            'color': part.find(id='color').string
        }
        month = part.find("p", class_="monthTxt").string
        items[month] = item
    print_result(items)

if __name__ == "__main__":
    scraping()
