'''
    File name: excel_reader.py
    Dependencies: gen.py, hm.py, calc_wirt.py, gauss_processor.py, H3_gen_sets_pruned.xlsx, H4_gen_sets_pruned.xlsx, D4_gen_sets_pruned.xlsx, D5_gen_sets_pruned.xlsx
    Author: Nathaniel Morrison
    Date created: 09/01/2019
    Date last modified: 05/04/2020
    Python Version: 2.7.15 (Should work with Python 3.x as well)
    Sage Version 8.6
'''
import xlsxwriter, sys, xlrd, gauss_processor, hm, calc_wirt, gen
import sys
from itertools import combinations, permutations
from copy import copy
import sys
#In Python 2, which a lot of people still use because it's integrated into Linux and Sage and a host of other OSes and programs, the functionality provided by input() in
#Python 3 is instead provided by raw_input(). To make this program compatible with either version, define raw_input() to be input() if we're in Python 3, and use raw_input()
#in place of input() throughout the code.
if sys.version_info[0]==3:
    def raw_input(prompt):
        return input(prompt)


#Function to pull name and gauss code from Excel sheet
def knot_processor(cur_row, knot_workbook, knot_table, name_col, gauss_col):
    #Call appropriate cell and convert to string object from cell object
    name = str(knot_table.cell(cur_row, name_col))
    #Get rid of prefix
    name = name.lstrip("text:\'")
    name=name.lstrip("u'")
    #Get rid of suffix
    name=name.rstrip("\'")
    #Repeat for gauss code
    raw_gauss_code= str(knot_table.cell(cur_row, gauss_col))
    raw_gauss_code = raw_gauss_code.lstrip("text:\'")
    raw_gauss_code=raw_gauss_code.rstrip("\'")
    #return the name of the knot and the isolated gauss code
    return name, raw_gauss_code

#Function to create the output file
def excel_creator(excel_name, choice):
    #Validate the user's input
    valid_directory=False
    while not valid_directory:
        if excel_name[-5:]!=".xlsx":
            print("It appears that the name you entered for the output Excel file is invalid.")
            excel_name=raw_input("Please re-enter the desired name of excel output file. Make sure the entry ends with the '.xlsx' file suffix: ")
        else:
            valid_directory=True
    #Create an Excel workbook object to store excel version of output
    workbook=xlsxwriter.Workbook(excel_name)
    #Add worksheet attribute within the Excel workbook object to put the data in
    worksheet = workbook.add_worksheet()
    #Enter column titles
    worksheet.write(0, 0, 'Knot Name')
    worksheet.write(0, 1, 'Gauss Notation')
    worksheet.write(0, 2, 'Seed Strand Set')
    worksheet.write(0, 3, 'Wirtinger Number')
    if choice == 2 or choice ==3 or choice ==4:
        worksheet.write(0, 4, 'Homomorphism?')
        worksheet.write(0, 5, 'Seed Strand Maps to Generating Set')
    elif choice ==5:
        worksheet.write(0, 4, 'Homomorphism to S Group?')
        worksheet.write(0, 5, 'Seed Strand Maps to S Group Generating Set')
        worksheet.write(0, 6, 'Homomorphism to D Group?')
        worksheet.write(0, 7, 'Seed Strand Maps to D Group Generating Set')
        worksheet.write(0, 8, 'Homomorphism to H Group?')
        worksheet.write(0, 9, 'Seed Strand Maps to H Group Generating Set')
    #Return worksheet
    return worksheet, workbook

#Function to write data to the output file
def excel_writer(name, seed_strand_with_gauss, knot_dict, raw_gauss_code, wirt_num, gen_set, Knot_Number, worksheet, workbook, choice, hmorph):
    #Write data to worksheet, with the row determined by the Knot_Number accumulator
    worksheet.write(Knot_Number, 0, str(name))
    worksheet.write(Knot_Number, 1, '{' + str(raw_gauss_code) + '}')
    worksheet.write(Knot_Number, 2, str(seed_strand_with_gauss))
    worksheet.write(Knot_Number, 3, wirt_num)
    if choice == 2 or choice == 3 or choice ==4:
        worksheet.write(Knot_Number, 4, str(hmorph))
        worksheet.write(Knot_Number, 5, str(gen_set))
    #If the user wants all possible homomorphisms, hmorph will be a list of 1s and 0s, with the first element being hm to S T/F, second being hm to D T/F,
    #and third being hm to H T/F. Similarly, gen_set will become a list of dictionaries, the first being the mapping to S if an hm was found or 'N/A' if an
    #hm was not found, the second the mapping to D or 'N/A', and the third the mapping to H or 'N/A'
    elif choice==5:
        worksheet.write(Knot_Number, 4, str(hmorph[0]))
        worksheet.write(Knot_Number, 5, str(gen_set[0]))
        worksheet.write(Knot_Number, 6, str(hmorph[1]))
        worksheet.write(Knot_Number, 7, str(gen_set[1]))
        worksheet.write(Knot_Number, 8, str(hmorph[2]))
        worksheet.write(Knot_Number, 9, str(gen_set[2]))
    return

