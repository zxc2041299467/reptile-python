import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def extract_image_urls(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
    }

    # 发送 HTTP 请求并获取网页源代码
    response = requests.get(url, headers=headers)

    # 检查请求是否成功
    if response.status_code == 200:
        # 使用 BeautifulSoup 解析 HTML 内容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 使用正则表达式匹配图片 URL
        img_pattern = re.compile(r'shop-phinf\.pstatic\.net/.*?\.(?:jpg|jpeg|png|gif)')
        img_urls = img_pattern.findall(response.text)

        # 将相对路径转换为绝对路径
        img_urls = [urljoin(url, img_url) for img_url in img_urls]

        return img_urls

    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []

if __name__ == "__main__":
    target_url = "https://brand.naver.com/vendict/products/8437484133"
    image_urls = extract_image_urls(target_url)

    # 打印获取到的图片 URL
    for i, img_url in enumerate(image_urls):
        print(f"Image_{i + 1}: {img_url}")

