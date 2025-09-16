from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common import TimeoutException
import pyotp
import os
# import json

# 定义AutoLogin类
class AutoLogin:

    def __init__(self, driver_path: str, disable_headless: bool):

        # 配置options
        browser_options = Options()

        if not disable_headless:
            browser_options.add_argument('--headless')

        browser_options.add_argument('--no-sandbox')
        browser_options.add_argument('--disable-gpu')
        browser_options.add_argument('--disable-dev-shm-usage')

        # 创建service
        browser_service = Service(executable_path = driver_path)

        # 初始化webdriver
        self.browser_driver = webdriver.Chrome(service = browser_service, options = browser_options)

    # 等待可见元素
    def wait_visible_elements(self, timeout: int, element: tuple[str,str]):
        try:
            visible_elements = WebDriverWait(self.browser_driver, timeout).until(
                expected_conditions.visibility_of_element_located(element)
            )
            return visible_elements

        except TimeoutException:
            # print('未找到可见元素')
            return False

    # 等待可点击元素
    def wait_clickable_elements(self, timeout: int, element: tuple[str,str]):
        try:
            clickable_elements = WebDriverWait(self.browser_driver, timeout).until(
                expected_conditions.element_to_be_clickable(element)
            )
            return clickable_elements

        except TimeoutException:
            # print('未找到可点击元素')
            return False

    # 获取localstorage
    # def get_local_storage(self):
    #
    #     # 初始化字典
    #     local_storage = {}
    #
    #     # 获取localstorage中的值
    #     local_storage_keys = ('auth', 'persist:user')
    #     for key in local_storage_keys:
    #         value = self.browser_driver.execute_script(f"return localStorage.getItem('{key}');")
    #
    #         # 解析json
    #         try:
    #             local_storage[key] = json.loads(value)
    #
    #         except json.JSONDecodeError:
    #             local_storage[key] = value
    #
    #     # 保存json文件
    #     with open('localstorage.json', 'w', encoding='utf-8') as f:
    #         json.dump(local_storage, f, ensure_ascii=False, indent=4)

    # 登陆验证
    def check(self) -> bool:

        check_condition_1 = self.wait_visible_elements(10, (By.XPATH, "//span[text()='歡迎回來']"))
        check_condition_2 = self.wait_clickable_elements(10, (By.XPATH, "//span[text()='退出']"))

        try:
            # 确认通知
            confirm_element = self.wait_clickable_elements(10, (By.XPATH, "//span[text()='確認']"))
            confirm_element.click()
            return True

        except Exception:
            if check_condition_1 or check_condition_2:
                print('未发现通知')
                return True
            else:
                print('登陆超时')
                return False

    # 模拟登录
    def by_simulation(self, username: str, password: str, secret_key: str):

        # 输入用户名
        username_element = self.wait_visible_elements(10, (By.ID, 'username'))
        username_element.send_keys(username)

        # 输入密码
        password_element = self.wait_visible_elements(10, (By.ID, 'password'))
        password_element.send_keys(password)

        # 登录
        login_element_01 = self.wait_visible_elements(10, (By.XPATH, "//span[text()='登 錄']"))
        login_element_01.click()

        try:
            # 输入验证码
            totp_code_element = self.wait_visible_elements(10, (By.ID, 'otpCode'))
            totp_code = pyotp.TOTP(secret_key).now()
            totp_code_element.send_keys(totp_code)

            # 登录
            login_element_02 = self.wait_clickable_elements(10, (By.XPATH, "//span[text()='登 錄']"))
            login_element_02.click()

        except Exception:
            if self.wait_clickable_elements(10, (By.XPATH, "//button[@type='button']")):
                print('未发现2fa验证')
            else:
                print('登录超时')

    # 本地存储登录
    # def by_local_storage(self):
    #
    #     # 等待加载
    #     self.wait_visible_elements(10, (By.XPATH, "//span[text()='登 錄']"))
    #
    #     # 清除localstorage
    #     self.browser_driver.execute_script("localStorage.clear();")
    #
    #     # 注入localstorage
    #     with open('localstorage.json', 'r', encoding='utf-8') as f:
    #         localstorage = json.load(f)
    #
    #     for key, value in localstorage.items():
    #         try:
    #             value = json.loads(value)
    #
    #         except TypeError:
    #             value = json.dumps(value, ensure_ascii=False)
    #         except json.JSONDecodeError:
    #             pass
    #
    #         self.browser_driver.execute_script(
    #             'localStorage.setItem(arguments[0], arguments[1]);', key, value
    #         )
    #     # 刷新
    #     self.browser_driver.refresh()

    # 关闭浏览器
    def quit(self, test: bool):
        if test:
            if input('输入q退出:') == 'q':
                self.browser_driver.quit()
        else:
            self.browser_driver.quit()

# 定义主函数
def main(test: bool = False, disable_headless: bool = False):

    # 获取环境变量
    if test:
        from tests.config import username, password, secret_key, driver_path
    else:
        username = os.getenv('USERNAME')
        password = os.getenv('PASSWORD')
        secret_key = os.getenv('SECRET_KEY')
        driver_path = os.getenv('DRIVER_PATH')

    # 初始化webdriver
    login = AutoLogin(driver_path, disable_headless)

    # 访问网页
    login.browser_driver.get('https://ob.m-team.cc')

    # 获取网页标题
    print('网页标题:', login.browser_driver.title)

    # 登录
    # '''
    # localstorage.json是否存在？
    # │
    # ├─ 是 → 本地存储登录 → 登陆检测是否通过？
    # │                       │
    # │                       ├─ 是 → 更新localstorage.json → 退出
    # │                       │
    # │                       └─ 否 → 模拟登录 → 登陆检测是否通过？
    # │                                           │
    # │                                           ├─ 是 → 更新localstorage.json → 退出
    # │                                           │
    # │                                           └─ 否 → 退出
    # │
    # └─ 否 → 模拟登录 → 登陆检测是否通过？
    #                     │
    #                     ├─ 是 → 更新localstorage.json → 退出
    #                     │
    #                     └─ 否 → 退出
    # '''
    # if os.path.isfile('./localstorage.json'):
    #     login.by_local_storage()
    #     if login.login_check():
    #         login.get_local_storage()
    #         login.quit_browser(test = True)
    #         print('本地存储登陆成功')
    #     else:
    #         login.by_simulation(username, password, secret_key)
    #         if login.login_check():
    #             login.get_local_storage()
    #             login.quit_browser(test)
    #             print('模拟登录成功')
    #         else:
    #             login.quit_browser(test)
    # else:
    #     login.by_simulation(username, password, secret_key)
    #     if login.login_check():
    #         login.get_local_storage()
    #         login.quit_browser(test)
    #         print('模拟登录成功')
    #     else:
    #         login.quit_browser(test)

    # 登录
    login.by_simulation(username, password, secret_key)
    if login.check():
        print('模拟登录成功')
        login.quit(test)
    else:
        print('模拟登录失败')
        login.quit(test)

if __name__ == '__main__':
    main(test = False, disable_headless = False)