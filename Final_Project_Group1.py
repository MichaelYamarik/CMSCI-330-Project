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

# # FUNCTIONS

# This function creates and array of group variables from the .RUN files.
# Inputs are: a .RUN file
# Outputs are: an array of .GRP files
def create_GRP(run): 
    data = []  
    with open(run) as file:
        line = file.readlines()
        for x in line:
            x = x.strip()
            data.append(x)
    return np.array(data)

# This function creates an array of .SEC files from the .GRP file
# Inputs are: a .GRP file
# Outputs are: an array of .SEC files
def create_SEC(grp):
    data = []
    with open(grp) as file:
        line = file.readlines()
        for x in line:
            x = x.strip()
            data.append(x)
    return np.array(data)

# This function creates students from the .SEC file
# Inputs are: a .SEC file
# Outputs are: an array of students
def create_students(sec):
    data = []
    
    with open(sec, 'r') as file:
        temp = file.readline()
        
        for x in file:
            val = x.strip().strip('"').split('","')
            if len(val) != 3:
                pass
            else:
                data.append(val)
        if temp.strip().endswith('3.0'):
            temp = 3.0
        elif temp.strip().endswith('3'):
            temp = 3.0
        else:
            temp = 4.0
        data.append(temp)
        
    for x in data[:-1]:
        val=x[2]
        point = letter_to_number(val)
        x[2]=point
    return data

# This function converts a lettergrade to a numerical value. all I's W's P's and NP's are converted to None.
# Inputs are: a letter Grade
# Outputs are: a numerical value for the letter grade
def letter_to_number(letterGrade):
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
    return gpaLetter.get(letterGrade,None)

# This function caculates the section GPAs for each section
# Inputs are: An array of students from a section, and the name of the Course
# Outputs are: The section GPA and the amount of credits for the class
def calc_SEC_GPA(array, course):
    global df
    global df_help
    credit = array[-1]
    data = []
    data.append(array[:-1])
    summy = np.empty((0,0))
    for x in data:
        for y in x:
            val = y[2]
            if isinstance(val, float):
                summy = np.append(summy, val)
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
    
# This function empties an array, particularly for emptying the GLOBAL variables after they have been used
# Inputs are: an array
# Outputs are: an empty version of that array
def empty_list(array):
    array.clear()
    
# This function calculates the GPA of the group
# Inputs are: gpas for the section, and the credits for the sections
# Outputs are: the group GPA
def calc_Group_GPA(gpas, creds):
    gps = 0
    chs = 0
    for x, y in zip(gpas, creds):
        temp = x * y
        gps += temp
        chs += y 
    groupGPA = gps / chs
    return groupGPA

# This function starts the full run of things
# Inputs are: a .RUN file
# Outputs are: 
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

# this section sets up the User interface
# this starts the user interface with a var named window
window = tk.Tk()
# title
window.title("GPA Project Calculator")
# size of window
window.geometry("700x350")
run_file = ""

# This function activates when the user presses the upload file button
# Inputs are: None
# Outputs are: None
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
    
# This function opens up the created text file for the project
# Inputs are: None
# Outputs are: None
def go_to_text():
    file_name = "GPA_Results.txt"
    try:
        notepad_command = f"notepad {file_name}"
        os.system(notepad_command)
    except FileNotFoundError:
        update_text("Error: Could not open the .txt file. Go directly to directory.")

# Button for uploading the .RUN file
upload_button = tk.Button(window, text="Upload .run File", command=upload_file)
upload_button.pack(pady=20)

# Button for going to the .txt file
txt_button = tk.Button(window,text="Go to text File!",command=go_to_text)
txt_button.pack(pady = 30)

# This function updates the text in the text box on the bottom
# Inputs are: text to update
# Outputs are: Shows text on screen
def update_text(text):
    text_box.insert(tk.END, text + "\n")
    text_box.see(tk.END)

# This is the text box that gets updated
text_box = tk.Text(window, width=50, height=70, font=("Arial", 12), wrap="word", borderwidth=2)
text_box.pack(padx=15, pady=20)
update_text("Please select the .RUN file you want to use!")

# This starts the main loop for everything in the GUI
window.mainloop()