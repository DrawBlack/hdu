import base64
from io import BytesIO
import hashlib
from PIL import Image
from lxml import etree
import requests
import json

host = 'http://jisuyzmsb.market.alicloudapi.com'
path = '/captcha/recognize'
method = 'POST'
querys = 'type=n5'
bodys = {}
url = host + path + '?' + querys

example_base64 = 'iVBORw0KGgoAAAANSUhEUgAAADwAAAAWCAIAAAATqWh1AAAABnRSTlMAZgAAAAB41IV8AAAEaElEQVR4nNWXQZrrKAyE//TXp4HZVV+FHIEco/2OYY4QruJa4utkFmB3OnHyvVkOC+JgIaRCKsmn5boQofE/mk9LWxTE0yhrUZOj91npQOxw9L27fKlFUW5+Mx/acDhczXydb0djuS6PK22Zr/OrucvMbX7e+F/HK5N2M34hvUOSU/bq994/CHg1DYBIB49GvyIivySr31za+7fdyNNyXZ6FugX7kTQOFbl6j7Pu6hsP96B0tNChzrKWHF4q2VV9Eg/8U9PpbBCQJ3JyqagfubpMMhaQlBmg5pRdy+U8NDPl5ftOYRAB1nLpapty2qBZiycPsetC+EH0GIXGh5sBJbmOnayczhYCBGWiVClCsyuXaayDqC5VNBMp526xASEmf539cFyZ7O5Ss2tREBRPw2DA56+y4mqvr+8t8qE48FBSWQtQzgZ05XZTTv0QuZkoV4Q1sdzyfLUR1U6ZhiuApjw35Qmwqi/VrvZaSrXrxRV1t4AosP/0a5nn25wnAE9F6R2ZuPljZE9PrCZXlwZIsXtCBk8mioqxkQJlNWjGIFYUhylK0CAhZBAmopBzwufuPwI2jnMzKH/L1YQsoPrxgn4PRX0QKbW4WkFKUhRIWGFIeA+GxHLLt5tykpqBS1fTimG+am5ST6+Ke5ykrCBXu7oAk/IWCQDr0L1l1GbuuuFYj+xvfPYcuoffXdFqNxQRFCBApWeJq4kqsefitr0nUABcJoScRFeSuJysqDnpMtk4Dz0d+tw5QCmLy25mWV8kYuSTiKsdURsxsDukaNqGSrUx6+AsR4zAeeo+2E1dvpyLN9rpOXr5xyC+NZJ+hzB4wDQIcRjs5ico70Bt/qBZSTnI/Ip9JY27Y2SPotwg2rELW1ep2RFapxfKeVzUfMs5SClToeFJmcGqQ1VE9CM0InM/O4no49gARX0S1aHqHEdA2BsYXZEhAzinfPmnx6vmW+6xri02NkZjezWgMdJULj0vQXCJX/m6ED24ZIUAof+RqpUygbI6P9NI48OjnqkTjZLmJKCgnDQwTr2yqJyLG6Dc9KDMf0qpAHPLrOUHp8bOcvuTkGsh5JwEna+gb0k/lTIHuZZHo4+7vOrTWdpyWaAJJWfyV/RA7s4OXTVHLnGnqp+Amm+Z6r33cC2jCNzm3HO9/pTDoa0tOdwv9JTzXt5LLR+0p9BJul35sbhp/lYOuWxOby72XynKdSt1vRz2dVyqjyvFiqtpKOU85V2bro8WA0rKIe9Xp6iX/TTPfdwdZu/HfSNFwxGNIBwNDBEYhKOQO3v8Zb/uelcRn9892hfxa2Gv3uZCb1QiP9QUvXEo4znknKSQ6e1UfFFKnserL5fDpta1MLrke+RMk5J6L95VldX6BbP1RLpb94saZrRHfwO5q0/zdX6gcdfi2AlY6rkfj9vfPkq1IgraNv7tRe/WK+i+g3//defVp6Ut9/3+r7DrpaRJdx8jRLPp7WHwAD/D27He5Z+C20LjFRs6d5IHnz9sLuF/AYr1AhGdzQ8qAAAAAElFTkSuQmCC'
example_appcode = '45fbfd16abe04372ac45479aed31b5cb'

# 学号
username = ''
# 密码
password = ''
# 年级
nj = ''
#行政班
hidXZB = ''


