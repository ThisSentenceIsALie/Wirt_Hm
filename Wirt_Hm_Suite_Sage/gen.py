'''
    File name: gen.py
    Dependencies: H3_gens_pruned.xlsx, H4_gens_pruned.xlsx, D4_gens_pruned.xlsx, D5_gen_pruned.xlsx
    Author: Nathaniel Morrison
    Date created: 09/06/2019
    Date last modified: 05/06/2020
    Python Version: 2.7.15
    SageMath version: 8.6
'''
'''
Translates info in the Excel file containing pruned generating sets into a list of sets of Sage matrices
'''
import xlrd
import os
from copy import copy
#Sage does not start out imported, even when running with the sage command wihtin the sage shell, for reasons. So, import everything. It adds like 4 sec to computation time.
from sage.all import *
import platform
#Globally define the varaible "a" to be sqrt(5). I know it's bad form, but defining it globally in every module that could concievably need it seems like the easiest thing
#given that I am not entirely sure how a function would react were it handed a matrix containing a "rational number field" datatype without having that datatype pre-defined
var('x')
K = NumberField(x**Integer(2)-Integer(5), names=('a',)); (a,) = K._first_ngens(1)

#An issue it took me way too long to notice, different OSs have different seperation characters in their directories. So, detect the OS and change character accordingly
if platform.system()=='Windows':
    dir_char="\\"
else:
    dir_char="/"
    
#Grab file with pruned genrators
def file_retriever(grp,g_ord):
    #Get directory of this file; also the directory of the pruned generator list
    dir_path = os.path.dirname(os.path.realpath(__file__))
    myfile=xlrd.open_workbook(dir_path+dir_char+str(grp)+str(g_ord)+"_gens_pruned.xlsx")
    wksht=myfile.sheets()[0]
    return wksht, myfile

#Grab row entry and convert it to a list of sage symbolic expresssions over a finite number field
def entry_processor(gen_str):
    #Define number field
    gen=list()
    del gen[:]
    #Run through each element of the generator matrix list
    for el in gen_str:
        try:
            #Try to turn it into an integer. This will catch all entries that do not have an "a" in them
            gen.append(int(el))
        except:
            #If that dosen't work, this element has an "a" in it. Find the index of the "a"
            a_loc=el.find("a")
            #A big,complcated chain of string transformations which converts the string to a rational expression
            gen.append((Rational(el[0:(a_loc+1)].replace("a","1").replace("*1",""))*a+Rational(el[(a_loc+1):].replace(" ","").lstrip("+"))))
    #Return matrix elements as a list of rational expressions
    return gen

#Function to read the file containing all the generatings sets which survived their respective pruning algorithm
def reader_main(grp,g_ord):
    #Get file containing the gen set info
    wksht, myfile=file_retriever(grp,g_ord)
    #Get total number of rows in file
    tot_rows=wksht.nrows - 1
    #Set current row index
    cur_row = 0
    master=list()
    del master[:]
    gen_set=list()
    gen=list()
    #Run through each row (one row=one generating set)
    while cur_row<=tot_rows:
        del gen_set[:]
        #There are g_ord columns in each row, one for each reflection in the generating set. Run through each of them.
        for i in range(g_ord):
            del gen[:]
            #Grab the entry in the cell, and covnert to a list of strings, each one an element of the matrix
            gen_str=str(wksht.cell(cur_row, i)).lstrip("text:u'[").rstrip("]'").split(", ")
            #Turn the lsit of strings into a list of rational expressions
            gen=entry_processor(gen_str)
            #Turn the list of rational expressions into a sage matrix and add to the genrating set
            gen_set.append(matrix(g_ord,gen))
        #Add generating set to the master set
        master.append(copy(gen_set))
        cur_row+=1
    #Return master set, called pruned_gens in the rest of the programs in this notebook
    return master

#Creates list of all generating transpositions that must be checked of each symeric group
def sym_gen_crafter(all_perms):
    #Defineing all the transpositions generating Sn+1 that must be checked, up to n=4
    s3a=((1,2),(1,3))
    s4a=((1,2),(1,3),(1,4))
    s4b=((1,2),(1,3),(2,4))
    s4c=((1,2),(1,3),(3,4))
    s5a=((1,2),(1,3),(1,4),(1,5))
    s5b=((1,2),(1,3),(1,4),(2,5))
    s5c=((1,2),(1,3),(1,4),(3,5))
    s5d=((1,2),(1,3),(1,4),(4,5))
    s5e=((1,2),(1,3),(2,4),(1,5))
    s5f=((1,2),(1,3),(2,4),(2,5))
    s5g=((1,2),(1,3),(2,4),(3,5))
    s5h=((1,2),(1,3),(2,4),(4,5))
    s5i=((1,2),(1,3),(3,4),(1,5))
    s5j=((1,2),(1,3),(3,4),(2,5))
    s5k=((1,2),(1,3),(3,4),(3,5))
    s5l=((1,2),(1,3),(3,4),(4,5))
    #To generate s6 generatring sets:
    #Create empty lists to house the transposition lists
    master_gen_list_s5=[]
    master_gen_list_s6=[]
    #Run through all the s5 generator sets
    for genor in (s5a,s5b,s5c,s5d,s5e,s5f,s5g,s5h,s5i,s5j,s5k,s5l):
        #Turn each tuple into a list for mutation
        gen_list_s5=list(genor)
        #Add the list version onto the big list of s5 generating sets
        master_gen_list_s5.append(gen_list_s5)
    #Run through all the s5 generating sets, list versions
    for s5_genor in master_gen_list_s5:
        #Run through the five transpositions that need to be tacked on to make s6 generating sets
        for s6_genor in [(1,6), (2,6), (3,6), (4,6), (5,6)]:
            #Create shallow copy of s5 generating set so we don't change the s5 set by accident
            gen_list_s6=copy(s5_genor)
            #Add the current s6 transposition onto the s5 set to create an s6 generating set
            gen_list_s6.append(s6_genor)
            #Add the new s6 generating set onto the big list of s6 generating sets as a tuple
            master_gen_list_s6.append(tuple(gen_list_s6))
    #Convert the whole thing to a tuple to save memory and processing time
    s6_set=tuple(master_gen_list_s6)
    #Put all the sub-tuples into a super-tuple, because you can't have enough tuples
    all_perms[0]=((s3a,), (s4a,s4b,s4c),(s5a,s5b,s5c,s5d,s5e,s5f,s5g,s5h,s5i,s5j,s5k,s5l), s6_set)#the extra comma in the first entry forces (s3a) to be a one-element tuple
    return all_perms

#Function to create a list of all generators of the requested D group that must be checked
def d_gen_crafter(user_wirt, all_perms):
    if user_wirt ==4 or user_wirt==0:
        all_perms[1]=tuple(reader_main("D",4))
    if user_wirt ==5 or user_wirt==0:
        all_perms[2]=tuple(reader_main("D",5))
    return all_perms

#Function to create a list of all generators of the requested H group that must be checked
def h_gen_crafter(wirt_num, all_perms):
    if wirt_num==3 or wirt_num==5:
        all_perms[3]=tuple(reader_main("H",3))
    if wirt_num==4 or wirt_num==5:
        all_perms[4]=tuple(reader_main("H",4))
    return all_perms

