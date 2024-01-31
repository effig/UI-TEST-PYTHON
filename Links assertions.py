import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


@pytest.fixture
def setup(request):
    driver = webdriver.Chrome()
    driver.get("https://www.90min.com/")

    def teardown():
        driver.quit()

    request.addfinalizer(teardown)
    return driver

#Scenario 1: Verify the text link is found in the header using Xpath 
def test_verify_link_text(setup):
    link_text_to_verify = "News"

    # Find the link using XPath
    link_element = setup.find_element(By.XPATH, f"//*[@id=mm-root]/header/div/div[1]/nav/div/ul/li[1]/a/span='{link_text_to_verify}']")

    # Assertion: Verify link text
    assert link_element.text == link_text_to_verify


#Scenario 2: Verify 'News' link is clickable
def test_link_text_clickable(setup):
    link_text = "News"
    
    # Find the link using XPath
    link_xpath = f"//*[@id=mm-root]/header/div/div[1]/nav/div/ul/li[1]/a/span(), '{link_text}')]"
    link_element = setup.find_element(By.XPATH, link_xpath)

    # Assert that the link is clickable
    assert link_element.is_displayed() and link_element.is_enabled()

    # Click on the link
    link_element.click()

    # Verify the new page title
    WebDriverWait(setup, 10).until(EC.title_contains("Football News"))


#Scenario 3: Verify the hover effect on a header link and assert the new titles behind
def test_hover_effect_and_titles(setup):
    
    link_xpath = "//*[@id=mm-root]/header/div/div[1]/nav/div/ul/li[3]/span(), 'Premier League')]"

    
    link_element = setup.find_element(By.XPATH, link_xpath)

    actions = ActionChains(setup)

    # Hover over  on the link
    actions.move_to_element(link_element).perform()


    title1_xpath = "//h2[contains(text(), 'Title 1')]"
    title2_xpath = "//h2[contains(text(), 'Title 2')]"

    # Assert that other titles are visible after the hover
    assert setup.find_element(By.XPATH, title1_xpath).is_displayed()
    assert setup.find_element(By.XPATH, title2_xpath).is_displayed()
    

