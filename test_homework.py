import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import browser



class TestPetFriends():
    def test_authorization_positive(self, browser):
        """Проверка корректной авторизации пользователя"""
        browser.get('https://petfriends.skillfactory.ru/login')
        browser.find_element(By.CSS_SELECTOR, 'input.form-control#email').send_keys('liza@liza.ru')
        browser.find_element(By.CSS_SELECTOR, 'input.form-control#pass').send_keys('123456789')
        browser.find_element(By.CSS_SELECTOR, 'button.btn.btn-success').click()
        assert browser.find_element(By.CSS_SELECTOR, 'h1.text-center').text == 'PetFriends'

    def test_pet_search(self, browser):
        """ Проверка, что в личном кабинете пользователя есть питомцы"""
        browser.get('https://petfriends.skillfactory.ru/login')
        browser.find_element(By.CSS_SELECTOR, 'input.form-control#email').send_keys('liza@liza.ru')
        browser.find_element(By.CSS_SELECTOR, 'input.form-control#pass').send_keys('123456789')
        browser.find_element(By.CSS_SELECTOR, 'button.btn.btn-success').click()
        browser.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()
        quantity = browser.find_elements(By.CSS_SELECTOR, 'tbody img')
        assert len(quantity) > 0
        print(f'У пользователя питомцев: {len(quantity)}')

    def test_have_a_picture_of_a_pet(self, browser):
        """ Проверка, что у половины питомцев загружена фотография"""
        browser.get('https://petfriends.skillfactory.ru/login')
        browser.find_element(By.CSS_SELECTOR, 'input.form-control#email').send_keys('liza@liza.ru')
        browser.find_element(By.CSS_SELECTOR, 'input.form-control#pass').send_keys('123456789')
        browser.find_element(By.CSS_SELECTOR, 'button.btn.btn-success').click()
        browser.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()
        images = WebDriverWait(browser, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'tbody img')))
        count_none_images = 0
        for i in range(len(images)):
            if images[i].get_attribute('src') == '':
                count_none_images += 1
        assert count_none_images <= (len(images)//2)
        print(f'У {count_none_images} питомцев отсутствует фотография из {len(images)} питомцев')

    def test_breed_age_name_check(self, browser):
        """ Проверка, что у всех питомцев есть имя, возраст и порода"""
        browser.get('https://petfriends.skillfactory.ru/login')
        browser.find_element(By.CSS_SELECTOR, 'input.form-control#email').send_keys('liza@liza.ru')
        browser.find_element(By.CSS_SELECTOR, 'input.form-control#pass').send_keys('123456789')
        browser.find_element(By.CSS_SELECTOR, 'button.btn.btn-success').click()
        browser.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()
        browser.implicitly_wait(5)
        names = browser.find_elements(By.CSS_SELECTOR, 'tbody tr td:nth-child(2)')
        ages = browser.find_elements(By.CSS_SELECTOR, 'tbody tr td:nth-child(4)')
        breeds = browser.find_elements(By.CSS_SELECTOR, 'tbody tr td:nth-child(3)')
        count_pets_none = 0
        for i in range(len(names)):
            if names[i].text == '' or ages[i].text == '' or breeds[i].text == '':
                count_pets_none += 1
        print(f'У {count_pets_none} карточек неполностью заполненны данные')
        assert len(names) == count_pets_none

    def test_check_name(self, browser):
        """ Проверка, что у всех питомцев разные имена"""
        browser.get('https://petfriends.skillfactory.ru/login')
        browser.find_element(By.CSS_SELECTOR, 'input.form-control#email').send_keys('liza@liza.ru')
        browser.find_element(By.CSS_SELECTOR, 'input.form-control#pass').send_keys('123456789')
        browser.find_element(By.CSS_SELECTOR, 'button.btn.btn-success').click()
        browser.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()
        names = browser.find_elements(By.CSS_SELECTOR, 'tbody tr td:nth-child(2)')
        check_name = dict()
        for i in range(len(names)):
            if names[i].text not in check_name:
                check_name[names[i].text] = 1
            else:
                check_name[names[i].text] += 1
        check_name_item = check_name.items()
        name_duplication = []
        count_unique_name = 0
        for name, count in check_name_item:
            if count >= 2:
                name_duplication.append(name)
            else:
                count_unique_name += 1
        print(f'{len(name_duplication)} имен часто повторяются в карточках питомцев. Всего {count_unique_name} неповтоящихся имени.')
        assert len(name_duplication) == 0

    def test_check_pets(self, browser):
        """ Проверка, что в списке нет повторяющихся питомцев"""
        browser.get('https://petfriends.skillfactory.ru/login')
        browser.find_element(By.CSS_SELECTOR, 'input.form-control#email').send_keys('liza@liza.ru')
        browser.find_element(By.CSS_SELECTOR, 'input.form-control#pass').send_keys('123456789')
        browser.find_element(By.CSS_SELECTOR, 'button.btn.btn-success').click()
        browser.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()
        names = browser.find_elements(By.CSS_SELECTOR, 'tbody tr td:nth-child(2)')
        ages = browser.find_elements(By.CSS_SELECTOR, 'tbody tr td:nth-child(4)')
        breeds = browser.find_elements(By.CSS_SELECTOR, 'tbody tr td:nth-child(3)')
        names_text = [names[i].text for i in range(len(names))]
        ages_text = [ages[i].text for i in range(len(ages))]
        breeds_text = [breeds[i].text for i in range(len(breeds))]
        zip_pets = list(zip(names_text, ages_text, breeds_text))
        count_dict = dict()
        for i in zip_pets:
            if i not in count_dict:
                count_dict[i] = 1
            else:
                count_dict[i] += 1
        count_dict_item = count_dict.items()
        count_unique_pet = 0
        for name, count in count_dict_item:
            if count == 1:
                count_unique_pet += 1
        print(f'В списке {count_unique_pet} неповторяющихся питомцев')
        assert count_unique_pet == len(names)

















