import argparse
import requests
from user_agent import generate_user_agent
import pytube
import lxml.html as html
import lxml.etree as etree
from io import StringIO
from selenium import webdriver
import time
import os

"""путь сохранения видео"""
PATH = './videos/'


def load_page(url: str):
    """ метод загрузки страницы, извлечение html, и поиск видео"""
    os.makedirs(PATH,exist_ok=True)     # создание папки если ее нет

    # создание webdriver Selenium
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") # безголовый режим
    driver = webdriver.Chrome(options=options)

    print('загрузка страницы' , url)
    try:
        driver.get(url)
    except:
        print('Ошибка загрузки страницы' , url)
        return

    time.sleep(5) # ожидание загрузки страницы

    # извлечение html страницы
    main_page = driver.find_element_by_tag_name('html')
    page = html.parse(StringIO(main_page.get_attribute(('innerHTML'))))

    # запись html в файл
    with open('html.txt', 'w') as f:
        f.write(etree.tostring(page, pretty_print= True).decode('utf-8'))

    """
    Составление запроса Xpath для поиска элементов, содержащих ссылки на youtube(для youtube плееров на странице)
    Если мы находимся на Youtube ссылки являются относительные и не содержат 'youtube.com'. поэтому мы меняем Xpath запрос.
    для поиска элементов на странице содержащих 'watch'
    """

    if 'youtube.com' in url:
        xpath_string = "//*[contains(@href, 'watch')]"
    else:
        xpath_string = "//*[contains(@href, 'youtube.com')]"

    """
    Получаем все элементы на страницы, которые так или иначе содержат ссылки на видео.
    или youtube-плеера или тег <video>. Объеденяим их все в один список элементов для дальнейшего перебора.
    """

    videos = page.xpath(xpath_string)
    videos.extend(page.xpath(xpath_string.replace('@href' , '@src'))) #ссылка на ютуб может быть как в href так и в src. поэтому дополняем список всеми возможными вариантами.
    videos.extend(page.xpath('//video'))
    for video in videos:
        if url_video := video.attrib.get('href') if video.attrib.get('href') else video.attrib.get('src'): # проверяем есть ли нужные нам аттрибуты у найденных элементов.
            if 'youtube.com' in url: url_video = 'https://www.youtube.com' + url_video #ссылки на youtube относительные поэтому необходимо добавить имя домена в начале.
            download_video(url_video, PATH)


def download_video(url: str , path: str):
    """Метод загрузки видео. если мы скачиваем с youtube то используем библиотеку pytube.
    Если же мы не на youtube скачиваем напрямую с источника и записываем в файл"""

    print('загрузка видео' , url)
    try:
        if 'youtube.com' in url:
            yt = pytube.YouTube(url)
            video = yt.streams.get_highest_resolution()
            video.download(path)
        else:
            response = requests.get(url, headers = {"User-Agent": generate_user_agent()})
            with open(path+str(time.time())+'.mp4', 'wb') as f:
                f.write(response.content)
        print("видео загружено" , url)
    except:
        print('не получилось скачать видео по ссылке' , url)


if __name__ == '__main__':
    # извлекаем аргументы командной строки.
    ap = argparse.ArgumentParser()
    ap.add_argument("-u", "--url", required=True, help="ссылка на страницу")
    args = vars(ap.parse_args())
    load_page(args['url'])