

# import random
# from playwright.sync_api import sync_playwright
# import requests
# import time


# # result = {'target_y': 10, 'target': [172, 94, 235, 130]}

# def request_image_location(gapimg_base64, fullimg_base64):

#     url = 'http://localhost:6688/api/ocr/slider/gap'

#     data = {
#         "gapimg_base64": gapimg_base64.replace("data:image/png;base64,", ""),
#         "fullimg_base64": fullimg_base64.replace("data:image/png;base64,", "")
#     }
#     response = requests.post(url, json=data)
    
#     return response.json()

# def generate_track(distance, steps):
#     track = []
#     current = 0
#     for _ in range(steps):
#         # 模拟缓动效果，步长逐渐减小
#         delta = (distance - current) * random.uniform(0.3, 0.6)
#         current += delta
#         track.append(delta)
#     return track



# with sync_playwright() as p:
#     # 启动浏览器
#     browser = p.chromium.launch(headless=False)  # 设置为 False 以便观察滑动过程
#     context = browser.new_context()
#     page = context.new_page()

#     # 打开目标页面
#     page.goto("https://txzbqy.miit.gov.cn/#/gateway/list")  # 替换为实际的滑块验证码页面

    
#     # 点击span标签
#     page.click("span[data-v-3206d594='']")

#     # 等待3s滑块出现
#     page.wait_for_timeout(3000)

#     # 获取滑块和背景图片
#     full_img = page.query_selector("img[class='slide-canvas']").get_attribute("src")
#     gap_img = page.query_selector("img[class='slide-block']").get_attribute("src")

    
#     # 调用自定义函数计算滑块距离
#     res = request_image_location(gap_img, full_img)
#     x = res['result']['target'][0]  # 滑块需要移动的距离
#     print(f"滑块需要移动的距离: {x}")


#     # 滑块按钮
#     slider = page.query_selector("div[id='slider-button2']")


#     # 模拟滑动操作
#     box = slider.bounding_box()  # 获取滑块的位置信息
#     if box:
#         start_x = box['x'] + box['width'] / 2  # 滑块中心点
#         start_y = box['y'] + box['height'] / 2
#         page.mouse.move(start_x, start_y)  # 移动鼠标到滑块
#         page.mouse.down()  # 按下鼠标

#         # 生成滑动轨迹
#         track = generate_track(x, steps=100)
#         current_x = start_x
#         for delta in track:
#             current_x += delta
#             page.mouse.move(current_x, start_y, steps=1)  # 按轨迹移动
           
#         page.mouse.up()  # 松开鼠标

#     # 等待3s查看结果
#     page.wait_for_timeout(3000)

#     # 截图
#     page.screenshot(path="example.png")

#     # 关闭浏览器
#     browser.close()



import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64



def request_image_location(gapimg_base64, fullimg_base64):

    url = 'http://localhost:6688/api/ocr/slider/gap'

    data = {
        "gapimg_base64": gapimg_base64.replace("data:image/png;base64,", ""),
        "fullimg_base64": fullimg_base64.replace("data:image/png;base64,", "")
    }
    response = requests.post(url, json=data)
    
    return response.json()['result']['target'][0]

def aes_encrypt(t, e):
    # 将输入的 t 和 e 转换为字节
    key = t.encode('utf-8')  # 相当于 l.a.enc.Utf8.parse(t)
    data = e.encode('utf-8')  # 相当于 l.a.enc.Utf8.parse(e)

    # 创建 AES 加密器（ECB 模式）
    cipher = AES.new(key, AES.MODE_ECB)

    # PKCS7 填充并加密
    encrypted = cipher.encrypt(pad(data, AES.block_size))

    # 转换为 Base64 字符串
    return base64.b64encode(encrypted).decode('utf-8')

