import pickle
import sys
import os
import numpy as np

def load_pickle_file(file_name):
    # Get the current script's directory
    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

    # Go up one directory
    parent_dir = os.path.dirname(script_dir)
    
    # Construct the path to the file in the "../models" folder
    file_path = os.path.join(parent_dir, 'models', file_name)
    
    try:
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
            print(f"Loaded data from file: {file_name}")
            return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None


# Load the trained models from files
exploitability_model = load_pickle_file('exploitability_model.pkl')
xcia_model = load_pickle_file('xcia_model.pkl')
xps_model = load_pickle_file('xps_model.pkl')
xsd_model = load_pickle_file('xsd_model.pkl')
xhb_model = load_pickle_file('xhb_model.pkl')


# Exploitability
def calc_exploitability(arr):
    if len(arr) != 4:
        raise ValueError('Input array for exploitability calculation must have 4 values')
    
    if (arr[0] == 1 and arr[1] == 1 and arr[2] == 1 and arr[3] == 1):
        prediction = 10
    elif (arr[0] == 4 and arr[1] == 6 and arr[2] == 3 and arr[3] == 2):        
        prediction = 0.1
    else:
        input = np.array(arr)
        prediction = exploitability_model.predict([input])[0]    
        if (prediction > 10):
            prediction = 10
        elif (prediction < 0):
            prediction = 0
        else:
            prediction = round(prediction, 1)
    
    return prediction


# XCIA
def calc_xcia(arr):

    if len(arr) != 7:
        raise ValueError('Input array for XCIA calculation must have 7 values')
    
    if (arr[0] == 1 and arr[1] == 1 and arr[2] == 1 and arr[3] == 1 and arr[4] == 3 and arr[5] == 3 and arr[6] == 3):
        prediction = 10
    elif (arr[4] == 1 and arr[5] == 1 and arr[6] == 1):        
        prediction = 0
    else:
        input = np.array(arr)
        prediction = xcia_model.predict([input])[0]
        if (prediction > 10):
            prediction = 10
        elif (prediction < 0):
            prediction = 0
        else:
            prediction = round(prediction, 1)

    return prediction


# XPS
def calc_xps(arr):

    if len(arr) != 5:
        raise ValueError('Input array for XPS calculation must have 5 values')
    
    if (arr[0] == 1 and arr[1] == 1 and arr[2] == 1 and arr[3] == 1 and arr[4] == 5):
        prediction = 10
    elif (arr[4] == 1):        
        prediction = 0
    else:
        input = np.array(arr)
        prediction = xps_model.predict([input])[0]
        if (prediction > 10):
            prediction = 10
        elif (prediction < 0):
            prediction = 0  
        else:
            prediction = round(prediction, 1)

    return prediction


#XSD
def calc_xsd(arr):
    
    if len(arr) != 5:
        raise ValueError('Input array for XSD calculation must have 5 values')
    
    if (arr[0] == 1 and arr[1] == 1 and arr[2] == 1 and arr[3] == 1 and arr[4] == 5):
        prediction = 10
    elif (arr[4] == 1):        
        prediction = 0
    else:
        input = np.array(arr)
        prediction = xsd_model.predict([input])[0]        
        if (prediction > 10):
            prediction = 10
        elif (prediction < 0):
            prediction = 0
        else:
            prediction = round(prediction, 1)

    return prediction


#XHB
def calc_xhb(arr):
    
    if len(arr) != 5:
        raise ValueError('Input array for XHB calculation must have 5 values')
    
    if (arr[0] == 1 and arr[1] == 1 and arr[2] == 1 and arr[3] == 1 and arr[4] == 4):
        prediction = 10
    elif (arr[4] == 1):        
        prediction = 0
    else:
        input = np.array(arr)
        prediction = xhb_model.predict([input])[0]
        if (prediction > 10):
            prediction = 10
        elif (prediction < 0):
            prediction = 0
        else:
            prediction = round(prediction, 1)

    return prediction