from tkinter import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

courseList = [] #Hold all the Course objects to run calculations off

PATH = 'C:\Program Files (x86)\chromedriver.exe'
#opts = Options()
#opts.add_argument("--headless") #Toggle headless browser
driver = webdriver.Chrome(PATH) 

gpas = None

class Course(): #Course object
    def __init__(self, name, grade, weight, credits):
        self.name = name
        self.grade = grade
        self.weight = weight
        self.credits = credits
    
    def __str__(self):
        return (f'NAME: {self.name}, GRADE: {self.grade}, WEIGHT: {self.weight}, CREDITS: {self.credits}')

#create main window
login_page = Tk()
login_page.configure(background = '#6200EE') 
login_page.geometry('300x300')
header = Label(login_page, background = '#6200EE' ,text = 'GPA CALCULATOR', fg = 'White', font = 'BEBAS 20 bold').place(x=20, y=0)

#creates the login page
def create_login_page():
    username_label = Label(login_page, text  = 'Enter Username:', background = '#6200EE', fg = 'White')
    password_label = Label(login_page, text = 'Enter Password', background = '#6200EE', fg = 'White')

    username_label.place(x = 20, y = 70)
    password_label.place(x = 20, y = 120)

    username_entry = Entry(login_page)
    password_entry = Entry(login_page)

    username_entry.place(x = 120, y = 70)
    password_entry.place(x = 120, y = 120)

    #Authenticates Login
    def authenticate_login():
        global PATH
        global driver

        driver.get("https://hac.friscoisd.org/HomeAccess/Grades/Transcript")

        username_field = driver.find_element_by_id("LogOnDetails_UserName")
        password_field = driver.find_element_by_id("LogOnDetails_Password")
        login_button = driver.find_element_by_id("login")

        username_field.send_keys(username_entry.get())
        password_field.send_keys(password_entry.get())

        password_field.send_keys(Keys.RETURN)

        if(driver.current_url == "https://hac.friscoisd.org/HomeAccess/Grades/Transcript"):
            login_page.destroy()

            get_grades()
        else:
            not_successful_popup = Tk()
            not_successful_popup.geometry('230x50')
            not_successful_popup.config(background = '#6200EE')

            not_successful_label = Label(not_successful_popup, text = 'Incorrect Username or Password', background = '#6200EE', font = 'Bebas 10 bold', fg = 'White').pack()

    login_button = Button(login_page, text = 'Login', command = authenticate_login, height = 2, width = 20)
    login_button.place(x = 68, y = 200)
    
    login_page.mainloop()

def get_grades():
    global driver
    global PATH
    global courseList

    driver.get("https://hac.friscoisd.org/HomeAccess/Content/Student/Transcript.aspx")

    current_weighted_gpa = driver.find_element_by_id("plnMain_rpTranscriptGroup_lblGPACum1").text
    current_unweighted_gpa = driver.find_element_by_id("plnMain_rpTranscriptGroup_lblGPACum2").text

    driver.get("https://hac.friscoisd.org/HomeAccess/Content/Student/Assignments.aspx")

    
    x = 4
    try:
        for i in range(15):
            name = driver.find_element_by_xpath(f'//*[@id="plnMain_pnlFullPage"]/div[{x}]/div[1]/a').text
            grade = driver.find_element_by_id(f'plnMain_rptAssigmnetsByCourse_lblHdrAverage_{i}').text
            weight = 5
            credits = 1

            x+=1
            
            if(grade != ''):
                grade = grade.replace('Student Grades ', '').replace('%', '')
                grade = float(grade)
                
                if(('pap' in name.lower()) or ('ap' in name.lower()) or ('adv computer science' in name.lower())):
                    weight = 6

                if(('ISM' in name) or ('Academic Decathlon' in name)):
                    weight = 5.5
                
                double_weighted = ['gt', 'physics c', 'veterinary', 'equipment', 'architectural design 2', 'interior design 2', 'animation', 'sports broadcasting', 'graphic Design', 'child guidance', 
                'education and training', 'practicum in govern', 'clinical', 'electrocardiography', 'medical technician', 'hospitality', 'culinary', 'ap computer', 'sports management']

                for b in double_weighted:
                    if(b in name.lower()):
                        credits = 2
                
                courseList.append(Course(name, grade, weight, credits))
                weight = 5
                credits = 1
    except:   
        compute_gpa()
        

def create_display_page(): #Displays the final weighted and unweighted GPA 
    global gpas

    mainpage = Tk()
    mainpage.configure(background = '#6200EE') 
    mainpage.geometry('300x300')
    header = Label(mainpage, background = '#6200EE' ,text = 'GPA CALCULATOR', fg = 'White', font = 'BEBAS 20 bold').place(x=20, y=0)


    weighted_gpa, unweighted_gpa = gpas
    
    weighted_gpa_header = Label(mainpage, text = 'Weighted GPA:', background = '#6200EE', font = 'bebas 15 bold', fg = 'White')
    unweighted_gpa_header = Label(mainpage, text = 'Unweighted GPA:', background = '#6200EE', font = 'bebas 15 bold', fg = 'white')

    weighted_gpa_header.place(x = 80, y = 70)
    unweighted_gpa_header.place(x = 70, y = 170)

    weighted_gpa_label = Label(mainpage, text = weighted_gpa, background = '#6200EE', font = 'bebas 15 bold', fg ='White')
    unweighted_gpa_label = Label(mainpage, text = unweighted_gpa, background = '#6200EE', font = 'bebas 15 bold', fg ='White')

    weighted_gpa_label.place(x = 135, y = 100)
    unweighted_gpa_label.place(x = 135, y = 200)

    def redo(): #Redo Calculation with new parameters
        global courseList
        
        weighted_gpa_header.destroy()
        unweighted_gpa_header.destroy()
        weighted_gpa_label.destroy()
        unweighted_gpa_label.destroy()
        redo_button.destroy()

        courseList.clear()

        create_main_page()

    redo_button = Button(mainpage, text = 'Retry', font = 'bebas 10 bold', height = 1, width = 20, command = redo)
    redo_button.place(x = 67, y = 250)

def compute_gpa(): #calculates the weighted and unweighted gpas from the courselist, Returns a tuple of both
	global courseList
	global gpas
	
	number_of_total_credits = 0
	for courses in courseList:
		number_of_total_credits += courses.credits

	weighted_gpa_list = []
	unweighted_gpa_list = []

	weightedGpa = 0.0
	unweightedGpa = 0.0

	for courses in courseList: #Iterates through the courselist and calculates weighted GPA given the scale of each class
		weightedGpa = ((courses.weight - ((100 - courses.grade)/10)) * courses.credits)

		weighted_gpa_list.append(weightedGpa)
	
	weightedGpa = (sum(weighted_gpa_list) / number_of_total_credits)
	
	for courses in courseList: #Iterates through the courselist and calculates unweighted GPA out of 4.0
		unweightedGpa = ((4.0 - ((90 - courses.grade)/10)) * courses.credits)
		
		if (unweightedGpa > 4.0):
			unweightedGpa = 4.0

		unweighted_gpa_list.append(unweightedGpa)

	unweightedGpa = (sum(unweighted_gpa_list) / number_of_total_credits)

	gpas = (weightedGpa, unweightedGpa)
	create_display_page()

def main():
    create_login_page()

if __name__ == "__main__":
    main()


