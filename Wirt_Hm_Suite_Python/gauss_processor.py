'''
    File name: gauss_processor.py
    Author: Nathaniel Morrison
    Date created: 09/01/2019
    Date last modified: 09/02/2019
    Python Version: 3.7.2
'''
#Function to convert gauss code entered to a standard list of integers. Since there are many, many ways to format gauss code, this function just pulls out groups of integers
#from the input code.
def process_gauss_code(raw_gauss_code):
    #Initialize variables
    prev_char_int=0
    cur_entry=''
    code=list()
    #Run through every character in the string version of the gauss code
    for char in raw_gauss_code:
        #Try to convert the character to an integer. If it happens to be a negative, send it on through anyway
        try:
            if char != '-':
                int(char)
        #If that dosen't work, then this character is not part of a code element; it is a beginning, end, or speration character
        except:
            #If the previous character was an integer...
            if prev_char_int==1:
                #Then the current value of cur_entry is a code element. Turn it into a number and stick it in the integer code
                code.append(int(cur_entry))
                #Reset cur_entry
                cur_entry=''
            #Set the value of "was the last entry an integer" to "no"
            prev_char_int=0
        #Otherwise, the character is either an integer or a negative sign
        else:
            #In either case, add it to the current entry
            cur_entry+=char
            #Set the value of "was the last entry an integer" to "yes"
            prev_char_int=1
    #If the end of the gauss code has been reached and there is still a new entry being built...
    if len(cur_entry) !=0:
        #Add that entry to the integer list
        code.append(int(cur_entry))
    #return the integer list version of the code
    return code
