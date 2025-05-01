import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class FooterTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.base_url = "https://only.digital/"
        self.wait = WebDriverWait(self.driver, 10) # Ждем, пока загрузится страница

    # Принимаем куки, чтобы баннер не закрывал элементы сайта
    def accept_cookies(self):
        try:
            cookie_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Принять') or contains(., 'Окей')]"))
            )
            cookie_btn.click()
            print("✔ Куки приняты")
        except TimeoutException:
            print("✘ Баннер куки не найден")

    def scroll_to_footer(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            footer = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "footer")))
            print("✔ Футер обнаружен на странице")
            return footer
        except TimeoutException:
            print("✘ Футер не найден на странице")
            return None

    def check_footer_elements(self):
        elements = {
            "Копирайт": "//footer//*[contains(., '©') or contains(., 'Copyright')]",  # Обязательный элемент
            "Логотип": "//footer//img[contains(@src, 'logo')] | //footer//*[contains(@class, 'logo')]",
            "Контакты": "//footer//*[contains(., '@') or contains(., 'тел') or contains(., 'phone')]",
            "Соцсети": "//footer//a[contains(@href, 'telegram') or contains(@href, 'vk') or contains(@href, 'social')]",
            "Годы работы": "//footer//*[contains(., '2014') or contains(., '2025')]"
        }

        results = {}
        for name, locator in elements.items():
            try:
                element = self.wait.until(EC.presence_of_element_located((By.XPATH, locator)))
                results[name] = "✔ Найден"
                if name == "Копирайт":
                    print(f"Текст копирайта: {element.text.strip()}")
            except TimeoutException:
                results[name] = "✘ Не найден"
                if name == "Копирайт":
                    print("✘ Копирайт не найден!")

        return results

    def test_footer(self):
        print("\n=== Начало тестирования футера ===")
        self.driver.get(self.base_url)
        self.accept_cookies()
        footer = self.scroll_to_footer()

        if footer:
            results = self.check_footer_elements()
            print("\nРезультаты проверки элементов:")
            for name, status in results.items():
                print(f"{name}: {status}")

            # Проверяем обязательное условие - наличие копирайта
            if results["Копирайт"] == "✔ Найден":
                print("\nТест пройден: обязательный элемент (копирайт) присутствует")
                # Дополнительно проверяем другие элементы
                found_elements = sum(1 for status in results.values() if status == "✔ Найден")
                print(f"Найдено элементов: {found_elements} из {len(results)}")
            else:
                print("\nТест не пройден: обязательный элемент (копирайт) отсутствует")
        else:
            print("\nТест не пройден: футер отсутствует на странице")

    def tearDown(self):
        self.driver.quit()
        print("\n=== Тестирование завершено ===")


if __name__ == "__main__":
    unittest.main()