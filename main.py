import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Укажите путь к geckodriver
gecko_path = "C:\\Users\\karon\\Desktop\\geckodriver.exe"

# Настройка для работы с Firefox через Selenium
options = Options()

# Создание объекта Service для geckodriver
service = Service(executable_path=gecko_path)

driver = webdriver.Firefox(service=service, options=options)

# Открытие веб-страницы
driver.get('https://poiskvps.ru/')  # Замените на ваш URL
print("Страница загружена: https://poiskvps.ru/")

# Ожидаем загрузки страницы
time.sleep(5)

# Список для хранения всех данных
data = []

# Пагинация: продолжаем парсить, пока есть страницы
page_number = 1

# Функция для сохранения данных в файл
def save_data_to_file(data):
    try:
        with open('output_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Данные успешно сохранены на странице {page_number}")
    except Exception as e:
        print(f"Ошибка при сохранении данных в файл: {e}")

while True:
    print(f"Парсинг страницы {page_number}...")

    # Получаем HTML страницы после загрузки
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Находим все таблицы с классом 'table 1'
    tables = soup.find_all('table', class_='table1')
    print(f"Найдено {len(tables)} таблиц на странице {page_number}")

    # Для каждой таблицы находим строки
    for table in tables:
        rows = table.find_all('tr')  # Все строки в таблице
        for row in rows:
            # Извлекаем все ячейки в строке
            cells = row.find_all('td')
            # Проверяем, что в строке есть достаточно ячеек
            if len(cells) >= 8:  # Например, ожидаем минимум 8 ячеек
                company_name = cells[0].find('a', class_='button2')
                company_url = company_name['href'] if company_name else 'Не найдено'

                # Извлекаем информацию из ячеек
                company_name = company_name.get_text(strip=True)
                disk_space = cells[2].get_text(strip=True)
                ram = cells[3].get_text(strip=True)
                cpu = cells[4].get_text(strip=True)
                traffic = cells[5].get_text(strip=True)
                price = cells[6].get_text(strip=True)
                virtualization = cells[7].get_text(strip=True)
                countries = cells[8].get_text(strip=True)

                # Собираем все данные в словарь
                company_data = {
                    "company_name": company_name,
                    "company_url": company_url,
                    "disk_space": disk_space,
                    "ram": ram,
                    "cpu": cpu,
                    "traffic": traffic,
                    "price": price,
                    "virtualization": virtualization,
                    "countries": countries
                }
                # Добавляем словарь в список
                data.append(company_data)
                print(f"Данные компании '{company_name}' добавлены.")

    # Сохраняем данные после каждой страницы
    save_data_to_file(data)

    # Пытаемся найти кнопку "Следующая страница"
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[text()="След →"]'))
        )
        print("Кнопка 'След →' найдена. Переход на следующую страницу.")
        next_button.click()  # Кликаем на кнопку для перехода на следующую страницу

        # Ожидаем, пока страница загрузится
        time.sleep(5)
        page_number += 1  # Увеличиваем номер страницы

    except Exception as e:
        print(f"Ошибка или нет следующей страницы: {e}")
        break  # Если кнопка не найдена или возникла ошибка, выходим из цикла

# Сохраняем данные в JSON файл
with open('output_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

# Закрываем драйвер
driver.quit()

print("Данные успешно сохранены в файл output_data.json")
