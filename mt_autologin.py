from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
import pyotp
import os

# selenium模拟登录
def simulate_login(username, password, secret_key):

    # 配置options
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # 创建service
    chrome_service = Service(executable_path =r'.\chromedriver.exe')

    # 初始化webdriver
    chrome_driver = webdriver.Chrome(service = chrome_service, options = chrome_options)

    # 访问网页
    chrome_driver.get('https://ob.m-team.cc')

    # 获取网页标题
    print('网页标题:', chrome_driver.title)

    # 等待加载
    login_element_01 = WebDriverWait(chrome_driver, 10).until(
        expected_conditions.element_to_be_clickable((By.XPATH, "//span[text()='登 錄']"))
    )

    # 输入用户名
    time.sleep(1)
    username_element = chrome_driver.find_element(By.ID, 'username')
    username_element.send_keys(username)

    # 输入密码
    time.sleep(1)
    password_element = chrome_driver.find_element(By.ID, 'password')
    password_element.send_keys(password)

    # 登录
    time.sleep(1)
    login_element_01.click()

    try:

        # 等待加载
        totp_code_element = WebDriverWait(chrome_driver, 10).until(
            expected_conditions.visibility_of_element_located((By.ID, 'totpcode'))
        )

        # 输入验证码
        time.sleep(1)
        totp_code = pyotp.TOTP(secret_key).now()
        totp_code_element.send_keys(totp_code)

        # 登录
        time.sleep(1)
        login_element_02 = chrome_driver.find_element(By.XPATH, "//span[text()='登 錄']")
        login_element_02.click()

    except:
        print('未发现验证')

    try:

        # 确认通知
        confirm_element = WebDriverWait(chrome_driver, 10).until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//span[text()='確認']"))
        )
        confirm_element.click()

    except:
        print('未发现通知')

    # 关闭浏览器

    if __name__ == "__main__":
        print('登陆完成')
        user_input = input('输入q关闭浏览器:')
        if user_input == 'q':
            chrome_driver.quit()


# 获取环境变量
USERNAME = os.getenv('username')
PASSWORD = os.getenv('password')
SECRET_KEY = os.getenv('secret_key')

# 登录
simulate_login(USERNAME, PASSWORD, SECRET_KEY)
