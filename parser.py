import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
}

url = "https://www.avito.ru/sankt_peterburg_i_lo/tovary_dlya_kompyutera/komplektuyuschie/operativnaya_pamyat"
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

rams = soup.find_all('div', {'data-marker': 'item'})

for ram in rams[:10]:
    try:
        # 1. Название (основные варианты поиска)
        title = None

        # Вариант 1: По data-marker
        title_elem = ram.find(attrs={"data-marker": "item-title"})
        if title_elem:
            title = title_elem.text.strip()

        # Вариант 2: По itemprop
        if not title:
            title_elem = ram.find(itemprop="name")
            if title_elem:
                title = title_elem.text.strip()

        # Вариант 3: По классу заголовка
        if not title:
            title_elem = ram.find('h3', class_=lambda x: x and 'title' in x.lower())
            if title_elem:
                title = title_elem.text.strip()

        # Вариант 4: Крайний случай - ищем любой h3
        if not title:
            title_elem = ram.find('h3')
            if title_elem:
                title = title_elem.text.strip()

        title = title or "Название не найдено"

        # 2. Цена
        price = ram.find('meta', itemprop='price')
        price = price['content'] if price else \
            ram.find(attrs={"data-marker": "item-price"}).text.strip() if car.find(
                attrs={"data-marker": "item-price"}) else \
                "Цена не указана"

        # 3. Параметры
        params = ram.find(attrs={"data-marker": "item-specific-params"})
        params = params.text.strip() if params else \
            ram.find('div', class_=lambda x: x and 'params' in x.lower()).text.strip() if ram.find('div', class_=lambda
                x: x and 'params' in x.lower()) else \
                "Параметры не указаны"

        # 4. Ссылка
        link = ram.find('a', itemprop='url')
        link = "https://www.avito.ru" + link['href'] if link else \
            "https://www.avito.ru" + ram.find('a', href=True)['href'] if ram.find('a', href=True) else \
                "Ссылка не найдена"

        print(f" {title}\n Цена: {price} ₽\n {params}\n {link}\n{'=' * 50}\n")

    except Exception as e:
        print(f"Ошибка при обработке объявления: {str(e)}")
        continue