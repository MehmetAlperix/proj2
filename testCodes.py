import unittest
from appium import webdriver

class SurveyAppTest(unittest.TestCase):
    def setUp(self):
        capabilities = {
            'platformName': 'Android',
            'platformVersion': '10',
            'deviceName': 'emulator-5554',
            'appPackage': 'org.test.surveyapp',
            'appActivity': '.SurveyApp',
            'automationName': 'UiAutomator2'
        }
        appium_options = webdriver.webdriver.AppiumOptions()
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub',
                                       options=appium_options.load_capabilities(capabilities))
        self.driver.implicitly_wait(10)

    # Test Functions
    def test_fill_survey_form(self):
        name_input = self.driver.find_element_by_accessibility_id("name_input")
        birth_date_input = self.driver.find_element_by_accessibility_id("birth_date_input")
        ok_button = self.driver.find_element_by_accessibility_id("ok_button")
        education_input = self.driver.find_element_by_accessibility_id("education_input")
        city_input = self.driver.find_element_by_accessibility_id("city_input")
        gender_input = self.driver.find_element_by_accessibility_id("gender_input")
        ai_input = self.driver.find_element_by_accessibility_id("ai_input")
        defects_input = self.driver.find_element_by_accessibility_id("defects_input")
        use_cases_input = self.driver.find_element_by_accessibility_id("use_cases_input")
        send_button = self.driver.find_element_by_accessibility_id("send_button")

        name_input.send_keys("Ahmet")
        birth_date_input.click()
        date = "31 March 2024"
        self.driver.find_element_by_accessibility_id(date).click()
        ok_button.click()
        education_input.send_keys("Bachelor's Degree")
        city_input.send_keys("Ankara")
        gender_input.click()
        gender = "Male"
        self.driver.find_element_by_accessibility_id(gender).click()
        ai_input.click()
        selected_model = "ChatGPT"
        self.driver.find_element_by_accessibility_id(selected_model).click()
        selected_model_2 = "Bard"
        self.driver.find_element_by_accessibility_id(selected_model_2).click()
        ok_button.click()
        defects_input.send_keys("None")
        use_cases_input.send_keys("Data analysis")

        # Click on the send button
        send_button.click()

        # Assert success message appears
        success_message = self.driver.find_element_by_accessibility_id("success_message")
        self.assertEqual(success_message.text, "Form successfully filled!")

    def test_empty_survey_submission(self):
        name_input = self.driver.find_element_by_accessibility_id("name_input")
        birth_date_input = self.driver.find_element_by_accessibility_id("birth_date_input")
        ok_button = self.driver.find_element_by_accessibility_id("ok_button")
        education_input = self.driver.find_element_by_accessibility_id("education_input")
        city_input = self.driver.find_element_by_accessibility_id("city_input")
        gender_input = self.driver.find_element_by_accessibility_id("gender_input")
        ai_input = self.driver.find_element_by_accessibility_id("ai_input")
        defects_input = self.driver.find_element_by_accessibility_id("defects_input")
        use_cases_input = self.driver.find_element_by_accessibility_id("use_cases_input")
        send_button = self.driver.find_element_by_accessibility_id("send_button")

        # Leave the name input field empty
        birth_date_input.click()
        date = "31 March 2024"
        self.driver.find_element_by_accessibility_id(date).click()
        ok_button.click()
        education_input.send_keys("Bachelor's Degree")
        city_input.send_keys("Ankara")
        gender_input.click()
        gender = "Male"
        self.driver.find_element_by_accessibility_id(gender).click()
        ai_input.click()
        selected_model = "ChatGPT"
        self.driver.find_element_by_accessibility_id(selected_model).click()
        selected_model_2 = "Bard"
        self.driver.find_element_by_accessibility_id(selected_model_2).click()
        ok_button.click()
        defects_input.send_keys("None")
        use_cases_input.send_keys("Data analysis")

        # Assert that the send button is not visible
        self.assertFalse(send_button.is_displayed(), "Send button is visible with empty fields")

    def test_refill_survey_form(self):
        refill_button = self.driver.find_element_by_accessibility_id("refill_button")

        # Click on the refill button
        refill_button.click()

        # Assert that the survey page is loaded again for refilling
        name_input = self.driver.find_element_by_accessibility_id("name_input")
        self.assertTrue(name_input.is_displayed(), "Survey page not loaded for refilling")

    def test_invalid_date_selection(self):
        birth_date_input = self.driver.find_element_by_accessibility_id("birth_date_input")
        ok_button = self.driver.find_element_by_accessibility_id("ok_button")

        # Select a future date
        birth_date_input.click()
        future_date = "15 December 2024"  # Select a future date
        self.driver.find_element_by_accessibility_id(future_date).click()
        ok_button.click()

        # Verify that the popup message is displayed
        popup_message = self.driver.find_element_by_accessibility_id("popup_message")
        self.assertTrue(popup_message.is_displayed(), "Popup message not displayed for future date selection")

    def test_defects_input_update(self):
        ai_input = self.driver.find_element_by_accessibility_id("ai_input")
        defects_input = self.driver.find_element_by_accessibility_id("defects_input")

        # Select an AI model
        ai_input.click()
        selected_model = "ChatGPT"
        self.driver.find_element_by_accessibility_id(selected_model).click()

        # Verify that defects or cons input is updated based on selected AI model
        expected_defects = "Defects for " + selected_model + ":"
        actual_defects = defects_input.text
        self.assertTrue(expected_defects in actual_defects, "Defects input not updated based on selected AI model")


    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()