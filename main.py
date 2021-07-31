import os
import sys
import json
from selenium import webdriver
from selenium_stealth import stealth
import chromedriver_autoinstaller


chromedriver_autoinstaller.install()


def main():
    unpacked_extension_path = r'./widevine-l3-guesser-master.crx'
    options = webdriver.ChromeOptions()
    options.add_extension(unpacked_extension_path)
    options.add_experimental_option("prefs", {
        "download.default_directory": os.getcwd(),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    options.add_argument('--log-level=3')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options) # Why selenium ? Because.

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    driver.get(sys.argv[sys.argv.index("--url") + 1])

    with open("cookie.txt", "r") as fp:
        if len(fp.read()) > 0:
            cookies = json.load(fp)
            for cookie in cookies:
                cookie.pop('sameSite')
                driver.add_cookie(cookie)

    driver.get(sys.argv[sys.argv.index("--url") + 1])

    while not os.path.exists('keys.txt'):
        pass

    driver.quit()

    with open("keys.txt", "r") as fichier:
        print(fichier.read()[:-1])

    os.remove("keys.txt")


if __name__ == '__main__':
    main()
