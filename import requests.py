import requests
import time
import os
import re

class Pictures:
    """docstring for Pictures"""
    def __init__(self, url, request=None, file_dir=None, headers=None):
        self.url = url
        if not request:
            self.requests = requests.session()
        else:
            self.requests = request
        if not file_dir:
            self.image_dir = './image/'
        else:
            self.image_dir = file_dir
        if not headers:
            self.headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip,deflate',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36'
            }
        else:
            self.headers = headers

    '''
    保存图片
    '''
    def save_image(self, url=None):
        if url is not None:
            self.url = url
        if not self.url:
            return False
        size = 0
        number = 0
        while size == 0:
            try:
                img_file = self.requests.get(url=self.url, headers=self.headers)
            except self.requests.exceptions.RequestException as e:
                raise e

            # 不是图片跳过
            if not self.check_image(img_file.headers['Content-Type']):
                return False
            file_path = self.image_path(img_file.headers)
            # 保存
            with open(file_path, 'wb') as f:
                f.write(img_file.content)
            # 判断是否正确保存图片
            size = os.path.getsize(file_path)
            if size == 0:
                os.remove(file_path)
            # 如果该图片获取超过十次则跳过
            number += 1
            if number >= 10:
                break
        return file_path if (size > 0) else False

    '''
    图片保存的路径
    '''
    def image_path(self, header):
        # 文件夹
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)
        # 文件名
        file_name = str(time.time()).replace('.', '')
        # 文件后缀
        suffix = self.img_type(header)

        return self.image_dir + file_name + suffix

    '''
    获取图片后缀名
    '''
    def img_type(self,header):
        # 获取文件属性
        image_attr = header['Content-Type']
        pattern = 'image/([a-zA-Z]+)'
        suffix = re.findall(pattern, image_attr, re.IGNORECASE)
        # 获取后缀
        if not suffix:
            suffix = 'png'
        else:
            suffix = suffix[0]
        if re.search('jpeg', suffix, re.IGNORECASE):
            suffix = 'jpg'

        return '.' + suffix

    # 检查是否为图片类型
    def check_image(self, content_type):
        if 'image' in content_type:
            return True
        else:
            return False

if __name__ == '__main__':
    image = Pictures('http://wsjd.gdhealth.net.cn:8080/gd/modules7/public/randNum.jsp?g=0.013899166096599025')
    for i in range(1000):
        image.save_image()