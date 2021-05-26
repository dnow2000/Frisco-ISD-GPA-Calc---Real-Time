'''
Author @SumitNalavade
'''

import tkinter
from tkinter import Tk, Label, Button, Entry, Frame
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from PIL import Image, ImageTk

courseList = []  # Hold all the Course objects to run calculations off

PATH = 'C:\Program Files (x86)\chromedriver.exe'
opts = Options()
opts.add_argument("--headless")  # Toggle headless browser
driver = webdriver.Chrome(PATH, options=opts)

gpas = None

# create main window
login_page = Tk()
login_page.geometry('300x300')

frame = Frame(login_page, bg = "#3c008b", width=300, height = 300) #Mainframe
frame.pack()

class Course():  # Course object
    def __init__(self, name, grade, weight, credits):
        self.name = name
        self.grade = grade
        self.weight = weight
        self.credits = credits

    def __str__(self):
        return (f'NAME: {self.name}, GRADE: {self.grade}, WEIGHT: {self.weight}, CREDITS: {self.credits}')

# creates the login page

def create_login_page():
    #Adds elements onto the mainframe
    header = Label(frame, background='#3c008b', text='GPA CALCULATOR',
                   fg='White', font='BEBAS 20 bold').place(x=20, y=0)
    username_label = Label(frame, text='Enter HAC Username:',
                           background='#3c008b', fg='White')
    password_label = Label(frame, text='Enter HAC Password:',
                           background='#3c008b', fg='White')

    username_label.place(x=20, y=70)
    password_label.place(x=20, y=120)

    username_entry = Entry(frame)
    password_entry = Entry(frame, show="*")

    username_entry.place(x=150, y=70)
    password_entry.place(x=150, y=120)
   
    # Authenticates Login
    def authenticate_login():
        global PATH
        global driver

        driver.get("https://hac.friscoisd.org/HomeAccess/Grades/Transcript")

        # Find and enter user inputted username and password into HAC
        username_field = driver.find_element_by_id("LogOnDetails_UserName")
        password_field = driver.find_element_by_id("LogOnDetails_Password")
        login_button = driver.find_element_by_id("login")

        username_field.send_keys(username_entry.get())
        password_field.send_keys(password_entry.get())

        password_field.send_keys(Keys.RETURN)  # Press enter button

        # If the login is successful, redirects to this page
        if(driver.current_url == "https://hac.friscoisd.org/HomeAccess/Grades/Transcript"):
            for widget in frame.winfo_children(): #Removes all widgets from the mainframe
                widget.destroy()
            pass

            compute_gpa()  # If the login is successful, the calculation begins
        else:
            not_successful_popup = Tk()
            not_successful_popup.geometry('230x50')
            not_successful_popup.config(background='#3c008b')

            not_successful_label = Label(not_successful_popup, text='Incorrect Username or Password',
                                         background='#3c008b', font='Bebas 10 bold', fg='White').pack()  # Pop up if login not successful

    login_button = Button(frame, text='Login', command=authenticate_login,
                          height=1, width=20, background='white', font='bebas 10 bold')
    login_button.place(x=68, y=200)
    
    login_page.mainloop()  # Runs the login page


def get_grades():
    global driver
    global PATH
    global courseList

    driver.get(
        "https://hac.friscoisd.org/HomeAccess/Content/Student/Transcript.aspx")

    # Finds the current weighted and unweighted GPAs
    current_weighted_gpa = driver.find_element_by_id(
        "plnMain_rpTranscriptGroup_lblGPACum1").text
    current_unweighted_gpa = driver.find_element_by_id(
        "plnMain_rpTranscriptGroup_lblGPACum2").text

    try:
        for a in range(6):
            current_gradelevel = driver.find_element_by_id(
                f"plnMain_rpTranscriptGroup_lblGradeValue_{a}").text
            current_gradelevel = int(current_gradelevel)
    except:
        pass

    # Naviagate to the real-time grades
    driver.get(
        "https://hac.friscoisd.org/HomeAccess/Content/Student/Assignments.aspx")

    x = 4
    try:
        for i in range(15):
            # Find the name and grades for all the current classes
            name = driver.find_element_by_xpath(
                f'//*[@id="plnMain_pnlFullPage"]/div[{x}]/div[1]/a').text
            grade = driver.find_element_by_id(
                f'plnMain_rptAssigmnetsByCourse_lblHdrAverage_{i}').text
            weight = 5
            credits = 1

            x += 1

            if(grade != ''):
                grade = grade.replace('Student Grades ', '').replace(
                    '%', '')  # Change grade from str to int
                grade = float(grade)

                # Edge cases in which the credit or weight is diffrent
                if(('pap' in name.lower()) or ('ap' in name.lower()) or ('adv computer science' in name.lower())):
                    weight = 6

                if(('ISM' in name) or ('Academic Dec' in name)):
                    weight = 5.5

                double_weighted = ['gt', 'physics c', 'veterinary', 'equipment', 'architectural design 2', 'interior design 2', 'animation', 'sports broadcasting', 'graphic Design', 'child guidance',
                                   'education and training', 'practicum in govern', 'clinical', 'electrocardiography', 'medical technician', 'hospitality', 'culinary', 'ap computer', 'sports management']

                for b in double_weighted:
                    if(b in name.lower()):
                        credits = 2

                # Creates a course object from the name, grade, wight and credits then appends it to the courselist
                courseList.append(Course(name, grade, weight, credits))
                weight = 5
                credits = 1
    except:
        return (current_gradelevel, current_unweighted_gpa, current_weighted_gpa)


