'''
    File name: Wirt_Hm_Suite_Master.py
    Dependencies: gen.py, hm.py, excel_reader.py, calc_wirt.py, gauss_processor.py, H3_gen_sets_pruned.xlsx, H4_gen_sets_pruned.xlsx, D4_gen_sets_pruned.xlsx,
                  D5_gen_sets_pruned.xlsx
    Author: Nathaniel Morrison
    Date created: 09/01/2019
    Date last modified: 05/04/2020
    Python Version: 2.7.15 (Should work with Python 3.x as well)
    Sage Version: 8.6
'''

'''
This program is designed to provide a more intuitve UI and collect all the Wirtinger coloring-based algorithms into one master program.
'''

import calc_wirt, hm, gen, excel_reader, gauss_processor
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
    print("4.     Search for a surjective homomorphism to an H group")
    print("5.     Search for a surjective homomorphism to any of the symmetric, D, and/or H groups")
    print("6.     Quit")
    choice=raw_input("Please enter your selection: ")
    while choice!="1" and choice!="2" and choice!="3" and choice!="4" and choice!="5" and choice!="6":
        choice=raw_input("You have not selected a valid menu choice. Please enter a number between 1 and 6: ")
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
    while choice != 6:
        choice2, data=menu2()
        if choice2 == 1:
            all_perms=[0,0,0,0,0]
            gauss_code= gauss_processor.process_gauss_code(data)
            knot_dict, seed_strand_set, wirt_num = calc_wirt.wirt_main(gauss_code)
            print("Wirtinger number: "+ str(wirt_num))
            print("Seed strand set used to color the knot: ")
            print(seed_strand_set)
            print("Knot dictionary: ")
            print(knot_dict)
            hmorph_sym=False
            hmorph_d=False
            hmorph_h=False
            no_sym=False
            no_d=False
            no_h=False
            if wirt_num<=5 and wirt_num>=2:
                if (choice==2 or choice==5):
                    all_perms_s=gen.sym_gen_crafter(all_perms)[0]
                    hmorph_sym, sym_gen_set = hm.homomorphism_finder(seed_strand_set, knot_dict, wirt_num, all_perms_s[(wirt_num-2)])
            elif choice ==2 or choice == 5:
                no_sym=True
            if wirt_num == 4 or wirt_num == 5:
                if (choice==3 or choice==5):
                    all_perms_d=gen.d_gen_crafter(wirt_num, all_perms)[(wirt_num-3)]
                    hmorph_d, cox_gen_set = hm.homomorphism_finder(seed_strand_set, knot_dict, wirt_num, all_perms_d)
                    cox_gen_set=hm.cox_writer(cox_gen_set)
            elif choice==3 or choice==5:
                no_d=True
            if wirt_num == 3 or wirt_num == 4:
                if (choice==4 or choice==5):
                    all_perms_h=gen.h_gen_crafter(wirt_num,all_perms)[wirt_num]
                    hmorph_h, h_gen_set = hm.homomorphism_finder(seed_strand_set, knot_dict, wirt_num, all_perms_h)
                    h_gen_set=hm.cox_writer(h_gen_set)
            elif choice==4 or choice==5:
                no_h=True
            if hmorph_sym:
                print("A surjective homomorphism to the S_"+str(wirt_num+1)+" group was found.")
                print("Seed strand to S group generating set mapping: ")
                print(sym_gen_set)
            elif no_sym:
                print("This program cannot conduct a search for surjective homomorphisms to the S_"+str(wirt_num+1)+" group.")
            elif choice==2 or choice==5:
                print("No surjective homomorphism to the S_"+str(wirt_num+1)+" group was found.")
            if hmorph_d:
                print("A surjective homomorphism to the D_"+str(wirt_num)+" group was found.")
                print("Seed strand to D group generating set mapping: ")
                print(cox_gen_set)
            elif no_d:
                print("This program cannot conduct a search for surjective homomorphisms to a D group of Coxeter rank "+str(wirt_num))
            elif choice==3 or choice==5:
                print("No surjective homomorphism to the D_"+str(wirt_num)+" group was found.")
            if hmorph_h:
                print("A surjective homomorphism to the H_"+str(wirt_num)+" group was found.")
                print("Seed strand to H group generating set mapping: ")
                print(h_gen_set)
            elif no_h:
                print("This program cannot conduct a search for surjective homomorphisms to an H group of Coxeter rank "+str(wirt_num))
            elif choice==4 or choice==5:
                print("No surjective homomorphism to the H_"+str(wirt_num)+" group was found.")
        else:
            excel_reader.excel_main(data, choice)
        choice = menu1()
    print("You have elected to quit. This program will now terminate.")
main()
