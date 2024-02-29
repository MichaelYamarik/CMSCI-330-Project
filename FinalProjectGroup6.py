import numpy as np
import pandas as pd

# Functions

# # Creating 2D arrays from a group, 2D is for the sections

# Function for assigning Groups to RUN files
def create_GRP(run): 
    #creates temp array that takes in a run file  
    data = [run]  
    #opens up the file
    with open(run) as file:
        #begins to read lines in file
        line = file.readlines()
        #for loop to loop through the lines  
        for x in line:
            #removes white space
            x = x.strip()
            #checks whether or not a .GRP file exists
            if x.endswith('.GRP'):
                #if exists appends to the data array
                data.append(x)
    #returns the array
    return np.array(data)

# Functions for assigning Sections to Groups
def create_SEC(grp):
    #creates a temp array
    data = [grp]
    #opens the group file
    with open(grp) as file:
        #begins reading lines
        line = file.readlines()
        #for loop to loop through the line
        for x in line:
            #strips the white space
            x = x.strip()
            #checks if there is a section file
            if x.endswith('.SEC'):
                #appends the section file to the temp array
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
        file.readline()
        #for loop
        for x in file:
            #strips the white space and the quotes
            val = x.strip().strip('"').split('","')
            #appends data to the array
            data.append(val)
    #the second for loop is for assigning the letter to number function to the third value of each array column
    for x in data:
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

# Calls the functions for createing GRPs and SECs

grp_arr = create_GRP("TESTRUN.RUN")
sec_arr = create_SEC(grp_arr[1])
stu_gra = create_students(sec_arr[1])

# Prints out the created arrays, 1st is the filename ($$$.RUN, or $$$.GRP), 2nd is all the data

print(grp_arr)
print(sec_arr)
print(stu_gra)
