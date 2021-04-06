# VideoSaver

скрипт получает html страницы, сохраняет в файл, ищет все теги \<video\> на странице и встроенные youtube-плеера получает ссылку на источник видео и скачивает их в отдельную папку.

скрипт использует Selenium, поэтому должен быть установлен WebDriver Chrome. его можно скачать по ссылке: https://chromedriver.chromium.org/downloads.

установка необходимых библиотек "pip install -r requirements.txt"

запуск скрипта с аргументов -u или --url и передачей ссылки на страницу.

например:

  python video-saver.py -u https://habr.com/ru/post/232515/
  
  python video-saver.py -u https://russian.rt.com/video
  
  python video-saver.py -u https://www.youtube.com/playlist?list=PLSyWgOLbiosMENv3PgMwzxq_zk_VHJNvs
  
на этих сайтах скрипт опробован и успешно сохранил html и все видео.
