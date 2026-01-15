
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
}


def get_rams(type=""):
    url = f"https://www.avito.ru/sankt_peterburg_i_lo/tovary_dlya_kompyutera/komplektuyuschie/operativnaya_pamyat{'?q=' + type if type else ''}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        rams_elements = soup.find_all('div', {'data-marker': 'item'})
        rams = []




        for ram in rams_elements[:10]:  # Берем первые 10 объявлений
            try:
                ram_data = parse_ram(ram)
                if ram_data:
                    rams.append(ram_data)
            except Exception as e:
                print(f"Ошибка при обработке объявления: {str(e)}")
                continue

        return rams

    except Exception as e:
        print(f"Ошибка при парсинге: {str(e)}")
        return []


def parse_ram(ram):
    ram_data = {}

    # 1. Название
    title_elem = (ram.find(attrs={"data-marker": "item-title"}) or
                  ram.find(itemprop="name") or
                  ram.find('h3', class_=lambda x: x and 'title' in x.lower()) or
                  ram.find('h3'))
    ram_data['title'] = title_elem.text.strip() if title_elem else "Название не найдено"

    # 2. Цена
    price_elem = (ram.find('meta', itemprop='price') or
                  ram.find(attrs={"data-marker": "item-price"}))
    if price_elem:
        ram_data['price'] = price_elem.get('content', price_elem.text.strip())
    else:
        ram_data['price'] = "Цена не указана"

    # 3. Параметры
    params_elem = (ram.find(attrs={"data-marker": "item-specific-params"}) or
                   ram.find('div', class_=lambda x: x and 'params' in x.lower()))
    ram_data['params'] = params_elem.text.strip() if params_elem else "Параметры не указаны"

    # 4. Ссылка
    link_elem = ram.find('a', itemprop='url') or ram.find('a', href=True)
    if link_elem:
        ram_data['link'] = "https://www.avito.ru" + link_elem.get('href', '')
    else:
        ram_data['link'] = "Ссылка не найдена"

    return ram_data