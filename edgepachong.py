import re
import os
import urllib.request
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service as EdgeService

def extract_filename_from_url(url):
    # 使用正则表达式从 URL 中提取有效的文件名
    match = re.search(r'/([^/?]+)\?', url)
    if match:
        return match.group(1)
    else:
        return None

def download_images(img_urls, folder_path='downloaded_images'):
    # 创建文件夹
    os.makedirs(folder_path, exist_ok=True)

    for i, img_url in enumerate(img_urls):
        # 从 URL 中提取文件名
        img_filename = extract_filename_from_url(img_url)

        if img_filename:
            # 构建保存路径
            img_path = os.path.join(folder_path, f"Image_{i + 1}_{img_filename}")

            try:
                # 下载图片
                urllib.request.urlretrieve(img_url, img_path)
                print(f"Image_{i + 1} saved to {img_path}")
            except Exception as e:
                print(f"Failed to download Image_{i + 1}: {e}")

def extract_image_urls(url, wait_time=15):
    # 设置 Edge 驱动器路径，将路径替换为您本地 msedgedriver.exe 的路径
    edge_path = "D:\edge\msedgedriver.exe"
    service = EdgeService(edge_path)

    # 启动 Edge 浏览器
    driver = webdriver.Edge(service=service)

    # 打开网页
    driver.get(url)

    # 等待页面加载
    time.sleep(wait_time)  # 可以根据实际情况调整等待时间

    # 使用正则表达式匹配图片 URL
    img_pattern = re.compile(r'shop-phinf\.pstatic\.net/.*?\.(?:jpg|jpeg|png|gif)')

    # 模拟滚动窗口操作，以触发懒加载
    body = driver.find_element(By.TAG_NAME, 'body')
    for _ in range(5):  # 可以根据实际情况调整滚动次数
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)  # 等待页面加载

    # 获取页面中的所有图片元素
    img_elements = driver.find_elements(By.TAG_NAME, 'img')

    # 提取图片链接
    img_urls = [img_element.get_attribute('src') for img_element in img_elements if img_element.get_attribute('src')]

    # 过滤出匹配的图片 URL
    img_urls = [img_url for img_url in img_urls if img_pattern.search(img_url)]

    # 关闭浏览器
    driver.quit()

    return img_urls

if __name__ == "__main__":
    target_url = "https://smartstore.naver.com/ojuju/products/8549603026"
    
    # 设置等待时间为 15 秒
    image_urls = extract_image_urls(target_url, wait_time=15)

    # 打印获取到的图片 URL
    for i, img_url in enumerate(image_urls):
        print(f"Image_{i + 1}: {img_url}")

    # 下载并保存图片
    download_images(image_urls)