def aes_decrypt(e, t):
    """
    使用 AES 解密（ECB 模式，PKCS7 填充）
    :param e: 加密后的 Base64 字符串
    :param t: 密钥（字符串，长度必须为 16/24/32 字节）
    :return: 解密后的明文字符串
    """
    # 将密钥转换为字节
    key = t.encode('utf-8')
    
    # 将加密的 Base64 字符串解码为字节
    encrypted_data = base64.b64decode(e)
    
    # 创建 AES 解密器（ECB 模式）
    cipher = AES.new(key, AES.MODE_ECB)
    
    # 解密并去除填充
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    
    # 返回解密后的明文字符串
    return decrypted_data.decode('utf-8')

def get_param():

    url = 'https://txzbqy.miit.gov.cn/zbtb/captcha/slideCaptcha'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Content-Type': 'application/json;charset=UTF-8'
    }
    data = {
        "canvasWidth": 320,
        "canvasHeight": 155,
        "blockWidth": "65",
        "blockHeight": "55",
        "blockRadius": 10
    }
    response = requests.post(url, json=data, headers=headers)
    
    gapimg_base64 = response.json()['data']['blockSrc']
    fullimg = response.json()['data']['canvasSrc']
    key  = response.json()['data']['nonceStr']
    fullimg_base64 = aes_decrypt(fullimg, key)


    silde_date =  request_image_location(gapimg_base64, fullimg_base64) 

    return silde_date, key

def get_list(token, code):
        
    list_url = 'https://txzbqy.miit.gov.cn/zbtb/gateway/gatewayPublicity/bidBulletinList'
    list_headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '394',
        'Content-Type': 'application/json;charset=UTF-8',
        'Host': 'txzbqy.miit.gov.cn',
        'Origin': 'https://txzbqy.miit.gov.cn',
        'Pragma': 'no-cache',
        'Referer': 'https://txzbqy.miit.gov.cn/',
        'Sec-CH-UA': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        'Sec-CH-UA-Mobile': '?0',
        'Sec-CH-UA-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
        }
    list_data = {
            "resource": "",
            "page": 1,
            "limit": 15,
            "totalSize": 0,
            "bulletinTitle": "",
            "issueDate": "",
            "status": "11",
            "bulletinType": "22",
            "unitRestrict": [],
            "supervisorName": [],
            "nationFlag": None,
            "bidType": None,
            "bidSubtype": None,
            "fileBuyBeginTime": "",
            "fileBuyEndTime": "",
            "occupationBeginDate": "",
            "occupationEndDate": "",
            "issueDates": [],
            "gatewayFlag": 0,
            "code": code,
            "token": token
        }
    response = requests.post(list_url, json=list_data, headers=list_headers)

    return response.json()



if __name__ == '__main__':

    silde_date, token = get_param()

    print(silde_date, token)

    code = aes_encrypt(token, str(silde_date))

    print(code)

    res = get_list(token, code)

    print(res)  




    

