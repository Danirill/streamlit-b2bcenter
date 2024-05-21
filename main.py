import requests
import streamlit as st
from bs4 import BeautifulSoup


b2b_url = st.text_input("URL to b2bcenter", value="https://www.b2b-center.ru/market/razrabotka-onlain-platformy-dlia-klientov-ao-slpk/tender-3652716/?recommended=1&message_info=NjYzMDg1MzI4Yjg5NzkuMTkxMDMxODZfWmN3OEpFWUVZbUFjS0JhdE4zdlVlY1JUUXJtUzMvSStyQkNwNHlNOVduVk5JK3R6MGpaQlJlVjNuNU9JSTc3VTJHOWMyN1BkSERlZmY0WUJMQ1hRZVE9PQ%3D%3D&utm_medium=email&utm_source=recommended&conversion_id=3&utm_term=1301&utm_campaign=bulletin_market&utm_content=3652716&end=0")
parsed_data = {}


def fetch_and_parse(url):
    # Загружаем страницу по указанному URL
    response = requests.get(url)

    # Проверяем успешность запроса
    if response.status_code == 200:
        # Получаем содержимое страницы
        page_content = response.content

        # Парсим содержимое страницы с помощью BeautifulSoup
        soup = BeautifulSoup(page_content, 'html.parser')
        st.write(f"Страница загружена")
        return soup
    else:
        st.write(f"Не удалось загрузить страницу. Статус-код: {response.status_code}")
        return None


if st.button("Создать лид"):
    st.write('parsing...')
    soup = fetch_and_parse(b2b_url)
    div = soup.find('div', class_='s2')

    if div:
        parsed_data['name'] = div.get_text(strip=True)
    else:
        st.write("Не удалось найти div с классом 's2'")

    main_table = soup.find('td', {'id': 'auction_info_td'})
    firstspan = main_table.find('span')
    secondspan = firstspan.find('span')
    parsed_data['description'] = secondspan.get_text(strip=True)



    webhook_url = "https://gratio.bitrix24.ru/rest/20/yztk13b75z7fvlyv/crm.lead.add.json"

    # Данные лида
    lead_data = {
        "fields": {
            "TITLE": parsed_data['name'],
            "SOURCE_DESCRIPTION": parsed_data['description'],
            # "NAME": "Имя",
            # "LAST_NAME": "Фамилия",
            # "STATUS_ID": "NEW",
            # "OPENED": "Y",
            # "ASSIGNED_BY_ID": 1,
            "COMMENTS": b2b_url,
            # "PHONE": [{"VALUE": "1234567890", "VALUE_TYPE": "WORK"}],
            # "EMAIL": [{"VALUE": "example@example.com", "VALUE_TYPE": "WORK"}],
            # Добавьте другие поля по мере необходимости
        },
        "params": {"REGISTER_SONET_EVENT": "Y"}
    }

    # Выполнение POST-запроса к API Битрикс24
    response = requests.post(webhook_url, json=lead_data)

    # Проверка ответа
    if response.status_code == 200:
        result = response.json()
        if result.get("result"):
            st.write(f"Лид успешно создан с ID: {result['result']}")
        else:
            st.write(f"Ошибка при создании лида: {result}")
    else:
        st.write(f"Ошибка HTTP: {response.status_code} {response.text}")







