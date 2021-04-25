from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

PATH = 'C:\Program Files (x86)\chromedriver.exe'

driver = webdriver.Chrome(PATH)

driver.get("https://hac.friscoisd.org/HomeAccess/Content/Student/Assignments.aspx")

username_field = driver.find_element_by_id("LogOnDetails_UserName")
password_field = driver.find_element_by_id("LogOnDetails_Password")
login_button = driver.find_element_by_id("login")

username_field.send_keys('177611')
password_field.send_keys('12242003')

password_field.send_keys(Keys.RETURN)

driver.get("https://hac.friscoisd.org/HomeAccess/Content/Student/Assignments.aspx")

hac_grade_elements = []
hac_grades = []

try:
    for i in range(15):
        test = driver.find_element_by_id(f"plnMain_rptAssigmnetsByCourse_lblHdrAverage_{i}").text
        hac_grade_elements.append((test.replace('Student Grades', '').replace('%', '')))
except:
    for elements in hac_grade_elements:
        try:
            hac_grades.append(float(elements))
        except ValueError:
            pass

    
