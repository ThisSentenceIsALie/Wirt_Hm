'''
    File name: hm.py
    Author: Nathaniel Morrison
    Date created: 09/06/2019
    Date last modified: 04/01/2020
    Python Version: 2.7.15
    SageMath Version: 8.6
'''
'''
Searches for a surjective homomorphism from the fundamental group of a given knot to one or more of the S, D, and H finite Coxeter groups.
'''
from itertools import combinations, permutations
from copy import copy
import numpy as np
#Sage does not start out imported, even when running with the sage command wihtin the sage shell, for reasons. So, import everything. It adds like 4 sec to computation time.
from sage.all import *
#Globally define the varaible "a" to be sqrt(5). I know it's bad form, but defining it globally in every module that could concievably need it seems like the easiest thing
#given that I am not entirely sure how a function would react were it handed a matrix containing a "rational number field" datatype without having that datatype pre-defined
var('x')
K = NumberField(x**Integer(2)-Integer(5), names=('a',)); (a,) = K._first_ngens(1)

#Function to search for surjective homomorphisms. Exists primarily to call the other functions in this file.
def homomorphism_finder(seed_strand_set, knot_dict, wirt_num,gen_sets):
    #Get all permutations of the seed strand set
    perms_of_seed_strands=list(permutations(seed_strand_set))
    #Set initial value of "We have found a homomorphism" to "No"
    hmorph=False
    #Run through every generating set in the proper symmetric group
    for gen_set in gen_sets:
        #Run through every permutation of the seed strand set
        for perm in perms_of_seed_strands:
            #Map each seed strand to a generator
            cox_gen_set = generator_assign(wirt_num, perm, gen_set)
            #Map every strand to a generator
            mapping = transposition_assignment(cox_gen_set, knot_dict)
            #Determine if that mapping admits a surjective homomorphism
            hmorph = homomorphism_tester(mapping, knot_dict)
            #If it does...
            if hmorph:
                #Return the Boolean variable indicating that it does and the seed-strand-to-generator mapping that produced it
                return hmorph, cox_gen_set
    #If no hm was found across all permutations, hmorph will be false and we don't care what the program thinks the sym_gen_set is
    return hmorph, cox_gen_set

def generator_assign(wirt_num, perm, gen_set):
    #Defining dictionary to house generating set of transpositions
    cox_gen_set={}
    #run through each element of the permuted seed strand set
    for i in range(len(perm)):
        #Add an entry to the generating set dictionary with the letter of the seed strand from the knot dictionary as the key and the Sn+1 generator as the entry
        cox_gen_set[perm[i]]=gen_set[i]
    #return the generating set, a dictionary with the keys being the seed strand letters and the enries being the Sn+1 generators assigned to them
    return cox_gen_set

#Function to determine whether a given generating set gives a homomorphism to the coxeter group. It's called "transposition" assignment because that's what I called it when I
#was writing the symetric group code and I couldn't be bothered to track down everywhere the function name appears and change it.
def transposition_assignment(cox_gen_set, knot_dict):
    #Create shallow copy of the generating set dictionary
    mapping=cox_gen_set.copy()
    #This variable will indicate when all strands that can be assigned a generator have been assigned a generator
    new_assignment=True
    #While we aren't done
    while new_assignment:
        #This iteration will be the last one unless told otherwise
        new_assignment=False
        #Scan through each overstrand in the knot dictionary
        for overstrand in knot_dict:
            #If the overstrand has been assigned a mapping...
            if overstrand in mapping:
                #Scan through all its understrand pairs (there may be more than one if the strand is the overstrand of more than one crossing)
                for understrands in knot_dict[overstrand][1]:
                    #If both understrands of this particular crossing have been assigned...
                    if understrands[0] in mapping and understrands[1] in mapping:
                        #This crossing has been fully assigned and we're done here
                        pass
                    #If only the first understrand has been assigned...
                    elif understrands[0] in mapping:
                        #Then add the second understrand to mapping, assigning it to a (possibly) new group element
                        mapping[understrands[1]]=transpose_product(mapping[overstrand],mapping[understrands[0]])
                        #A new assignment has been made, so another iteration is necessary to make sure all possible assigments have been made
                        new_assignment=True
                    #If only the second understrand has been assigned...
                    elif understrands[1] in mapping:
                        #Then add the first understrand to mapping, assigning it to a (possibly) new group element
                        mapping[understrands[0]]=transpose_product(mapping[overstrand],mapping[understrands[1]])
                        #A new assignment has been made, so another iteration is necessary to make sure all possible assigments have been made
                        new_assignment=True
                    #Otherwise, neither understrand has yet been assigned a group element, so let another iteration happen
            #Otherwise, the overstrand has not been assigned a mapping yet, and there is nothing we can do yet, so let another iteration happen
    #Return mapping, a dictionary with all strands that can be assigned a group element as keys, and their corresponding numpy array Coxeter group elements as entries.
    return mapping

