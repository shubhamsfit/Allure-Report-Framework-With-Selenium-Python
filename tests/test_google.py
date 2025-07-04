import allure

def test_google_title(driver):
    with allure.step("Open Google homepage"):
        driver.get("https://www.google.com")
    with allure.step("Check page title contains 'Google'"):
        assert "Google" in driver.title
