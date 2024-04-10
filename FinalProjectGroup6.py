import numpy as np
import pandas as pd
from collections import Counter
import tkinter as tk
from tkinter import filedialog
import os
# Functions

#globals

temp_sec = []

temp_students = []

temp_bad_students = []

# # Creating 2D arrays from a group, 2D is for the sections

# Function for assigning Groups to RUN files
def create_GRP(run): 
    #print(f"\nCurrently Displaying: {run}  ************\n")
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
    #print(f"\nCurrently Displaying: {grp}  ************\n")
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
    
    
    #print(f"\nCurrently Displaying: {sec}  ************\n")
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
def calc_SEC_GPA(array):
    
    #print(f"\nCurrently Displaying: GPA  ************\n")
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
    #prints the GPA of the section
    
    for x in data:
        for y in x:
            temp = y[2]
            if temp is not None:
                if temp >= 3.7:
                    temp_students.append(y[0])
                elif temp <= 1.3:
                    temp_bad_students.append(y[0])
    
    
    
    newGPA = (np.sum(summy))/(credit*np.size(summy))
    
    temp_sec.append(newGPA)
    
    return newGPA
    
    
#function to start the whole thing  

def empty_list(array):
    global temp_sec
    temp_sec.clear()



def remove_non_duplicates(array):
    name_counts = Counter(student[0] for student in array)
    duplicates = [name for name, count in name_counts.items() if count > 1]
    filtered_array = [student for student in array if student[0] in duplicates]
    return filtered_array


#########    NOT FINAL    ###################
def begin(run):
    
    file = open('GPA_Results.txt', 'w')
    
    empty_list(temp_sec)
    #creates an array of the groups 
    array = create_GRP(run)
    
    update_text("Getting the Groups...")
    
    update_text("Calculating the SEC GPA's...")
    
    for x in array[1:]:
        
        file.write(f"****** Now Showing Group {x} ******\n\n")
        
        #creates the group array
        temp = create_SEC(x)
        #prints the current group
        print(temp)
        count = 0
        temp_sum = 0
        std_dev = 0
        sec_gps = []
        empty_list(temp_sec)
        for y in temp[1:]:
            #creates the section array
            temptwo = create_students(y)
            #prints the current section array
            #print(temptwo)
            #prints the current GPA of the section
            sectempgpa = calc_SEC_GPA(temptwo)
            sec_gps.append(sectempgpa)
            temp_sum = sum(temp_sec)
            count = count + 1
            temp_sum = temp_sum / count
            std_dev = np.std(temp_sec)
            #print(f"Section {y}'s GPA is {sectempgpa}")
            #print(f"Current Group, {x}'s GPA is {temp_sum }")
        file.write(f"\nThe GPA of group {x} is: {round(temp_sum,3)}\n\n")
        newtemp = create_SEC(x)
        newcount = 0
        for g in newtemp[1:]:
            print(g)
            empty_list(temp_sec)
            newsectemp = sec_gps[newcount]
            newcount = newcount + 1
            z_score = (newsectemp - temp_sum) / std_dev
            file.write(f"\nSection {g}'s GPA is {round(newsectemp,3)}") 
            if z_score >= 2 or z_score <= -2:
                file.write(f" and the relevant Z-Score is {round(z_score,2)}")
            else:
                file.write(".")

        file.write("\n\n")
    
    update_text("Getting Relevant Students...")
    
    important_Students = remove_non_duplicates(temp_students)
    help_students = remove_non_duplicates(temp_bad_students)
    
    update_text("Printing...")
    
    file.write(f"\nHere are the students with more than one A-, A\n")
    for x in important_Students:
        file.write(f"{x}\n")
        
    file.write(f"\nHere are the students with more than one D+, D, D-, F\n")
    for x in help_students:
        file.write(f"{x}\n")
        
    update_text("DONE! Please go to the file location of the .RUN file for the .txt file!")
    
    

window = tk.Tk()
window.title("GPA Project Calculator")
window.geometry("700x350")

run_file = ""

def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Runnable Files", "*.run")])
    print("Selected file:", file_path)
    run_file = file_path
    begin(run_file)


def go_to_text():
    file_name = "GPA_Results.txt"
    try:
        notepad_command = f"notepad {file_name}"
        os.system(notepad_command)
    except FileNotFoundError:
        update_text("Error:File not found! Contact Distributor.")
    

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