def getCode(pic, appcode):
    bodys['pic'] = pic
    headers = {'Authorization': 'APPCODE ' + appcode,
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    r = requests.post(url, bodys, headers=headers)
    data = json.loads(r.text)
    return data['result']['code']


def md5(str):
    m = hashlib.md5(str.encode("utf-8"))
    return m.hexdigest()


# 获取请求参数中的lt
def getLT():
    lt_url = 'http://cas.hdu.edu.cn/cas/login?service=http%3A%2F%2Fi.hdu.edu.cn%2Fdcp%2Findex.jsp'
    r = requests.get(lt_url)
    html_text = r.text
    html_tree = etree.HTML(html_text)
    print('LT')
    return html_tree.xpath('//*[@id="login_form"]/div/div[1]/input[2]')[0].get('value')


def getValueByXpath(html_text, xpath, ele_type):
    html_tree = etree.HTML(html_text)
    return html_tree.xpath(xpath)[0].get(ele_type)


def getAllByXpath(html_text, xpath):
    html_tree = etree.HTML(html_text)
    return html_tree.xpath(xpath)


def getCookie():
    url = 'http://cas.hdu.edu.cn/cas/login'
    payload = {'encodedService': 'http://i.hdu.edu.cn/dcp/index.jsp', 'service': 'http://jxgl.hdu.edu.cn/default.aspx',
               'serviceName': '', 'loginErrCnt': '0', 'username': username, 'password': md5(password), 'lt': getLT()}

    # 获取登陆ticket
    r = requests.post(url, data=payload)
    ticket_xpath = '/html/body/noscript/p/a'
    url_ticket = getValueByXpath(r.text, ticket_xpath, 'href')

    # 获取选课页面的cookie，后面的选课请求都会在header中设置cookie，没有cookie将无法登陆选课页面和选课操作
    next = requests.get(url_ticket)
    cookie = str(next.headers.get('Set-Cookie'))
    print(cookie)
    return cookie


def getParams(headers, xh, nj):
    select_class_by_kzy = 'http://jxgl.hdu.edu.cn/zylb.aspx?xh=' + username + '&nj=' + nj
    mianban = requests.get(select_class_by_kzy, headers=headers)

    view_state_xpath = '//*[@id="__VIEWSTATE"]'
    event_validation_xpath = '//*[@id="__EVENTVALIDATION"]'

    view_state = getValueByXpath(mianban.text, view_state_xpath, 'value')
    view_validation = getValueByXpath(mianban.text, event_validation_xpath, 'value')
    query_class_by_num_payload = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '_LASTFOCUS': '',
        '__VIEWSTATE': view_state,
        '__EVENTVALIDATION': view_validation,
        'cx': 'cx',
        'DropDownList2': '01',
        'TextBox1': xh,
        'RadioButtonList1': '3',
        'Button3': '%C8%B7%B6%A8',
        'DropDownList1': nj
    }
    print(query_class_by_num_payload)
    return query_class_by_num_payload


def select_class(xh):
    headers = {'Cookie': getCookie()}
    query_class_by_num_payload = getParams(headers, xh, nj)
    select_class_by_kzy = 'http://jxgl.hdu.edu.cn/zylb.aspx?xh=' + username + '&nj=' + nj
    class_info = requests.post(select_class_by_kzy, data=query_class_by_num_payload, headers=headers)
    class_with_teachers_urltext = getValueByXpath(class_info.text, '//a', 'onclick')

    strs = str(class_with_teachers_urltext).split(',')
    print(strs[0])
    start = int(strs[0].find('(') + 2)
    end = int(strs[0].find(')'))
    class_with_teachers_url = strs[0][start:end]

    class_with_teachers_detail = requests.get('http://jxgl.hdu.edu.cn/' + class_with_teachers_url,
                                              headers=headers)

    # 识别验证码
    yz_code_img_url = 'http://jxgl.hdu.edu.cn/CheckCode.aspx'
    img_response = requests.get(yz_code_img_url, headers=headers)
    img = Image.open(BytesIO(img_response.content))
    # 转换成RGB模式
    img = img.convert('RGB')
    img.save('out.jpg')

    f = open('out.jpg', 'rb')  # 二进制方式打开图文件
    img_base64 = str(base64.b64encode(f.read()))  # 读取文件内容，转换为base64编码
    f.close()
    img_base64 = img_base64[2:-1]
    img_code = getCode(img_base64, example_appcode)  # 识别出来的验证码
    print(img_code)

    # 获取选课课号(默认第一个)
    inputs = getAllByXpath(class_with_teachers_detail.text, '//input')
    xkkh = inputs[0].get('value')
    hidZYDM = inputs[8].get('value')

    select_class_params = {'__EVENTTARGET': 'Button1',
                           '__EVENTARGUMENT': '',
                           '__VIEWSTATE': '/wEPDwULLTEzMDk5NDU3NTEPFgweAnhtBQbmsarmnbAeAnh5BQ'
                                          '/orqHnrpfmnLrlrabpmaIeBHp5bWMFDOi9r'
                                          '+S7tuW3peeoix4FZHFzemoFBDIwMTUeA3h6YgUIMTUwNTI3MTIeBHp5ZG0FBDA1MjcWAmYPZBYCAgMPEGRkFgBkZA==',
                           '__EVENTVALIDATION': '/wEWDQKXyNPgBQKS+9acCwL444i9AQLn44i9AQL3jKLTDQLax9vVBgKM54rGBgKF2fXbAwLWlM+bAgK7q7GGCALejczkBgKgpuLGBALujYy8Bg==',

                           'xkkh': xkkh, 'txtYz': img_code,
                           'RadioButtonList1': '0',
                           'hidNJ': nj, 'hidZYDM': hidZYDM, 'hidXZB': hidXZB}

    select_result = requests.post(
        'http://jxgl.hdu.edu.cn/' + class_with_teachers_url,
        data=select_class_params, headers=headers)

    print(select_result.text)


# 要选的课程代码
xh = 'B0502670'
select_class(xh)
