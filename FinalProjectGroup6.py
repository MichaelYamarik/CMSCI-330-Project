import numpy as np
import pandas as pd

# Functions

# # Creating 2D arrays from a group, 2D is for the sections


# function takes in a .RUN file
# # fucntion then reads the groups in the .RUN and adds them to an array that it returns
def ini_GRP(run):   
    data = [run]  
    with open(run) as file:
        line = file.readlines()  
        for x in line:
            x = x.strip()
            if x.endswith('.GRP'):
                data.append(x)
    return np.array(data)

# function takes in a .GRP file
# # function then reads the .GRP for the .SEC and adds them to an array that it returns
def ini_SEC(grp):
    data = [grp]
    with open(grp) as file:
        line = file.readlines()
        for x in line:
            x = x.strip()
            if x.endswith('.SEC'):
                data.append(x)
    return np.array(data)


def grd_val(letterGrade):
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

