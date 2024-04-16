# all the imports
import numpy as np
import pandas as pd
from collections import Counter
import tkinter as tk
from tkinter import filedialog
import os



# # globals (ALL GLOBALS ARE DELETED THROUGHOUT THE FUNCTION TO ENSURE THAT NONE REMAIN AT THE END OF RUNTIME)

temp_sec = []

temp_students = []

temp_bad_students = []

temp_group_GPA = []

df = pd.DataFrame(columns=['Student','Courses'])

df_help = pd.DataFrame(columns=['Student','Courses'])

# # Creating 2D arrays from a group, 2D is for the sections

# Function for assigning Groups to RUN files

def create_GRP(run): 
    
   
    #creates temp array that takes in a run file
    
    data = []  

    #opens up the file
    with open(run) as file:
        
        #begins to read lines in file
        line = file.readlines()
        
        #for loop to loop through the lines  
        for x in line:
            
            #removes white space
            x = x.strip()
            
            #checks whether or not a .GRP file exists
            data.append(x)
            
    #returns the array
    return np.array(data)

# Functions for assigning Sections to Groups
def create_SEC(grp):
    
    #creates a temp array
    data = []
    
    #opens the group file
    with open(grp) as file:
        
        #begins reading lines
        line = file.readlines()
        
        #for loop to loop through the line
        for x in line:
            
            #strips the white space
            x = x.strip()
            
            #checks if there is a section file
            data.append(x)
            
    #returns the array to the 
    return np.array(data)

#creates an array for the students
def create_students(sec):
    
    #creates a temp array
    data = []
    
    #opens up the section file to read
    with open(sec, 'r') as file:
        
        #reads the first line and adds it to the array
        temp = file.readline()
        
        #for loop
        for x in file:
            
            #strips the white space and the quotes
            val = x.strip().strip('"').split('","')
            
            #appends data to the array
            if len(val) != 3:
                pass
            else:
                data.append(val)
        #finds out what the credit hours are
        if temp.strip().endswith('3.0'):
            temp = 3.0
        elif temp.strip().endswith('3'):
            temp = 3.0
        else:
            temp = 4.0
        #appends the data to the data array
        data.append(temp)
    #the second for loop is for assigning the letter to number function to the third value of each array column
    
    for x in data[:-1]:
        
        val=x[2]
        
        #calls the letter to num function to convert grade letter to number
        point = letter_to_number(val)
        x[2]=point
    #returns the array
    return data

# Function for assigning letters to GPA numbers
def letter_to_number(letterGrade):
    
    
    #long list of values for each possible grade
    gpaLetter = {
        'A': 4.0,
        'A-': 3.7,
        'B+': 3.3,
        'B': 3.0,
        'B-': 2.7,
        'C+': 2.3,
        'C': 2.0,
        'C-': 1.7,
        'D+': 1.3,
        'D': 1.0,
        'F': 0.0,
        'I': None,  
        'W': None,  
        'P': None,  
        'NP': None
    }
    
    #returns a get function to see what the inputted letter is related to for GPA's
    return gpaLetter.get(letterGrade,None)

#function for finding the GPA. Uses an array
def calc_SEC_GPA(array, course):
    global df
    global df_help
   
    #assigns credit hours to a variable
    credit = array[-1]
    #creates the data temp array
    data = []
    #only takes in the values, not the credit hours
    data.append(array[:-1])
    #creates an empty temp numpy array
    summy = np.empty((0,0))
    #for loop to loop through specifically the grade numbers
    for x in data:
        for y in x:
            val = y[2]
            if isinstance(val, float):
                summy = np.append(summy, val)
    #calculations for the GPA
    summy = summy * credit
    

    
    students_to_append = []
    help_append = []
    
    for x in data:
        for y in x:
            temp_student = y[0]
            temp_grade = y[2]
            temp_class = course
            
            if temp_grade is not None:
                
                    if temp_grade >= 3.7:
                    
                            students_to_append.append({'Student': temp_student, 'Courses': temp_class})
                    elif temp_grade <= 1.3:
                        
                            help_append.append({'Student': temp_student, 'Courses': temp_class})   
    
    df_temp = pd.DataFrame(students_to_append)
    
    df_help_temp = pd.DataFrame(help_append)
        
    df = pd.concat([df, df_temp], ignore_index=True)
    
    df_help = pd.concat([df_help, df_help_temp], ignore_index=True)
               
    newGPA = (np.sum(summy))/(credit*np.size(summy))
    
    temp_sec.append(newGPA)
    
    return newGPA, credit
    
#function to start the whole thing  

def empty_list(array):
    global temp_sec
    temp_sec.clear()

def calc_Group_GPA(gpas, creds):
    
    gps = 0
    chs = 0
    
    for x, y in zip(gpas, creds):
        temp = x * y
        gps += temp
        chs += y
        
    groupGPA = gps / chs
    return groupGPA

