import pytest
from selenium import webdriver


@pytest.fixture()
def browser():
    try:
        browser = webdriver.Chrome()
        yield browser
    finally:
        browser.quit()