#     {'msg': 'success', 'code': 0, 'page': {'totalCount': 113924, 'pageSize': 15, 'totalPage': 7595, 'currPage': 1, 'list': [{'issueDate': 1743170515684, 'bulletinTitle': '中国移动（宁夏中卫）数据中心四期2-2号楼机电工程总承包采购项目
# _招标公告', 'uuid': '188a0d639622421f8eae54d6903f24a3', 'frequency': 0}, {'issueDate': 1743168732535, 'bulletinTitle': '2025年天津联通UPS电源设备集中采购项目（二次招标）公告', 'uuid': '1d29f6b057014340be78ce3e34d0f124', 'frequency': 0}, {'issueDate': 1743168094738, 'bulletinTitle': '中国移动通信集团广东有限公司2025年政企项目（01号）相关软硬
# 件公开招标采购项目_招标公告', 'uuid': 'abacc196ded54ade99b01d710c0ef530', 'frequency': 0}, {'issueDate': 1743167575154, 'bulletinTitle': '2025年中国联通乌鲁木齐天津路核心局房动力配套改造工程油机系统改造施工采购项目招标公告', 'uuid': '5dc9ee22f522b153a7d6fed077a9bb98', 'frequency': 0}, {'issueDate': 1743167504244, 'bulletinTitle': '重庆铁塔-2025-2027年塔类土建、配套、外市电施工服务（YT、ZL、NY）招标公告', 'uuid': '67f93b6866230f8d3fa239228624ac44', 'fre2025-2027年塔类土建、配套、外市电施工服务（YT、ZL、NY）招标公告', 'uuid': '67f93b6866230f8d3fa239228624ac44', 'frequency': 0}, {'issueDate': 1743165659917, 'bulletinTitle': '中国电信北京公司2025年外市电引入及变配电工程设计施工一
# 体化集中公开招标项目招标公告', 'uuid': '2b44a8af62950f1ef163639a87b58aff', 'frequency': 0}, {'issueDate': 174316472025-2027年塔类土建、配套、外市电施工服务（YT、ZL、NY）招标公告', 'uuid': '67f93b6866230f8d3fa239228624ac44', 'frequency': 0}, {'issueDate': 1743165659917, 'bulletinTitle': '中国电信北京公司2025年外市电引入及变配电工程设计施工一
# 2025-2027年塔类土建、配套、外市电施工服务（YT、ZL、NY）招标公告', 'uuid': '67f93b6866230f8d3fa239228624ac44', 'fre2025-2027年塔类土建、配套、外市电施工服务（YT、ZL、NY）招标公告', 'uuid': '67f93b6866230f8d3fa239228624ac44', 'frequency': 0}, {'issueDate': 1743165659917, 'bulletinTitle': '中国电信北京公司2025年外市电引入及变配电工程设计施工一
# 体化集中公开招标项目招标公告', 'uuid': '2b44a8af62950f1ef163639a87b58aff', 'frequency': 0}, {'issueDate': 1743164725416, 'bulletinTitle': '中国移动通信集团广西有限公司南宁分公司2025年教育城域网一阶段工程安全系统采购项目_招标公告
# ', 'uuid': 'a25dd9450aef427399ed361d2655b0ee', 'frequency': 0}, {'issueDate': 1743163527161, 'bulletinTitle': '中 
# 国移动四川公司2025年全网通机载基站购置项目_招标公告', 'uuid': '9b1d32b3650e4233a4d701e67cd86985', 'frequency': 0}, {'issueDate': 1743162704046, 'bulletinTitle': '2025-2026年河北联通光缆分纤箱、光缆终端盒采购测试公告（变更）', 'uuid': '9bf4492a4af245c2b3a3d786787db5b7', 'frequency': 0}, {'issueDate': 1743161406289, 'bulletinTitle': '2025年铁
# 塔能源昌吉州重点区域光伏施工采购项目招标公告', 'uuid': '849594bd53c6405e8df995e29175ef6d', 'frequency': 0}, {'issueDate': 1743158028248, 'bulletinTitle': '中国电信郑州分公司2025年港区IDC机房出局及荆州路等道路管道购置项目重新招标
# 招标公告', 'uuid': '84c484d0bb864b6da00379f64fc43c5b', 'frequency': 0}, {'issueDate': 1743157715715, 'bulletinTitle': '2025-2027年天津联通移动网多模微室分系统公开招标采购项目公告', 'uuid': 'cc638a10802b19ef9a00f8299a98944a', 'frequency': 0}, {'issueDate': 1743157701162, 'bulletinTitle': '2025年深圳联通无线网络系统集成服务项目招标公告', 'uuid': '83bb78c8d11a9e471926cb59d2177914', 'frequency': 0}, {'issueDate': 1743157314166, 'bulletinTitle': '中国移动通
# 信集团甘肃有限公司2025年至2027年全省数据中心与通信枢纽、汇聚机房、自有基站、室分站点市电引入及高（低）压配电系统可
# 研和设计采购项目_招标公告', 'uuid': '38550320f2a64ae0b2f547b395023ee7', 'frequency': 0}, {'issueDate': 1743155996968, 'bulletinTitle': '2025年联通数科通用服务器集中采购项目招标公告', 'uuid': '2873027d04dbc608ae008cd8012fa4f3', 'frequency': 0}]}}