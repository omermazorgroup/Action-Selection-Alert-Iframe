import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
import pytest
import logging
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.ERROR)
mylogger = logging.getLogger()
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrom_driver_path = "C:/Users/omerm/AppData/Local/Temp/Temp1_chromedriver_win32.zip/chromedriver.exe"


@pytest.fixture
def user():
    return {
      "email": "omermazor144@gmail.com",
      "password": "12345"
    }


def test_drag_and_drop():
    driver = webdriver.Chrome(chrom_driver_path, chrome_options=chrome_options)
    driver.maximize_window()
    driver.get('https://demo.guru99.com/test/drag_drop.html')
    actions = ActionChains(driver)
    amount = driver.find_element(By.ID, 'fourth')
    bank_element = driver.find_element(By.ID, 'credit2')
    sales_element = driver.find_element(By.ID, 'credit1')
    debit_side_account = driver.find_element(By.CSS_SELECTOR, '#bank li')
    debit_side_amount = driver.find_element(By.CSS_SELECTOR, '#amt7 li')
    credit_side_account = driver.find_element(By.CSS_SELECTOR, '#loan li')
    credit_side_amount = driver.find_element(By.CSS_SELECTOR, '#amt8 li')
    actions.drag_and_drop(
      bank_element,
      debit_side_account
    ).perform()

    actions.drag_and_drop(
      amount,
      debit_side_amount
    ).perform()

    actions.drag_and_drop(
      sales_element,
      credit_side_account
    ).perform()

    actions.drag_and_drop(
      amount,
      credit_side_amount
    ).perform()
    assert driver.find_element(By.CSS_SELECTOR, '.table4_result > a').text == "Perfect!"
    driver.close()


def test_iframe(user):
    driver = webdriver.Chrome(chrom_driver_path, chrome_options=chrome_options)
    driver.set_window_size(800, 800)
    driver.get('http://automationpractice.com/index.php')
    first_product = driver.find_elements(By.CLASS_NAME, "product-container")[0]
    first_product.find_element(By.CLASS_NAME, 'icon-eye-open').click()
    print(first_product.text)
    time.sleep(5)
    iframe = driver.find_element(By.CLASS_NAME, 'fancybox-iframe')
    driver.switch_to.frame(iframe)
    product_price = driver.find_element(By.ID, 'our_price_display').text
    driver.find_element(By.CSS_SELECTOR, '.box-cart-bottom button').click()
    time.sleep(5)
    driver.find_element(By.CSS_SELECTOR, '#layer_cart .button-container>a').click()
    time.sleep(2)
    driver.find_element(By.CLASS_NAME, "standard-checkout").click()
    driver.find_element(By.ID, "email").send_keys(user["email"])
    driver.find_element(By.ID, "passwd").send_keys(user["password"])
    driver.find_element(By.ID, "SubmitLogin").click()
    driver.find_element(By.CSS_SELECTOR, '[name=processAddress]').click()
    driver.find_element(By.CSS_SELECTOR, 'input#cgv').click()
    driver.find_element(By.CSS_SELECTOR, '[name=processCarrier]').click()
    final_price = driver.find_element(By.ID, "total_product").text
    assert product_price == final_price
    driver.find_element(By.CLASS_NAME, "bankwire").click()
    driver.find_element(By.CSS_SELECTOR, "#cart_navigation > button").click()
    time.sleep(2)
    assert "Your order on My Store is complete" in driver.find_element(By.TAG_NAME, 'body').text
    mylogger.info("text succeeded!")
    driver.close()


def test_alerts():
    driver = webdriver.Chrome(chrom_driver_path, chrome_options=chrome_options)
    driver.maximize_window()
    driver.get('http://the-internet.herokuapp.com/javascript_alerts')
    driver.execute_script("jsAlert()")
    driver.switch_to.alert.accept()
    assert "You successfully clicked an alert" == driver.find_element(By.ID, 'result').text
    driver.execute_script("jsConfirm()")
    driver.switch_to.alert.accept()
    assert "You clicked: Ok" == driver.find_element(By.ID, 'result').text
    driver.execute_script("jsConfirm()")
    driver.switch_to.alert.dismiss()
    assert "You clicked: Cancel" == driver.find_element(By.ID, 'result').text
    driver.execute_script("jsPrompt()")
    driver.implicitly_wait(5)
    text = "Hello Everyone!"
    alert = driver.switch_to.alert
    alert.send_keys(text)
    alert.accept()
    assert f"You entered: {text}" == driver.find_element(By.ID, 'result').text
    driver.close()


def test_selection():
    driver = webdriver.Chrome(chrom_driver_path, chrome_options=chrome_options)
    driver.maximize_window()
    driver.get('https://demo.guru99.com/test/newtours/register.php')
    first_name = "Omer"
    last_name = "Mazor"
    username = "omermazor"
    details = [first_name, last_name, username]
    driver.find_element(By.NAME, 'firstName').send_keys(first_name)
    driver.find_element(By.NAME, 'lastName').send_keys(last_name)
    driver.find_element(By.NAME, 'phone').send_keys("0527712334")
    driver.find_element(By.NAME, 'userName').send_keys("omermazor144@gmail.com")
    driver.find_element(By.NAME, 'address1').send_keys("King George 6")
    driver.find_element(By.NAME, 'city').send_keys("Tel Aviv")
    driver.find_element(By.NAME, 'state').send_keys("Israel")
    driver.find_element(By.NAME, 'postalCode').send_keys("43546")
    select = Select(driver.find_element(By.NAME, 'country'))
    select.select_by_visible_text("ISRAEL")
    driver.find_element(By.NAME, 'email').send_keys(username)
    driver.find_element(By.NAME, 'password').send_keys("12345")
    driver.find_element(By.NAME, 'confirmPassword').send_keys("12345")
    driver.find_element(By.NAME, 'submit').click()
    assert driver.current_url == "https://demo.guru99.com/test/newtours/register_sucess.php"
    assert all(substring in driver.find_element(By.TAG_NAME, 'body').text for substring in details)
