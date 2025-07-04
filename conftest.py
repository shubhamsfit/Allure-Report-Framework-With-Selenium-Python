import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import allure
import tempfile
import shutil

@pytest.fixture
def driver():
    options = Options()

    # Create a temporary directory for user data
    temp_profile_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={temp_profile_dir}")

    driver = webdriver.Chrome(options=options)

    yield driver

    driver.quit()

    # Clean up temp directory after quitting the driver
    shutil.rmtree(temp_profile_dir)

# Screenshot on failure
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
