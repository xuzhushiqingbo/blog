from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import datetime
from PIL import Image
from aip import AipOcr
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from LehuXuexi.settings import MEDIA_ROOT, YU_MING, MEDIA_URL


@require_http_methods(['GET'])
def get_select(request, city):
    opt = Options()
    opt.add_argument('--headless')
    opt.add_argument('--disable-gpu')
    wd = webdriver.Chrome(chrome_options=opt)
    # wd = webdriver.Chrome()
    wd.get("http://www.weather.com.cn/")
    wd.find_element_by_xpath('//*[@id="txtZip"]').send_keys(city)
    weather_list = {}
    time.sleep(1)
    try:
        for i in range(1, 13):
            try:
                weather_list[str(i)] = wd.find_element_by_xpath('//*[@id="show"]/ul/li[' + str(i) + ']').text
                print(weather_list[str(i)])
            except:
                print(1)
                pass
    except:
        print(2)
        pass
    wd.close()
    return JsonResponse(weather_list, safe=True, json_dumps_params={'ensure_ascii': False})


@require_http_methods(['GET'])
def get_picture(request, city, num):
    opt = Options()
    opt.add_argument('--headless')
    opt.add_argument('--disable-gpu')
    wd = webdriver.Chrome(chrome_options=opt)
    wd.get("http://www.weather.com.cn/")
    wd.find_element_by_xpath('//*[@id="txtZip"]').send_keys(city)
    time.sleep(1)
    wd.find_element_by_xpath('//*[@id="show"]/ul/li[' + num + ']').click()
    # //*[@id="show"]/ul/li[2]
    windows = wd.window_handles
    wd.switch_to.window(windows[-1])
    time.sleep(2)
    try:
        wd.find_element_by_xpath('//*[@id="someDayNav"]/li[2]').click()
    except:
        wd.find_element_by_xpath('/html/body/div[4]/div[2]/a[2]').click()
    # /html/body/div[4]/div[2]/a[2]
    now = time.time()
    picture_time = int(now * 1000)
    picture_path = wd.get_screenshot_as_file(MEDIA_ROOT + '/weather/' + str(picture_time) + '.png')
    wd.close()
    img = Image.open(MEDIA_ROOT + '/weather/' + str(picture_time) + '.png')
    cropped = img.crop((50, 300, 730, 580))
    cropped.save(MEDIA_ROOT + '/weather/' + str(picture_time) + '_cut.png')
    return HttpResponse(YU_MING + MEDIA_URL + 'weather/' + str(picture_time) + '_cut.png')


@require_http_methods(['GET'])
def search_weather(request, city_name):
    APP_ID = ''      # 输入百度api的id
    API_KEY = ''     # 输入APIKey
    SECRET_KEY = ''  # 输入SerectKey
    aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    opt = Options()
    opt.add_argument('--headless')
    opt.add_argument('--disable-gpu')
    wd = webdriver.Chrome(options=opt)
    wd.get("http://www.baidu.com")
    wd.find_element_by_xpath('//*[@id="kw"]').send_keys(city_name + "天气")
    wd.find_element_by_xpath('//*[@id="su"]').click()
    time.sleep(1)
    now = time.time()
    picture_time = int(now * 1000)
    picture_url = wd.get_screenshot_as_file(MEDIA_ROOT + '/weather/' + str(picture_time) + '.png')
    img = Image.open(MEDIA_ROOT + '/weather/' + str(picture_time) + '.png')
    cropped = img.crop((115, 166, 663, 550))
    cropped.save(MEDIA_ROOT + '/weather/' + str(picture_time) + '_cut.png')
    wd.close()
    img = Image.open(MEDIA_ROOT + '/weather/' + str(picture_time) + '_cut.png')
    cropped = img.crop((0, 0, 200, 40))
    cropped.save(MEDIA_ROOT + '/weather/' + str(picture_time) + '_test.png')
    i = open(MEDIA_ROOT + '/weather/' + str(picture_time) + '_test.png', 'rb')
    img = i.read()
    message = aipOcr.basicGeneral(img)
    try:
        message = message['words_result'][0]['words'][:6]
    except:
        message = message['words_result'][0]['words'][:-1]
    # day = datetime.datetime.now().day
    # month = datetime.datetime.now().month
    # o_day = str(day)
    # o_month = str(month)
    # if len(o_day) < 2:
    #     o_day = '0' + o_day
    # if len(o_month) < 2:
    #     o_month = '0' + o_month
    # o_string = o_month + '月' + o_day + '日'
    print(message)
    if (message[2] == '月' and message[5] == '日') or message[0:2] == city_name:
        return HttpResponse(YU_MING + MEDIA_URL + 'weather/' + str(picture_time) + '_cut.png')
    else:
        return HttpResponse(YU_MING + MEDIA_URL + 'weather/citynotexit.png')
