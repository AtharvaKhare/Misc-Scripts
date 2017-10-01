import pickle
from html.parser import HTMLParser
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

chromedriver = "/root/programs/bkp/.tmp/chromedriver"
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
    

os.environ["webdriver.chrome.driver"] = chromedriver
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(chromedriver, chrome_options=chrome_options)
driver.get("http://results.unipune.ac.in/SE2015_CreditPattern.aspx?Course_Code=70215&Course_Name=SE2015")
#assert "Python" in driver.title
students = pickle.load(open('student_info.p','rb'))
sgpa = []
all_subjects = []
raw_html = []
for index, record in enumerate(students):
    elem = driver.find_element_by_name("ctl00$ContentPlaceHolder1$txtSeatno")
    elem.clear()
    elem.send_keys(str(record[0]))
    elem = driver.find_element_by_name("ctl00$ContentPlaceHolder1$txtMother")
    elem.clear()
    elem.send_keys(str(record[1]))
    elem = driver.find_element_by_name("ctl00$ContentPlaceHolder1$btnSubmit")
    elem.send_keys(Keys.ENTER)

    try:
        WebDriverWait(driver, 1).until(EC.alert_is_present(),'Timed out waiting for PA creation ' + 'confirmation popup to appear.')
        alert = driver.switch_to.alert
        alert.accept()
        sgpa.append('Invalid')
        all_subjects.append('Invalid' + record[0])
        continue
    except TimeoutException:
        pass
    raw_html.append(driver.page_source.split("S.E.2015 EXAMINATION MAY 2017 19(S.E.(2015 PAT.)(COMPUTER))")[1].split(" The results published online")[0])
    stripped_src = strip_tags(driver.page_source)
    stripped_src = stripped_src.split("S.E.2015 EXAMINATION MAY 2017 19(S.E.(2015 PAT.)(COMPUTER))")[1].split(" The results published online")[0]
    stripped_src = " ".join(stripped_src.split())
    print(record[0],':',stripped_src[-57:-53])
    all_subjects.append(stripped_src)
    sgpa.append(stripped_src[-57:-53])
    pickle.dump(sgpa, open('sgpa.p','wb'))
    pickle.dump(all_subjects, open('all_subjects.p','wb'))
pickle.dump(sgpa, open('sgpa_final.p','wb'))
pickle.dump(all_subjects, open('all_subjects_final.p','wb'))
pickle.dump(raw_html, open('raw_html.p','wb'))

driver.close()

