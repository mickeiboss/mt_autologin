import os
import sys

import pyotp
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


# 定义AutoLogin类
class AutoLogin:

    def __init__(self, driver_path: str, user_data_dir: str, headless: bool = True):

        # 生成useragent
        ua = UserAgent(browsers = 'Chrome')

        # 配置options
        options = Options()

        if headless:
            options.add_argument('--headless') # 启用无头浏览器

        options.add_argument('--no-sandbox') # 禁用沙盒
        options.add_argument('--disable-gpu') # 禁用gpu
        options.add_argument('--disable-dev-shm-usage') # 禁用共享内存
        options.add_argument(f'--user-agent={ua.random}') # 设置useragent
        options.add_argument(f'--user-data-dir={user_data_dir}') # 设置用户数据目录
        options.add_argument('--disable-blink-features=AutomationControlled') # 隐藏警告
        options.add_experimental_option('excludeSwitches', ['enable-automation']) # 移除enable-automation
        options.add_experimental_option('useAutomationExtension', False) # 禁用selenium扩展
        options.add_experimental_option('prefs', {'profile.password_manager_enabled': False}) # 禁用密码管理器

        # 创建service
        service = Service(executable_path = driver_path)

        # 初始化webdriver
        self.driver = webdriver.Chrome(service = service, options = options)
        self.driver.execute_cdp_cmd(
            'Page.addScriptToEvaluateOnNewDocument',
            {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'}
        )

    # 等待可见元素
    def wait_visible_elements(self, timeout: int, element: tuple[str,str]) -> WebElement | TimeoutException:

        try:
            visible_elements = WebDriverWait(driver = self.driver, timeout = timeout).until(
                method = expected_conditions.visibility_of_element_located(locator = element)
            )

        except TimeoutException:
            raise TimeoutException

        else:
            return visible_elements

    # 等待可点击元素
    def wait_clickable_elements(self, timeout: int, element: tuple[str,str]) -> WebElement | TimeoutException:

        try:
            clickable_elements = WebDriverWait(driver = self.driver, timeout = timeout).until(
                method = expected_conditions.element_to_be_clickable(mark = element)
            )

        except TimeoutException:
            raise TimeoutException

        else:
            return clickable_elements

    # 登陆验证并确认通知
    def check(self) -> bool:

        # 登陆验证
        try:
            self.wait_visible_elements(10, (By.XPATH, '//span[text()="歡迎回來"]'))
            self.wait_visible_elements(10, (By.XPATH, '//span[text()="退出"]'))

        except TimeoutException:
            print('登录超时')
            return False

        else:
            # 确认通知
            try:
                confirm_button = self.wait_clickable_elements(10, (By.XPATH, '//span[text()="確認"]'))

            except TimeoutException:
                print('未发现通知')

            else:
                confirm_button.click()

            finally:
                return True

    # 通过模拟操作登录
    def by_simulation(self, username: str, password: str, secret_key: str):

    # 输入用户名和密码
        try:
            username_input = self.wait_clickable_elements(10, (By.ID, 'username'))
            password_input = self.wait_clickable_elements(10, (By.ID, 'password'))
            login_button_01 = self.wait_clickable_elements(10, (By.XPATH, '//span[text()="登 錄"]'))

        except TimeoutException:
            pass

        else:
            username_input.send_keys(username)
            password_input.send_keys(password)
            login_button_01.click()

        # 验证
        try:
            error_01 = self.wait_visible_elements(3, (By.XPATH, '//div[@class="ant-message-notice-content"]'))

        except TimeoutException:
            pass

        else:
            print(error_01.text)

        # 输入totp验证码
        try:
            totp_code_option = self.wait_clickable_elements(10, (By.ID, 'rc-tabs-0-tab-otp'))
            totp_code_input = self.wait_clickable_elements(10, (By.ID, 'otpCode'))
            login_button_02 = self.wait_clickable_elements(10, (By.XPATH, '//span[text()="登 錄"]'))

        except TimeoutException:
            print('未发现2fa验证')

        else:
            totp_code_option.click()
            totp_code = pyotp.TOTP(secret_key).now()
            totp_code_input.send_keys(totp_code)
            login_button_02.click()

        # 验证
        try:
            error_02 = self.wait_visible_elements(3, (By.XPATH, '//div[@class="ant-message-notice-content"]'))

        except TimeoutException:
            pass

        else:
            print(error_02.text)

    # 关闭浏览器
    def quit(self):
        self.driver.quit()

# 定义主函数
def main():

    # 检查并生成用户数据目录
    # 获取当前脚本所在目录（绝对路径）
    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

    # 在脚本同级目录下创建一个名为 "chrome_profile" 的目录
    user_data_dir = os.path.join(script_dir, "user_data")

    # 创建目录（如果不存在），并确保权限
    os.makedirs(user_data_dir, exist_ok=True)

    # 初始化webdriver
    driver_path = os.getenv('DRIVER_PATH')
    login = AutoLogin(driver_path = driver_path, user_data_dir = user_data_dir)

    # 访问网页
    login.driver.get('https://ob.m-team.cc')

    # 获取网页标题
    print('网页标题:', login.driver.title)

    # 登录
    if login.check():
        pass

    else:
        username = os.getenv('MT_USERNAME')
        password = os.getenv('MT_PASSWORD')
        secret_key = os.getenv('MT_SECRET_KEY')
        login.by_simulation(username, password, secret_key)
        login.check()

    login.quit()


if __name__ == '__main__':
    main()