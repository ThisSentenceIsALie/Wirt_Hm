'''
    File name: Wirt_Hm_Suite_Master.py
    Dependencies: d4_gen.py, d5_gen.py, calc_wirt.py, sym_hm.py, d_hm.py, excel_reader.py, gauss_processor.py, D4_gens_pruned.txt, D5_gens_pruned.txt
    Author: Nathaniel Morrison
    Date created: 09/01/2019
    Date last modified: 03/18/2020
    Python Version: 3.7.2, but should work in any version since 2.7
'''

'''
This program is designed to provide a more intuitve UI and collect all the Wirtinger coloring-based algorithms into one master program.
'''

import calc_wirt, sym_hm, d_hm, excel_reader, gauss_processor
import sys
#In Python 2, which a lot of people still use because it's integrated into Linux and Sage and a host of other OSes and programs, the functionality provided by input() in
#Python 3 is instead provided by raw_input(). To make this program compatible with either version, define raw_input() to be input() if we're in Python 3, and use raw_input()
#in place of input() throughout the code.
if sys.version_info[0]==3:
    def raw_input(prompt):
        return input(prompt)
    
def menu1():
    print("Welcome to the Wirtinger coloring algorithms suite. Please select an option from the menu:")
    print("1.     Compute Wirtinger number")
    print("2.     Search for a surjective homomorphism to a symmetric group")
    print("3.     Search for a surjective homomorphism to a D group")
    print("4.     Quit")
    choice=raw_input("Please enter your selection: ")
    while choice!="1" and choice!="2" and choice!="3" and choice!="4":
        choice=raw_input("You have not selected a valid menu choice. Please enter a number between 1 and 5: ")
    return int(choice)

def menu2():
    choice2=raw_input("Enter 1 if you would like to input the Gauss code of a single knot or 2 if you would like to input an Excel file: ")
    while choice2!="1" and choice2!="2":
        choice2=raw_input("You have not selected a valid choice. Please enter 1 or 2: ")
    if choice2 =="1":
        data=raw_input("Enter the gauss code of the knot as a sequence of integers. Use any seperation characters you like: ")
    else:
        data=raw_input("Enter the input file path (including directory and extension): ")
    return int(choice2), data

def main():
    choice=menu1()
    while choice != 4:
        if choice == 1:
            choice2, data=menu2()
            if choice2 == 1:
                gauss_code= gauss_processor.process_gauss_code(data)
                knot_dict, seed_strand_set, wirt_num = calc_wirt.wirt_main(gauss_code)
                print("Wirtinger number: ", wirt_num)
                print("Seed strand set used to color the knot: ")
                print(seed_strand_set)
                print("Knot dictionary: ")
                print(knot_dict)
            else:
                  excel_reader.excel_main(data, choice)
            choice = menu1()
        elif choice == 2:
            choice2, data=menu2()
            if choice2 == 1:
                gauss_code= gauss_processor.process_gauss_code(data)
                knot_dict, seed_strand_set, wirt_num = calc_wirt.wirt_main(gauss_code)
                transpositions=sym_hm.sym_group_crafter()
                hmorph, sym_gen_set = sym_hm.homomorphism_finder(seed_strand_set, knot_dict, wirt_num, transpositions)
                print("Wirtinger number: ", wirt_num)
                print("Seed strand set used to color the knot: ")
                print(seed_strand_set)
                print("Knot dictionary: ")
                print(knot_dict)
                if hmorph:
                    print("A surjective homomorphism to the S_"+str(wirt_num+1)+" group was found.")
                    print("Seed strand to symmetric group generating set mapping: ")
                    print(sym_gen_set)
                else:
                    print("No surjective homomorphism to the S_"+str(wirt_num+1)+" group was found.")
            else:
                  excel_reader.excel_main(data, choice)
            choice = menu1()
        elif choice ==3:
            choice2, data=menu2()
            if choice2 == 1:
                gauss_code= gauss_processor.process_gauss_code(data)
                knot_dict, seed_strand_set, wirt_num = calc_wirt.wirt_main(gauss_code)
                if wirt_num == 4 or wirt_num == 5:
                    all_perms=d_hm.coxeter_gen_crafter(wirt_num)
                    hmorph, cox_gen_set = d_hm.homomorphism_finder(seed_strand_set, knot_dict, wirt_num, all_perms)
                    print("Wirtinger number: ", wirt_num)
                    print("Seed strand set used to color the knot: ")
                    print(seed_strand_set)
                    print("Knot dictionary: ")
                    print(knot_dict)
                    if hmorph:
                        cox_gen_set_writable=d_hm.cox_writer(cox_gen_set)
                        print("A surjective homomorphism to the D_"+str(wirt_num)+" group was found.")
                        print("Seed strand to d group generating set mapping: ")
                        print(cox_gen_set_writable)
                    else:
                        print("No surjective homomorphism to the D_"+str(wirt_num)+" group was found.")
                elif wirt_num <=3:
                    print("The Wirtinger number of this knot is "+str(wirt_num)+". The D group of this order is isomorphic to the symmetric group of order " + str(wirt_num+1)+".")
                    print("Please select option 2 from the main menu and re-enter the knot information to search for a homomorphism to this group.")
                else:
                    print("The Wirtinger number of this knot is "+str(wirt_num)+". This program currently supports only Wirtinger numbers less than or equal to 5.")
                    print("No search for surjective homomorphisms can be carried out.")
            else:
                  excel_reader.excel_main(data, choice)
            choice = menu1()
    print("You have elected to quit. This program will now terminate.")
main()
