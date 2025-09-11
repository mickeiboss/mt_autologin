from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
# import time
import pyotp
import os

# selenium模拟登录
def simulate_login(username, password, secret_key, driver_path):

    # 配置options
    browser_options = Options()
    browser_options.add_argument('--headless')
    browser_options.add_argument('--no-sandbox')
    browser_options.add_argument('--disable-gpu')
    browser_options.add_argument('--disable-dev-shm-usage')

    # 创建service
    browser_service = Service(executable_path = driver_path)

    # 初始化webdriver
    browser_driver = webdriver.Chrome(service = browser_service, options = browser_options)

    # 访问网页
    browser_driver.get('https://ob.m-team.cc')

    # 获取网页标题
    print('网页标题:', browser_driver.title)

    # 输入用户名
    username_element = WebDriverWait(browser_driver, 10).until(
        expected_conditions.visibility_of_element_located((By.ID, 'username'))
    )
    username_element.send_keys(username)

    # 输入密码
    password_element = WebDriverWait(browser_driver, 10).until(
        expected_conditions.visibility_of_element_located((By.ID, 'password'))
    )
    password_element.send_keys(password)

    # 登录
    login_element_01 = WebDriverWait(browser_driver, 10).until(
        expected_conditions.element_to_be_clickable((By.XPATH, "//span[text()='登 錄']"))
    )
    login_element_01.click()

    try:
        # 输入验证码
        totp_code = pyotp.TOTP(secret_key).now()
        totp_code_element = WebDriverWait(browser_driver, 10).until(
            expected_conditions.visibility_of_element_located((By.ID, 'otpCode'))
        )
        totp_code_element.send_keys(totp_code)

        # 登录
        login_element_02 = WebDriverWait(browser_driver, 10).until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//span[text()='登 錄']"))
        )
        login_element_02.click()

    except:
        print('未发现验证')

    try:
        # 确认通知
        confirm_element = WebDriverWait(browser_driver, 10).until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//span[text()='確認']"))
        )
        confirm_element.click()

    except:
        print('未发现通知')

    # 关闭浏览器
    # user_input = input('输入q关闭浏览器:')
    # if user_input == 'q':
        browser_driver.quit()

# 定义主函数
def main():

    # 获取环境变量
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    secret_key = os.getenv('SECRET_KEY')
    driver_path = os.getenv('DRIVER_PATH')

    # 登录
    simulate_login(username, password, secret_key, driver_path)

if __name__ == '__main__':
    main()
    print('登陆成功')
