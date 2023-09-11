import re
import time
import aiohttp
import asyncio
import pyfiglet
from colorama import Fore, Style
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


YELLOW = '\033[93m'
RESET = '\033[0m'

def save_credentials(email, password):
    # Define the file path
    file_path = 'credentials.txt'

    # Open the file in append mode
    with open(file_path, 'a') as file:
        # Append the email and password
        file.write(f'{email}:{password}\n')

accounts = []
class TextStyler:
    @staticmethod
    def banner(text):
        banner_text = pyfiglet.figlet_format(text)
        styled_text = f"{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}{banner_text}{Fore.RESET}{Style.NORMAL}"
        return styled_text

    @staticmethod
    def warning(text):
        styled_text = f"{Fore.LIGHTYELLOW_EX}[!]{Fore.RESET}{Style.DIM} {text}{Fore.RESET}{Style.NORMAL}"
        return styled_text

    @staticmethod
    def success(text):
        styled_text = f"{Fore.LIGHTGREEN_EX}[+]{Fore.RESET}{Style.BRIGHT} {text}{Fore.RESET}{Style.NORMAL}"
        return styled_text

    @staticmethod
    def ask(text):
        styled_text = f"{Fore.LIGHTCYAN_EX}[?]{Fore.RESET}{Style.DIM} {text}{Fore.RESET}{Style.NORMAL}"
        return styled_text

    @staticmethod
    def process(text):
        styled_text = f"{Fore.YELLOW}[->]{Fore.RESET}{Style.DIM} {text}{Fore.RESET}{Style.NORMAL}"
        return styled_text


