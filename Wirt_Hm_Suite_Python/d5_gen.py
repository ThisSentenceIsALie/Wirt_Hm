'''
    File name: d5_gen.py
    Dependencies: D5_gens_pruned.txt
    Author: Nathaniel Morrison
    Date created: 01/17/2019
    Date last modified: 09/02/2019
    Python Version: 3.7.2
'''

'''
Generates an exhaustive list of all minimal generating sets of reflections of the D5 Coxeter group
'''

from itertools import combinations, permutations
import numpy as np
import os

class D5Gen:
    
    def __init__(self):
        self.__gen_set_master= list()
        
    #Function to retrieve the list of 42448 minimal generating sets from file produced in Sage
    def retriever(self):
       #Get directory of this file; also the directory of the pruned generator list
        dir_path = os.path.dirname(os.path.realpath(__file__))
        #Open said file
        generator_file=open(dir_path+'\\D5_gens_pruned.txt', 'r')
        #Read the contents of said file, covnerting them into one long string
        content=generator_file.read()
        #Return the string
        return content

    #Function to turn the string retrieved from the text file into a list of lists of numpy arrays
    def formater(self, content):
        #Initialize previous character as the empty string
        char_prev=""
        #Iterator to keep track of how many elements are in one row
        n=0
        #Iterator to keep track of how many rows are in one matrix
        m=0
        #Iterator to keep track of how many matrices are in one set
        i=0
        #Create master list to store all the generating sets
        self.__gen_set_master=list()
        #Define list to hold one row's worth of elements
        single_row=list()
        #Clear said list
        del single_row[:]
        #Define list to hold one matrix's worth of elements
        single_matrix=list()
        #Clear said list
        del single_matrix[:]
        #Define list to hold a single four-matrix generating set
        single_set=list()
        #Clear said list
        del single_set[:]
        for char in content:
            #If character is a number...
            if char.isdigit():
                #If, additionally, the previous character was a dash...
                if (char_prev+char)=="-1":
                    #Append a -1 to the current matrix list
                    single_row.append(int(char_prev+char))
                #Or, similarly...
                elif (char_prev+char)=="-2":
                    #Append a -2 to the current matrix list
                    single_row.append(int(char_prev+char))
                #If the previous character was not a dash...
                else:
                    #Append the integer version of the character tot he current matrix list
                    single_row.append(int(char))
                #In either case, add one to number of elements in row
                n+=1
                #If five elements have been added to the row...
                if n==5:
                    #Add this row to the matrix, making a shallow copy by slicing
                    single_matrix.append(single_row[:])
                    #Add one to the number of rows
                    m+=1
                    #Reset number of elements in row
                    n=0
                    #Reset row list
                    del single_row[:]
                #If five rows have been added to the matrix...
                if m==5:
                    #Convert the matrix to a numpy array and add the the set, making a shallow copy by slicing
                    single_set.append(np.array(single_matrix[:]))
                    #Add one to the number of matrices
                    i+=1
                    #Reset number of rows
                    m=0
                    #Reset matrix
                    del single_matrix[:]
                #If five matrices have been added to the set...
                if i==5:
                    #Add the set to the master list of generating sets, making a shallow copy by slicing
                    self.__gen_set_master.append(single_set[:])
                    #Reset number of matrices
                    i=0
                    #Reset the set
                    del single_set[:]
            char_prev=char
        #Return a list of 42448 lists of five numpy arrays
        return self.__gen_set_master

    #Function to be the main
    def d5gen_main(self):
        #Get the reflections that will be used
        content = self.retriever()
        #Get the exhaustive list of minimal generating sets
        self.__gen_set_master=self.formater(content)
        return self.__gen_set_master
