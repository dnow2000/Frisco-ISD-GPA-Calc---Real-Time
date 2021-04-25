from tkinter import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

courseList = [] #Hold all the Course objects to run calculations off

PATH = 'C:\Program Files (x86)\chromedriver.exe'
opts = Options()
opts.add_argument("--headless")
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

        driver.get("https://hac.friscoisd.org/HomeAccess/Content/Student/Assignments.aspx")

        username_field = driver.find_element_by_id("LogOnDetails_UserName")
        password_field = driver.find_element_by_id("LogOnDetails_Password")
        login_button = driver.find_element_by_id("login")

        username_field.send_keys(username_entry.get())
        password_field.send_keys(password_entry.get())

        password_field.send_keys(Keys.RETURN)

        if(driver.current_url == "https://hac.friscoisd.org/HomeAccess/Home/WeekView"):
            login_page.destroy()

            create_main_page()
        else:
            not_successful_popup = Tk()
            not_successful_popup.geometry('230x50')
            not_successful_popup.config(background = '#6200EE')

            not_successful_label = Label(not_successful_popup, text = 'Incorrect Username or Password', background = '#6200EE', font = 'Bebas 10 bold', fg = 'White').pack()

    login_button = Button(login_page, text = 'Login', command = authenticate_login, height = 2, width = 20)
    login_button.place(x = 68, y = 200)
    
    login_page.mainloop()

#Once the login is authenticated, this is the calculation page
def create_main_page():  
    mainpage = Tk()
    mainpage.configure(background = '#6200EE') 
    mainpage.geometry('300x300')
    header = Label(mainpage, background = '#6200EE' ,text = 'GPA CALCULATOR', fg = 'White', font = 'BEBAS 20 bold').place(x=20, y=0)
    
    course_name_label = Label(mainpage, text = 'Course Name:', background = '#6200EE', fg = 'White')
    course_grade_label = Label(mainpage, text = 'Grade:', background = '#6200EE', fg = 'White')
    course_weight_label = Label(mainpage, text = 'Weight:', background = '#6200EE', fg = 'White')
    course_credits_label = Label(mainpage, text = 'Credit:', background = '#6200EE', fg = 'White')

    course_name_label.place(x = 20, y = 50)
    course_grade_label.place(x = 20, y = 100)
    course_weight_label.place(x= 20, y = 150)
    course_credits_label.place(x = 20, y = 200)

    course_name_entry = (Entry(mainpage))
    course_grade_entry = Entry(mainpage)
    course_weight_entry = Entry(mainpage)
    course_credits_entry = Entry(mainpage)

    course_name_entry.place(x = 120, y = 50)
    course_grade_entry.place(x = 120, y = 100)
    course_weight_entry.place(x = 120, y = 150)
    course_credits_entry.place(x = 120, y = 200)

    #Decorator to avoid ZeroDivisionError if there are no classes added to the courselist
    def smart_clear(func):
        def inner():
            if(len(courseList) <= 0):
                no_classes_label = Label(mainpage, text = 'No classes added', background = '#6200EE', font = 'bebas 10 bold', fg = 'White').pack()
            else:
                func()
        return inner

    @smart_clear
    def clear():
        course_name_label.destroy() #Destroy all elements on the window
        course_grade_label.destroy()
        course_weight_label.destroy()
        course_credits_label.destroy()

        course_name_entry.destroy()
        course_grade_entry.destroy()
        course_weight_entry.destroy()
        course_credits_entry.destroy()
        
        add_button.destroy()
        calc_gpa.destroy()

        compute_gpa() #Begins the calculation on all the Class objecsts in the courselist

    #Adds a Course object to the courseList
    def add_to_courseList():
        global courseList

        try:
            name = course_name_entry.get()
            grade = float(course_grade_entry.get())
            weight = int(course_weight_entry.get())
            num_credits = int(course_credits_entry.get())
        except ValueError: #Ex: String in place of an float
            value_error_popup = Tk()
            value_error_popup.config(background = '#6200EE')
            value_error_label = Label(value_error_popup, text = 'Incorrect Values', background = '#6200EE', font = 'bebas 10 bold', fg = 'White').pack()
        else:
            courseList.append(Course(name, grade, weight, num_credits)) #Create a Course object using the parameters then append that to the courselist

            #Popup that says the class was added successfully
            class_added_window = Tk()
            class_added_window.config(background = '#6200EE')
            class_added_window.geometry('200x50')

            class_added_label = Label(class_added_window, text = 'Class added successfully', background = '#6200EE', font = 'bebas 10 bold', fg = 'White').pack()      

    #Don't forget to create the button
    add_button = Button(text = 'Add Class', command = add_to_courseList, height = 1, width = 10)
    calc_gpa = Button(text = 'Calculate', command = clear, height = 1, width = 10)

    add_button.place(x = 35, y = 250)
    calc_gpa.place(x = 165, y = 250)
    
    mainpage.mainloop() #Make the elements show up

def create_display_page(): #Displays the final weighted and unweighted GPA 
    global gpas

    weighted_gpa, unweighted_gpa = gpas
    
    weighted_gpa_header = Label(mainpage, text = 'Weighted GPA:', background = '#6200EE', font = 'bebas 15 bold', fg = 'White')
    unweighted_gpa_header = Label(mainpage, text = 'Unweighted GPA:', background = '#6200EE', font = 'bebas 15 bold', fg = 'white')

    weighted_gpa_header.place(x = 80, y = 70)
    unweighted_gpa_header.place(x = 70, y = 170)

    weighted_gpa_label = Label(mainpage, text = weighted_gpa, background = '#6200EE', font = 'bebas 15 bold', fg ='White')
    unweighted_gpa_label = Label(mainpage, text = unweighted_gpa, background = '#6200EE', font = 'bebas 15 bold', fg ='White')

    weighted_gpa_label.place(x = 135, y = 100)
    unweighted_gpa_label.place(x = 135, y = 200)

    def redo():
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