def excel_main(input_name, choice):
    #Get info about input file format. Excel index start at 1 while xlrd index starts at 0, so subtract 1 from all user inputs
    name_col=int(raw_input("Please enter the number of the column containing knot names in the input file (e.g. A=1, B=2, etc): "))-1
    gauss_col=int(raw_input("Please enter the number of the column containing the gauss code in the input file: "))-1
    start_row=int(raw_input("Please enter the number of the row containing the first knot's information: "))-1
    #Get name of output and input files from user
    excel_name=raw_input("Enter desired name of excel output file (include directory and extension): ")
    #Create accumulator to let us keep track of how many knots have had a homomorphism found
    Knot_Number = 1
    #Create a workbook object and worksheet attribute
    worksheet, workbook = excel_creator(excel_name, choice)
    #Validate the user's input
    valid_directory=False
    while not valid_directory:
        try:
            knot_workbook=xlrd.open_workbook(input_name)
            valid_directory=True
        except:
            print("It appears that the input Excel file you entered does not exist.")
            input_name=raw_input("Please re-enter the desired name of excel input file. Make sure to include the full path to the folder in which the file is located as well"+
                                 " as the '.xlsx' file suffix: ")
    #Call first (and only) worksheet in workbook
    knot_table=knot_workbook.sheets()[0]
    #Get total number of rows; since Python index starts at 0, and Excel's starts at 1, subtract 1 from the value .nrows gives
    tot_rows=knot_table.nrows - 1
    #Set current row index
    cur_row = start_row
    #This is a list to house all the algebraic group permutations; first entry is for the symmetric groups, second for D4, third for D5, fifth H3, and sixth H4.
    all_perms=[0,0,0,0,0]
    #Load the appropriate generating set lists based on user selection
    if choice == 2 or choice==5:
        print("Loading symmetric group generating sets...")
        all_perms=gen.sym_gen_crafter(all_perms)
        print("Symetric group generating sets loaded.")
    if choice ==3 or choice==5:
        print("Loading D group generating sets...")
        user_wirt=raw_input("Enter the wirtinger number of the knots you wish to test for D group mappings (only 4 and 5 are supported), or 0 to include both: ")
        while user_wirt !="4" and user_wirt!="5" and user_wirt!="0":
            user_wirt=raw_input("You have not entered a valid number. Please enter either 4, 5, or 0: ")
        user_wirt_D=int(user_wirt)
        if user_wirt_D==4 or user_wirt_D==0:
            all_perms=gen.d_gen_crafter(4, all_perms)
        if user_wirt_D==5 or user_wirt_D==0:
            all_perms=gen.d_gen_crafter(5, all_perms)
        print("D group generating sets loaded.")
    if choice ==4 or choice ==5:
        print("Loading H group generating sets...")
        user_wirt=raw_input("Enter the wirtinger number of the knots you wish to test for H group mappings (only 3 and 4 are supported), or 0 to include both: ")
        while user_wirt !="3" and user_wirt!="4" and user_wirt!="0":
            user_wirt=raw_input("You have not entered a valid number. Please enter either 3, 4, or 0: ")
        user_wirt_H=int(user_wirt)
        if user_wirt_H==3 or user_wirt_H==0:
            all_perms=gen.h_gen_crafter(3, all_perms)
        if user_wirt_H==4 or user_wirt_H==0:
            all_perms=gen.h_gen_crafter(4, all_perms)
        print("H group generating sets loaded.")
    print("Beginning search for surjective homomorphisms...")
    processed_knots=0
    #Until the last row is reached...
    while cur_row <= tot_rows:
        #Parse current row for the name and gauss code
        name, raw_gauss_code = knot_processor(cur_row, knot_workbook, knot_table, name_col, gauss_col)
        #Convert the raw gauss code, a string, into a list of integers.
        gauss_code = gauss_processor.process_gauss_code(raw_gauss_code)
        #Compute the Wirtinger info of the knot
        knot_dict, seed_strand_set, wirt_num = calc_wirt.wirt_main(gauss_code)
        #Set up output version of the seed strand set, complete with the gauss code string of each strand
        seed_strand_with_gauss=dict()
        #Swap out the strand label for the corresponding gauss code segment in the seed strand set. That way, the user can tell which strand it is without the knot_dict.
        for strand in seed_strand_set:
            seed_strand_with_gauss[strand]= knot_dict[strand][0]
        #Knots of wirtinger number greater than 5 are not supported. If a w6 or greater is encountered, no hm search can be performed.
        if wirt_num<=5:
            #Conduct the appropriate hm search(s) based on user selection and knot wirtinger number.
            if choice==2:
                hmorph, gen_set=hm.homomorphism_finder(seed_strand_set, knot_dict, wirt_num, all_perms[0][wirt_num-2])
                if not hmorph:
                    gen_set='N/A'
            elif choice==3:
                hmorph='N/A'
                if (user_wirt_D==4 or user_wirt_D==0) and wirt_num == 4:
                    hmorph, gen_set = hm.homomorphism_finder(seed_strand_set, knot_dict, wirt_num, all_perms[1])
                    gen_set=hm.cox_writer(gen_set)
                elif (user_wirt_D==5 or user_wirt_D==0) and wirt_num == 5:
                    hmorph, gen_set = hm.homomorphism_finder(seed_strand_set, knot_dict, wirt_num, all_perms[2])
                    gen_set=hm.cox_writer(gen_set)
                if hmorph != True:
                    gen_set='N/A'
            elif choice==4:
                hmorph='N/A'
                if (user_wirt_H==3 or user_wirt_H==0) and wirt_num == 3:
                    hmorph, gen_set = hm.homomorphism_finder(seed_strand_set, knot_dict, wirt_num, all_perms[3])
                    gen_set=hm.cox_writer(gen_set)
                elif (user_wirt_H==4 or user_wirt_H==0) and wirt_num == 4:
                    hmorph, gen_set = hm.homomorphism_finder(seed_strand_set, knot_dict, wirt_num, all_perms[4])
                    gen_set=hm.cox_writer(gen_set)
                if hmorph != True:
                    gen_set='N/A'
            #If the user wants to do a universal search, the format is different.
            elif choice==5:
                #Initialize a list of "was an hm found" flags. The first is the S group, the second D, and the third H. Start by assuming no search can be carried out due to
                #the wirtinger number being the wrong value.
                hmorph=['N/A','N/A','N/A']
                #Same as above, but for a list of generating set mappings used to find the above hms.
                gen_set=['N/A','N/A','N/A']
                #Populate the lists
                hmorph[0], gen_set[0]=hm.homomorphism_finder(seed_strand_set, knot_dict, wirt_num, all_perms[0][wirt_num-2])
                if (wirt_num==4 or wirt_num==5) and (user_wirt_D==0 or user_wirt_D==wirt_num):
                    hmorph[1], gen_set_d = hm.homomorphism_finder(seed_strand_set, knot_dict, wirt_num, all_perms[(wirt_num-3)])
                    gen_set[1]=hm.cox_writer(gen_set_d)
                if (wirt_num==3 or wirt_num==4) and (user_wirt_H==0 or user_wirt_H==wirt_num):
                    hmorph[2], gen_set_h = hm.homomorphism_finder(seed_strand_set, knot_dict, wirt_num, all_perms[(wirt_num)])
                    gen_set[2]=hm.cox_writer(gen_set_h)
                #If no hm is found, the homomophism_finder() functions will return the last generating set attempted. Since this is a meaningless value, change the generating
                #set to 'N/A' if no homomorphism was found.
                for i in range(len(hmorph)):
                    if hmorph[i]==False:
                        gen_set[i]='N/A'
            #The program will default here if the user selected option 1. In this case, no hm search is desired, so set hmorph=False because it dosen't matter.
            else:
                hmorph=False
                gen_set='N/A'
        #If the wirtinger number is greater than 5 and the user selected option 5, then put 'N/A' in all hm entries
        elif choice==5:
            hmorph=['N/A','N/A','N/A']
            gen_set=['N/A','N/A','N/A']
        #If the Wirtinger number is greater than 5 and the user selected option 1-4, then put 'N/A' in all hm entries
        else:
            hmorph='N/A'
            gen_set='N/A'
        #Write results to the output Excel file
        excel_writer(name, seed_strand_with_gauss, knot_dict, gauss_code, wirt_num, gen_set, Knot_Number, worksheet, workbook, choice, hmorph)
        processed_knots+=1
        #Let the user know how many knots have been processed
        print("Knots processed: "+str(processed_knots))
        #After printing the above, move the cursor up and clear the output in memory so the next print erases this one
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K")
        Knot_Number+=1
        cur_row+=1
    print("Search complete. Generating output file...")
    #Close the excel file
    workbook.close()
    print("Output file generated. The program is now complete.")
    
        
    
