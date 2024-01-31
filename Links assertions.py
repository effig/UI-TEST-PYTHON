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

    # Step 1: Find the link using XPath
    link_element = setup.find_element(By.XPATH, f"//*[@id=mm-root]/header/div/div[1]/nav/div/ul/li[1]/a/span='{link_text_to_verify}']")

    # Step 2: Assertion: Verify link text
    assert link_element.text == link_text_to_verify



#Scenario 2: Verify 'News' link is clickable
def test_link_text_clickable(setup):
    link_text = "News"
    
    # Step 1: Find the link using XPath
    link_xpath = f"//*[@id=mm-root]/header/div/div[1]/nav/div/ul/li[1]/a/span(), '{link_text}')]"
    link_element = setup.find_element(By.XPATH, link_xpath)

    # Step 2: Assert that the link is clickable
    assert link_element.is_displayed() and link_element.is_enabled()

    # Step 3: Click on the link
    link_element.click()

    # Step 4: Verify the new page title
    WebDriverWait(setup, 10).until(EC.title_contains("Football News"))



#Scenario 3: Verify the hover effect on a header link and assert a new titla behind and click on it
def test_hover_effect_and_title_click(setup):
    
    link_xpath = "//*[@id=mm-root]/header/div/div[1]/nav/div/ul/li[3]/span(), 'Premier League')]"
    link_element = setup.find_element(By.XPATH, link_xpath)
    actions = ActionChains(setup)

    # Step 1: Hover over  on the link
    actions.move_to_element(link_element).perform()
    title1_xpath = "//SomeElement, 'Fixtures')]"

    # Step 2: Assert a title which is visible after the hover action
    assert setup.find_element(By.XPATH, title1_xpath).is_displayed()

    # Step 4: Click on the  'Fixtures' link
    title1_xpath.click()

    # Step 5: Verify the new page title
    WebDriverWait(setup, 10).until(EC.title_contains("Premier League fixtures: 2023/24 season"))


#Scenario 4: Verify Responsiveness  on resized page, user will not see the header links, he will get the 'Hamburder' element    
def test_link_not_present_resized_page(setup):
    link_text = "News"
    
    # Step 1: Find the link using XPath
    link_xpath = f"//*[@id=mm-root]/header/div/div[1]/nav/div/ul/li[1]/a/span(), '{link_text}')]"
    link_element = setup.find_element(By.XPATH, link_xpath)

    # Step 2: Verify that the link is present before resizing
    assert link_element.is_displayed(), "Link is  present before resizing"

    # Step 3: Resize the browser window
    driver = webdriver.Chrome()
    driver.set_window_size(800, 600)  #  desired window size

    # Step 4: Verify that the link is not present after resizing
    assert not link_element.is_displayed(), "Link is not present after resizing"

    # Step 5: Verify 'Hamburger' elememnt is present after resize
    element_after_resize = setup.find_element(By.XPATH, "//*[@id=mm-root]/header/div/div[1]/div[1]/div")
    assert element_after_resize.is_displayed(), "Element is displayed after resizing"

    

