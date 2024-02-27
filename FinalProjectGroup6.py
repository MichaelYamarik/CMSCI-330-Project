import numpy as np
import pandas as pd

# Functions

# # Creating 2D arrays from a group, 2D is for the sections

# Function for assigning Groups to RUN files

def create_GRP(run):   
    data = [run]  
    with open(run) as file:
        line = file.readlines()  
        for x in line:
            x = x.strip()
            if x.endswith('.GRP'):
                data.append(x)
    return np.array(data)

# Functions for assigning Sections to Groups

def create_SEC(grp):
    data = [grp]
    with open(grp) as file:
        line = file.readlines()
        for x in line:
            x = x.strip()
            if x.endswith('.SEC'):
                data.append(x)
    return np.array(data)

# Function for assigning letters to GPA numbers

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

# Calls the functions for createing GRPs and SECs

grp_arr = create_GRP("TESTRUN.RUN")
sec_arr = create_SEC(grp_arr[1])

# Prints out the created arrays, 1st is the filename ($$$.RUN, or $$$.GRP), 2nd is all the data

print(grp_arr)
print(sec_arr)
