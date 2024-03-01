import numpy as np
import pandas as pd

# Functions

# # Creating 2D arrays from a group, 2D is for the sections

# Function for assigning Groups to RUN files
def create_GRP(run): 
    print(f"\nCurrently Displaying: {run}  ************\n")
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
    print(f"\nCurrently Displaying: {grp}  ************\n")
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
    
    print(f"\nCurrently Displaying: GPA  ************\n")
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
    print(f"GPA of is {(np.sum(summy))/(credit*np.size(summy))}")
    
#function to start the whole thing  

#########    NOT FINAL    ###################
def begin(run):
    #creates an array of the groups 
    array = create_GRP(run)
    print(array)
    for x in array[1:]:
        #creates the group array
        temp = create_SEC(x)
        #prints the current group
        print(temp)
        for y in temp[1:]:
            #creates the section array
            temptwo = create_students(y)
            #prints the current section array
            #print(temptwo)
            #prints the current GPA of the section
            print(calc_SEC_GPA(temptwo))

for x in range(5):
    print("****************************************\n")
#Use any .run file you want


begin("TestRun02.run")