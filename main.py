import base64
import requests
import os


path = os.path.abspath(os.path.dirname(__file__)) + "/pic/"


def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def ocr_image(image_path):
    # 通用识别接口
    url = 'http://localhost:6688/api/ocr/image'
    base64_string = image_to_base64(image_path)
    data = {
        "img_base64": base64_string
    }
    response = requests.post(url, json=data)
    return response.json()




# 数字识别
def ocr_image_number(image_path):
    url = 'http://localhost:6688/api/ocr/number'
    base64_string = image_to_base64(image_path)
    data = {
        "img_base64": base64_string
    }
    response = requests.post(url, json=data)
    return response.json()


# 计算识别
def ocr_image_compute(image_path):
    url = 'http://localhost:6688/api/ocr/compute'
    base64_string = image_to_base64(image_path)
    data = {
        "img_base64": base64_string
    }
    response = requests.post(url, json=data)
    return response.json()


# 字母识别
def ocr_image_alphabet(image_path):
    url = 'http://localhost:6688/api/ocr/alphabet'
    base64_string = image_to_base64(image_path)
    data = {
        "img_base64": base64_string
    }
    response = requests.post(url, json=data)
    return response.json()

# 文字点选
def ocr_image_det(image_path):
    url = 'http://localhost:6688/api/ocr/detection'
    base64_string = image_to_base64(image_path)
    data = {
        "img_base64": base64_string
    }
    response = requests.post(url, json=data)
    return response.json()

# 缺口滑块识别
def ocr_image_slider_gap(gapimg_path, fullimg_path):
    url = 'http://localhost:6688/api/ocr/slider/gap'
    gapimg_base64 = image_to_base64(gapimg_path)
    fullimg_base64 = image_to_base64(fullimg_path)
    data = {
        "gapimg_base64": gapimg_base64,
        "fullimg_base64": fullimg_base64
    }
    response = requests.post(url, json=data)
    return response.json()





# 示例调用
if __name__ == "__main__":
    
    # image_path = os.path.join(path, "1.png")
    # print(ocr_image(image_path))
    # print(ocr_image_number(image_path))
    # print(ocr_image_alphabet(image_path))
    



    # image_path = os.path.join(path, "13.png")
    # print(ocr_image_compute(image_path))
    
    
    # print(ocr_image_det(image_path))


    # gapimg_path = os.path.join(path, "12.png")
    # fullimg_path = os.path.join(path, "11.png")

    # print(ocr_image_slider_gap(gapimg_path, fullimg_path))
    # {'result': {'target_y': 10, 'target': [172, 94, 235, 130]}}


    image_path = os.path.join(path, "146.png")
    
    print(ocr_image_det(image_path))
