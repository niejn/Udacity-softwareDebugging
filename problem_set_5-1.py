#!/usr/bin/env python
import sys
import math
# INSTRUCTIONS !
# This provided, working code calculates phi coefficients for each code line.
# Make sure that you understand how this works, then modify the traceit 
# function to work for function calls instead of lines. It should save the 
# function name and the return value of the function for each function call. 
# Use the mystery function that can be found at line 155 and the
# test cases at line 180 for this exercise.
# Modify the provided functions to use this information to calculate
# phi values for the function calls as described in the video.
# You should get 3 phi values for each function - one for positive values (1),
# one for 0 values and one for negative values (-1), called "bins" in the video.
# When you have found out which function call and which return value type (bin)
# correlates the most with failure, fill in the following 3 variables,
# Do NOT set these values dynamically.

# Steps taken:
# =================
# 1. Start from scratch copying and modifying the provided functions one by 
#    one (this makes it easier and cleaner) - start with the mystery function and 
#    inputs as these aren't modified
# 2. Modify traceit
# 3. Modify run_tests
# 4. Modify init_tables
# 5. Copy phi and modify print_tables
# 6. Modify compute_n
# 
# 
# 

answer_function = "f3"   # One of f1, f2, f3
answer_bin = -1         # One of 1, 0, -1
answer_value = 0.8165   # precision to 4 decimal places.

###### MYSTERY FUNCTION

def mystery(magic):
    assert type(magic) == tuple
    assert len(magic) == 3
    
    l, s, n = magic
    
    r1 = f1(l)
    
    r2 = f2(s)
    
    r3 = f3(n)

    if -1 in [r1, r2, r3]:
        return "FAIL"
    elif r3 < 0:
        return "FAIL"
    elif not r1 or not r2:
        return "FAIL"
    else:
        return "PASS"


# These are the input values you should test the mystery function with
inputs = [([1,2],"ab", 10), 
          ([1,2],"ab", 2),
          ([1,2],"ab", 12),
          ([1,2],"ab", 21),
          ("a",1, [1]),
          ([1],"a", 1),
          ([1,2],"abcd", 8),
          ([1,2,3,4,5],"abcde", 8),
          ([1,2,3,4,5],"abcdefgijkl", 18),
          ([1,2,3,4,5,6,7],"abcdefghij", 5)]

def f1(ml):
    if type(ml) is not list:
        return -1
    elif len(ml) <6 :
        return len(ml)
    else:
        return 0
    
def f2(ms):    
    if type(ms) is not str:
        return -1
    elif len(ms) <6 :
        return len(ms)
    else:
        return 0

def f3(mn):
    if type(mn) is not int:
        return -1
    if mn > 10:
        return -100
    else:
        return mn

# global variable to keep the coverage data in
coverage = {}

# Tracing function that saves the coverage data
# To track function calls, you will have to check 'if event == "return"', and in 
# that case the variable arg will hold the return value of the function,
# and frame.f_code.co_name will hold the function name
def traceit(frame, event, arg):
    global coverage

    if event == "return":
        if frame.f_code.co_name == "f1" or frame.f_code.co_name == "f2" or frame.f_code.co_name == "f3":
            coverage[frame.f_code.co_name] = arg
        
    return traceit

# Run the program with each test case and record 
# input, result and coverage of functions
def run_tests(inputs):
    runs   = []
    for input in inputs:
        global coverage
        coverage = {}
        sys.settrace(traceit)
        result = mystery(input)
        sys.settrace(None)
        runs.append((input, result, coverage))
    return runs

# Compute n11, n10, etc. for each function, first categorising
# the result of the function (01, 0, 1)
# TO BE AMENDED AS CURRENTLY ONLY WORKING FOR INTEGER RESULTS
def compute_n(tables):
    for input, outcome, coverage in runs:        
        for fun, value in coverage.iteritems():
            #print fun, value
            category = ""

            if value > 0:
                category = '1'
            elif value == 0:
                category = '0'
            else:
                category = '-1'
            
            # DO FOR LIST, STRING, SET

            # DO FOR BOOLEAN

            # DO NAN and NONE and EXCEPTIONS

            for categories in tables[fun]:
                n11, n10, n01, n00 = tables[fun][categories]
                if categories == category:
                    if outcome == 'FAIL':
                        n11 += 1 # this category and fail
                    else:
                        n10 += 1 # this category and pass
                else:
                    if outcome == 'FAIL':
                        n01 += 1 # complement and fail
                    else:
                        n00 += 1 # complement and pass

                tables[fun][categories] = (n11, n10, n01, n00)
    return tables
     

# Create dictionary of empty tuples for each function
# for each function there are three categories (less than zero, zero, greater than zero)
def init_tables(runs):
    tables = {}
    for (input, outcome, coverage) in runs:
        for fun in coverage:
            tables[fun] = {'-1': (0,0,0,0), '0': (0,0,0,0), '1': (0,0,0,0)}
    return tables

# Calculate phi coefficient from given values            
def phi(n11, n10, n01, n00):
    return ((n11 * n00 - n10 * n01) / 
             math.sqrt((n10 + n11) * (n01 + n00) * (n10 + n00) * (n01 + n11)))

# Print out values of phi, and result of runs for each function 
# and category of function (-1, 0, 1)
# Also calculates the answer (the function and category with the greatest coefficient)
def print_tables(tables):
    answer = {"max_factor": 0, "function": "", "category": ""}
    for fun in tables:
        for category, res in tables[fun].iteritems():
            (n11, n10, n01, n00) = res
            try:
                factor = phi(n11, n10, n01, n00)
                if factor > answer["max_factor"]:
                    answer["max_factor"] = factor
                    answer["category"] = category
                    answer["function"] = fun
                prefix = "%+.4f%2d%2d%2d%2d" % (factor, n11, n10, n01, n00)
            except:
                prefix = "       %2d%2d%2d%2d" % (n11, n10, n01, n00)
            print prefix, fun, category
    print "Answer function = ", answer["function"]
    print "Answer bin = ", answer["category"]
    print "Answer value = %.4f" % answer["max_factor"]


runs = run_tests(inputs)
tables = init_tables(runs)
tables = compute_n(tables)
print_tables(tables) 