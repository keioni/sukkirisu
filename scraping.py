from urllib import request
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

def get_sukkirisu(soup):
    items = dict()
    for div_body in soup.find_all("div", class_='flTxt'):
        part = div_body.find_all('p')
        rank_level = div_body.attrs['class'][0]
        if len(part) == 3:
            month = part[0].string
            rank = part[1].string
            message = part[2].string
        elif len(part) == 2:
            month = part[0].string
            rank = ''
            message = part[1].string
        item = {
            'rank': rank,
            'rank_level': rank_level,
            'text': message,
            'color': div_body.find(id='color').string
        }
        month = div_body.find("p", class_="monthTxt").string
        items[month] = item
    return items

def scraping():
    # url = "http://www.ntv.co.jp/sukkiri/sukkirisu/index.html"
    # html = request.urlopen(url)
    # soup = BeautifulSoup(html, "html.parser")
    soup = BeautifulSoup(open("tmp/sukkirisu.html", encoding='utf8'), features='html.parser')
    items = get_sukkirisu(soup)
    print_result(items)

if __name__ == "__main__":
    scraping()