class TempMailGenerator:
    def _init_(self):
        self.text_styler = TextStyler
        self.email_addresses = []

    async def generate_temp_email_addresses(self, count):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for _ in range(count):
                task = self.generate_single_temp_email(session)
                tasks.append(task)
            self.email_addresses = await asyncio.gather(*tasks)

    async def generate_single_temp_email(self, session):
        api_url = "https://www.1secmail.com/api/v1/?action=genRandomMailbox"
        async with session.get(api_url) as response:
            if response.status == 200:
                data = await response.json()
                return data[0]
            else:
                print(self.text_styler.warning(f"Error: {response.status} - {await response.text()}"))
                return None

    async def check_mail(self, email):
        login, domain = email.split('@')
        api_url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}"
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status == 200:
                    messages = await response.json()
                    return messages
                else:
                    print(self.text_styler.warning(f"Error: {response.status} - {await response.text()}"))
                    return None

    async def run(self, num_emails):
        await self.generate_temp_email_addresses(num_emails)
        if self.email_addresses:
            print("Generating Emails")
            for email in self.email_addresses:
                print((email) + " is processing....")
                # mail
                mail = email

                # Set the wait time (in seconds)
                wait_time = 10

                # Create ChromeOptions object
                options = webdriver.ChromeOptions()

                # Set the browser to run in headless mode (without opening a GUI)
                options.add_argument('--headless')
                options.add_argument('--start-maximized')
                options.add_argument('--disable-extensions')
                options.add_argument('--disable-software-rasterizer')
                options.add_argument('--disable-accelerated-2d-canvas')
                options.add_argument('--disable-accelerated-jpeg-decoding')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--disable-infobars')
                options.add_argument('--disable-notifications')
                options.add_argument('--incognito')
                # Initialize the WebDriver with the path and options
                driver = webdriver.Chrome(options=options)

                # Navigate to a website
                driver.get("https://www.syncedthegame.com/en/")
                cookie = WebDriverWait(driver, wait_time).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div/div[2]/div/button[2]"))
                )
                cookie.click()

                try:
                    cookie = WebDriverWait(driver, wait_time).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div/div[2]/div/button[2]"))
                    )
                    cookie.click()
                    # Wait until the element is present before attempting to interact with it
                    log_in = WebDriverWait(driver, wait_time).until(
                        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[3]"))
                    )
                    log_in.click()
                    print(f"Register Clicked")
                    register_now = WebDriverWait(driver, wait_time).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "/html/body/div[3]/div/div[2]/div/div/div/div/div/div[3]/div/span"))
                    )
                    register_now.click()

                    email_input = WebDriverWait(driver, wait_time).until(
                        EC.presence_of_element_located((By.XPATH,
                                                        "/html/body/div[3]/div/div[2]/div/div/div/div/div/form/div/div/div/div/div[1]/div/div/div[1]/div/div[3]/div/div/div/div/span/input"))
                    )
                    email_input.click()
                    email_input.send_keys(mail)
                    print("Email Entered")

                    send = WebDriverWait(driver, wait_time).until(
                        EC.presence_of_element_located((By.XPATH,
                                                        "/html/body/div[3]/div/div[2]/div/div/div/div/div/form/div/div/div/div/div[1]/div/div/div[1]/div/div[4]/div/div/div/div/span/span/div/div"))
                    )
                    send.click()
                    time.sleep(1)
                    code_input = WebDriverWait(driver, wait_time).until(
                        EC.presence_of_element_located((By.XPATH,
                                                        "/html/body/div[3]/div/div[2]/div/div/div/div/div/form/div/div/div/div/div[1]/div/div/div[1]/div/div[4]/div/div/div/div/span/input"))
                    )
                    code_num = ""
                    messages = []
                    while not messages:
                        time.sleep(5)
                        messages = await self.check_mail(email)
                        if messages:
                            code_num = re.search(r'\b\d{5}\b', messages[0]['subject']).group()
                        else:
                            print(self.text_styler.warning(f"No messages for {email}"))
                    code_input.click()
                    code_input.send_keys(code_num)
                    print("CODE Entered")
                    time.sleep(2)
                    # Wait for an element to be visible
                    region = WebDriverWait(driver, wait_time).until(
                        EC.visibility_of_element_located((By.XPATH,
                                                          "/html/body/div[3]/div/div[2]/div/div/div/div/div/form/div/div/div/div/div[1]/div/div/div[1]/div/div[5]/div/form/div/div/div/div/div/div/div/div/span[1]/input"))
                    )
                    region.click()
                    region.send_keys("Poland")
                    region.send_keys(Keys.RETURN)
                    print(f"Region selected Poland")
                    time.sleep(1)
                    check_box = WebDriverWait(driver, wait_time).until(
                        EC.visibility_of_element_located((By.XPATH,
                                                          "/html/body/div[3]/div/div[2]/div/div/div/div/div/form/div/div/div/div/div[1]/div/div/div[1]/div/form/div/div/label/span[2]/span"))
                    )
                    check_box.click()
                    print("T&C Agreed")

                    continue_but = WebDriverWait(driver, wait_time).until(
                        EC.visibility_of_element_located((By.XPATH,
                                                          "/html/body/div[3]/div/div[2]/div/div/div/div/div/form/div/div/div/div/div[1]/div/div/div[2]/button"))
                    )
                    continue_but.click()
                    time.sleep(1)

                    password = WebDriverWait(driver, wait_time).until(
                        EC.visibility_of_element_located((By.XPATH,
                                                          "/html/body/div[3]/div/div[2]/div/div/div/div/div/form/div/div/div/div/div[2]/div/div/div[1]/div[2]/div[1]/div/div[1]/div/span/input"))
                    )
                    password.send_keys("ajrockey0288")
                    password.send_keys(Keys.RETURN)

                    con_password = WebDriverWait(driver, wait_time).until(
                        EC.visibility_of_element_located((By.XPATH,
                                                          "/html/body/div[3]/div/div[2]/div/div/div/div/div/form/div/div/div/div/div[2]/div/div/div[1]/div[4]/div[1]/div/div[1]/div/span/input"))
                    )
                    con_password.click()
                    con_password.send_keys("ajrockey0288")
                    print("Password Confirmed")

                    done = WebDriverWait(driver, wait_time).until(
                        EC.visibility_of_element_located((By.XPATH,
                                                          "/html/body/div[3]/div/div[2]/div/div/div/div/div/form/div/div/div/div/div[2]/div/div/div[2]/button"))
                    )
                    done.click()
                    time.sleep(3)
                    save_credentials(mail, password="ajrockey0288")


                except Exception as e:
                    driver.quit()
                    print(f"An error occurred: {e}")

                # Do other actions as needed

                finally:
                    # Close the WebDriver
                    driver.quit()
                    print(f"Account with {email} Created Succefully")
            print(f"{num_emails} emails made and stored in credentials.txt")


if  __name__ == "__main__":
    print(TextStyler.banner("Bishop's Genrator"))
    styler = TextStyler()
    num_emails = int(input("Enter the amounts of account you want to create: "))
    start_time = time.time()
    email_manager = TempMailGenerator()
    asyncio.run(email_manager.run(num_emails))
    end_time = time.time()
    elapsed_time = end_time-start_time
    print(f"The code took {elapsed_time} seconds to execute.")