#Function to test if the mapping given by the (aptly-named) mapping dictionary is a homoporphism from the fundamental group to the Coxeter group
def homomorphism_tester(mapping, knot_dict):
    #If the length of mapping does not equal the length of the knot_dictionary, then something has gone badly wrong and we don't even have a valid generator assignment for
    #for each strand
    if len(mapping) != len(knot_dict):
        #Return a False value
        return False
    #Run through each entry (overstrand) in knot_dict
    for overstrand in knot_dict:
        #scan through all its understrand pairs 
        for understrands in knot_dict[overstrand][1]:
            #If ever one of the understrands' generators (it dosen't matter which understrand, since all the group elements are conveniently involutory. Otherwise, it would)
            #does not equal the transpose product of the overstrand and other understrand, the Wirtinger relation does not hold for this crossing, and this is not a
            #homomorphism.
            try:
                if not np.array_equal(mapping[understrands[0]], transpose_product(mapping[overstrand], mapping[understrands[1]])):
                    #return a False value
                    return False
            #If the above does not work, then the strands are mapped to transpositions, not matrices. So, check via this instead:
            except:
                if set(mapping[understrands[0]]) != set(transpose_product(mapping[overstrand], mapping[understrands[1]])):
                    #Return a False value
                    return False
    #If the function has not been exited yet, then we have a valid homomorphism
    return True
                              
#Function to find product of three matrices as per the Wirtinger relations. It's called "transpose" product because that's what it was called when I was doing the symmetric
#groups and I couldn't be bothered to track down and change every spot where the name appears. Nothing is actually being transposed here.
def transpose_product(overstrands, understrands):
    #If this is a D or H group, then multiply the matrices
    try:
        semiproduct=understrands*overstrands
        product=overstrands*semiproduct
    #If this is a symmetric group, the above commands will make the computer very confused. So, do this instead:
    except:
        #Convert each transposition tuple to a set to make computation easier
        ostrand=set(overstrands)
        ustrand=set(understrands)
        #If the two transpositions are the same...
        if ostrand == ustrand:
            #Then the product is itself
            product=overstrands
        #If the two transpositions have one element in common...
        elif len(ostrand.intersection(ustrand))== 1:
            #Then the product is the symmetric difference (the two elements that are not in both origional transpositions)
            product=tuple(ostrand.symmetric_difference(ustrand)) #note that the product is converted back to a tuple so that it can be iterated over later
        #otherwise, the two transpositions are entirely disjoint
        else:
            #In this case, the product is the understrand
            product=understrands
    return product

#Function to convert array objects into better-looking, formatted string objects for writing to Excel
def cox_writer(cox_gen_set):
    #Create a new dictionary of beutified matrices
    cox_gen_set_writable=dict()
    #Gather a list of the dictionary keys
    cox_keys=list(cox_gen_set.keys())
    #Run through each key
    for key in cox_keys:
        #Create an empty string to house the new matrix
        matrix=''
        #Run through all the rows of the numpy array, which are themselves arrays, after converting the larger array into a tuple
        for array_row in tuple(cox_gen_set[key]):
            #Make it look pretty. Or at least less ugly
            array_row_str=str(tuple(array_row))
            array_row_str=array_row_str.replace('a','sqrt(5)')
            matrix=matrix+array_row_str+"|"
        matrix=matrix.rstrip("|")
        #Reload The Matrix (ba-dum tish!) into the dictionary
        cox_gen_set_writable[key]=matrix
    return cox_gen_set_writable