def create_display_page():  # Displays the final weighted and unweighted GPA
    global gpas

    header = Label(frame, background='#3c008b', text='GPA CALCULATOR',
                   fg='White', font='BEBAS 20 bold').place(x=20, y=0)

    weighted_gpa, unweighted_gpa = gpas

    weighted_gpa = round(weighted_gpa, 3)
    unweighted_gpa = round(unweighted_gpa, 3)

    weighted_gpa_header = Label(frame, text='Weighted GPA:',
                                background='#3c008b', font='bebas 15 bold', fg='White')
    unweighted_gpa_header = Label(
        frame, text='Unweighted GPA:', background='#3c008b', font='bebas 15 bold', fg='white')

    weighted_gpa_header.place(x=75, y=70)
    unweighted_gpa_header.place(x=65, y=170)

    weighted_gpa_label = Label(frame, text=weighted_gpa,
                               background='#3c008b', font='bebas 15 bold', fg='White')
    unweighted_gpa_label = Label(
        frame, text=unweighted_gpa, background='#3c008b', font='bebas 15 bold', fg='White')

    weighted_gpa_label.place(x=123, y=100)
    unweighted_gpa_label.place(x=123, y=200)

    driver.quit()

    def redo():  # Redo Calculation with new parameters
        global courseList
        global driver

        weighted_gpa_header.destroy()
        unweighted_gpa_header.destroy()
        weighted_gpa_label.destroy()
        unweighted_gpa_label.destroy()
        redo_button.destroy()

        courseList.clear()

        # Reinitializes the webdriver
        driver = webdriver.Chrome(PATH, options=opts)

        create_login_page()

    redo_button = Button(frame, text='Retry',
                         font='bebas 10 bold', height=1, width=20, command=redo)
    redo_button.place(x=67, y=250)


def compute_gpa():  # calculates the weighted and unweighted gpas from the courselist, Returns a tuple of both
    global courseList
    global gpas

    current_gradelevel, current_unweighted_gpa, current_weighted_gpa = get_grades()

    number_of_total_credits = 0
    total_semesters = 0

    if(current_gradelevel == 12):
        total_semesters = 7
    elif(current_gradelevel == 11):
        total_semesters = 5
    elif(current_gradelevel == 10):
        total_semesters = 3
    elif(current_gradelevel == 9):
        total_semesters = 1

    for courses in courseList:
        number_of_total_credits += courses.credits

    weighted_gpa_list = []
    unweighted_gpa_list = []

    weightedGpa = 0.0
    unweightedGpa = 0.0

    for courses in courseList:  # Iterates through the courselist and calculates weighted GPA given the scale of each class
        if(courses.grade < 70):
            weightedGpa = 0
        elif(courses.grade == 70):
            weightedGpa = 3
        else:
            weightedGpa = (
                (courses.weight - ((100 - courses.grade)/10)) * courses.credits)

        weighted_gpa_list.append(weightedGpa)

    weightedGpa = (sum(weighted_gpa_list) / number_of_total_credits)

    for courses in courseList:  # Iterates through the courselist and calculates unweighted GPA out of 4.0
        if (courses.grade < 70):
            unweightedGpa = 0
        elif(courses.grade == 70):
            unweightedGpa = 2
        else:
            unweightedGpa = ((4.0 - ((90 - courses.grade)/10))
                             * courses.credits)

        if((courses.credits == 2) and (unweightedGpa > 8.0)):
            unweightedGpa = 8.0
        elif (unweightedGpa > 4.0):
            unweightedGpa = 4.0

        unweighted_gpa_list.append(unweightedGpa)

    unweightedGpa = (sum(unweighted_gpa_list) / number_of_total_credits)

    weightedGpa = ((float(current_weighted_gpa) * total_semesters) + weightedGpa) / \
        (total_semesters+1)  # Merges the gpas from HAC with the current calculated GPAs
    unweightedGpa = ((float(current_unweighted_gpa) *
                     total_semesters) + unweightedGpa)/(total_semesters+1)

    gpas = (weightedGpa, unweightedGpa)
    create_display_page()


def main():
    create_login_page()


if __name__ == "__main__":
    main()
