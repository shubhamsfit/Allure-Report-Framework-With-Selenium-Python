import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import allure
import tempfile
import shutil
import time

@pytest.fixture
def driver():
    options = Options()

    # Run Chrome in headless mode to avoid GUI and profile conflicts
    options.add_argument("--headless=new")  # Use old "--headless" if this causes issues
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Use a temporary Chrome profile directory (optional but safer)
    temp_profile_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={temp_profile_dir}")

    driver = webdriver.Chrome(options=options)

    yield driver

    # Clean up
    driver.quit()
    time.sleep(2)  # Let Chrome processes fully exit
    shutil.rmtree(temp_profile_dir, ignore_errors=True)

# Screenshot on failure for Allure report
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            allure.attach(driver.get_screenshot_as_png(),
                          name="screenshot",
                          attachment_type=allure.attachment_type.PNG)