def begin(run):
    
    
    file = open('GPA_Results.txt', 'w')
    
    
    array = create_GRP(run)
    empty_list(temp_sec)
    update_text("Getting the Groups...")
    update_text("Calculating the SEC GPA's...")
    
    
    
    
    
    group_GPAs = []
    
    
    for x in array[1:]:
        file.write(f"****** Now Showing Group {x} ******\n\n")
        temp = create_SEC(x)
        temp_sum = 0
        std_dev = 0
        sec_gps = []
        temp_credit = []
        
        empty_list(temp_sec)
        
        for y in temp[1:]:
            temptwo = create_students(y)
            sectempgpa, temp_cred = calc_SEC_GPA(temptwo, y)
            sec_gps.append(sectempgpa)
            temp_credit.append(temp_cred)
            std_dev = np.std(temp_sec)
        
        
        
        temp_GROUP = calc_Group_GPA(sec_gps, temp_credit)
        group_GPAs.append(temp_GROUP)
        
        
        
        file.write(f"\nThe GPA of group {x} is: {round(temp_GROUP,3)}\n\n")
        newtemp = create_SEC(x)
        newcount = 0
        
        '''
        FAST FUNCTION BABY
        '''
        
        for g in newtemp[1:]:
            empty_list(temp_sec)
            newsectemp = sec_gps[newcount]
            newcount = newcount + 1
            z_score = (newsectemp - temp_GROUP) / std_dev
            file.write(f"\nSection {g}'s GPA is {round(newsectemp,3)}") 
            if z_score >= 2 or z_score <= -2:
                file.write(f" which is different from the Group GPA by a Z-Score of {round(z_score,2)}")
            else:
                file.write(".")
        file.write("\n\n")
    
    
    
    temp_av = sum(group_GPAs) / len(group_GPAs)
    
    
    temp_grp_std = 0
    temp_grp_std = np.std(group_GPAs)
    
    '''
    FAST FUNCTION BABY
    '''
    
    for x in group_GPAs:
        temp_gpa = x
        temp_Z_score = (temp_gpa - temp_av) / temp_grp_std
        if temp_Z_score > 2.0 or temp_Z_score < -2:
            file.write(f"\n\n Group {x} standard deviation is significant to the group, Z_Score = {temp_Z_score}")
    
    
    update_text("Getting Relevant Students...")
    
    
    #creates a new array that groups the array of students that got very good grades and resets the index
    df_grouped_good = df.groupby('Student')['Courses'].agg(', '.join).reset_index()
    
    #creates a new column that is the number of courses a student has (for sorting by the amount of courses)
    df_grouped_good['Num_Courses'] = df_grouped_good['Courses'].apply(lambda x: len(x.split(', ')))
    
    #creates a new filtered array that filters out the students with only 1 very good grade
    df_filtered_good = df_grouped_good[df_grouped_good['Num_Courses'] >= 2]
    
    #sorts the array by the number of courses
    df_filtered_good = df_filtered_good.sort_values(by=['Num_Courses', 'Student'])
    
    #then removes the column because it is no longer necessary
    df_filtered_good = df_filtered_good.drop(columns=['Num_Courses'])
    
    #does the same thing as above except for the students with bad grades
    df_grouped_help = df_help.groupby('Student')['Courses'].agg(', '.join).reset_index()
    df_grouped_help['Num_Courses'] = df_grouped_help['Courses'].apply(lambda x: len(x.split(', ')))
    df_filtered_help = df_grouped_help[df_grouped_help['Num_Courses'] >= 2]
    df_filtered_help = df_filtered_help.sort_values(by=['Num_Courses', 'Student'])
    df_filtered_help = df_filtered_help.drop(columns=['Num_Courses'])
    
    update_text("Printing...")
    
    file.write(f"\nHere are the students with more than one A-, A\n\n")
    for index, row in df_filtered_good.iterrows():
        file.write(row['Student'] + ' || ' + row['Courses'] + '\n')
        file.write(' ' * 80 + '\n')
    
    file.write(f"\nHere are the students with more than one D+, D, D-, F\n\n")
    for index, row in df_filtered_help.iterrows():
        file.write(row['Student'] + ' || ' + row['Courses'] + '\n')
        file.write(' ' * 80 + '\n')
    
    update_text("Removing existing data...")
    
    update_text("DONE! Please go to the file location of the .RUN file for the .txt file!")

window = tk.Tk()
window.title("GPA Project Calculator")
window.geometry("700x350")

run_file = ""

def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Runnable Files", "*.run")])
   
    run_file = file_path
    
    print("Start")
    begin(run_file)
    
    # removes all the data from the GLOBAL VARIABLES
    
    empty_list(temp_sec)
    empty_list(temp_students)
    empty_list(temp_bad_students)
    empty_list(temp_group_GPA)
    df = pd.DataFrame()
    df_help = pd.DataFrame()
    
    
    

def go_to_text():
    file_name = "GPA_Results.txt"
    try:
        notepad_command = f"notepad {file_name}"
        os.system(notepad_command)
    except FileNotFoundError:
        update_text("Error: Could not open the .txt file. Go directly to directory.")

upload_button = tk.Button(window, text="Upload .run File", command=upload_file)
upload_button.pack(pady=20)

txt_button = tk.Button(window,text="Go to text File!",command=go_to_text)
txt_button.pack(pady = 30)

def update_text(text):
    text_box.insert(tk.END, text + "\n")
    text_box.see(tk.END)

text_box = tk.Text(window, width=50, height=70, font=("Arial", 12), wrap="word", borderwidth=2)
text_box.pack(padx=15, pady=20)

update_text("Please select the .RUN file you want to use!")

window.mainloop()

#Use any .run file you want

'''
3 SIGNIFICANT DIGITS

Students should include the Sections where they got the good grades in.

STUDENTS ORDER
- ordered by most A's, alphabetically (so 3 A's alphabetically, 2 A's alphabetically, same with the D's)

'''