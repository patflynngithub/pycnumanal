# user_interface.py: pycnumanal text-based user interface system
# 
#    VERSION 0.13
#
#    - text-based menus for:
#
#         - add a program to the database
#         - delete a program from the database (and its timings)
#         - display programs in the database
#         - manually enter timings for a program
#         - generate/store timings for a program
#         - display timings for a program
#         - delete all of a program's timings
#         - plot timings for a program
#
#    - runs on Linux (not tested on Windows)
#    - Python 3.x (not tested with Python 2.x)
#    - text-based interface
#    - SQlite (sqlite3) database used for storage
#    - no database operations error checking (as of yet)
#
# --------------------------------------------------------
#
# Change log:
#
#    12/07/2018 (pf)   Version 0.11:
#                      - created this module as part of this version's
#                        "separating the concerns" of the core, database,
#                        and user_interface operations of pycnumanal version 0.10
#                      - added import statement to allow calling of functions in pycnumanal module
#
#    12/08/2018 (pf)   Version 0.12:
#                      - added new functionalities to the overall application
#                          - manually entering in timings for a program
#                          - generating timings for a program
#                          - displaying timings for a program
#                      - added functions to support the above new functionalities
#                          - manually_add_timings()
#                          - choose_program_and_display_timings()
#                          - display_timings()
#                      - eliminated the get_programs() function
#                          - now directly calling main.get_programs()
#
#    12/09/2018 (pf)   Version 0.13:
#                      - added new functionality to the overall application
#                          - plot timings (vs problem size)
#                      - added function to support the above new functionality
#                          - plot_timings()
#
#    THIS CODE IS NOW pycnumanal VERSION, NOT pycnumanal-lessons VERSION
#
#    12/12/2018 (pf)   - added "Delete all of a program's timings" functionality
#                          - added option to top_menu()
#                          - added delete_program_timings()
#                      - professionalized the commenting
#                          - pycnumanal-lessons version has more commenting for the student
#                      - modified generate_and_add_timings() 
#                          - to allow user to use just one line of input to enter multiple 
#                            problem sizes
#
#    12/12/2018 (pf)   - modified plot_timings()
#                          - allow user to use enter one line of input to choose multiple 
#                            programs (program #'s)
#                          - added code and rearranged the logic to better handle chosen
#                            programs that have no timings
#
#    12/19/2018 (pf)   - added get_ints_from_input() to handle the input of 
#                        multiple intetgers in one input string
#                            - modified top_menu() to use it
#                            - modified choose_program() to use it
#                            - modified generate_and_add_timings() to use it
#                            - modified plot_timings() to use it
#
#    12/20/2018 (pf)   - improved add_program()'s handling of user input, allowing cancellation
#                        of input
#                      - added delete_program()
#                      - modified top_menu() to add new delete program option
#                      - improved some comments
#                      - plot_timings() now checks if any programs found
#
#    12/21/2018 (pf)   - improved top_menu()'s handling of incorrect menu option user input
#                      - choose_program(): added to prompt - "BLANK to cancel"
#                      - improved manually_add_timings()'s handling of incorrect menu option user input
#                      - improved some comments
#                      - choose_program(): added print statement about entering invalid program #
#                      - plot_timings(): added logic to check for valid problem sizes (> 0)
#
#    12/21/2018 (pf)   - added checking for existence of executable external program:
#                           - add_program()
#                           - generate_and_add_timings()
#
#    12/22/2018 (pf)   - started process of adding database exception handling
#                           - display_programs()
#
#    12/27/2018 (pf)   - modified add_program()
#                           - logic to check if program already in database
#                      - added prob_size_in_list()
#                           - determines if a problem size is already in a program's list of timings
#                      - modified generate_and_add_timings()
#                           - logic to check if problem size already in database for a program
#                      - modified manually_add_timings()
#                           - logic to check if problem size already in database for a program
#
#    12/28/2018 (pf)   - added yes_or_no()
#                      - modified add_program()
#                           - allow adding of a program even if its executable isn't in current directory
#
#    12/29/2018 (pf)   - changed name of the function get_program_info_from_DB() to get_program_info()
#                      - modified add_program()
#                          - changed call to get_program_info_from_DB() to get_program_info()
#                          - accomodates modifications to main.get_program_info() (and db.get_program_info())
#                              - where data is returned from them with each field's values having their own
#                                separate list rather than each data row having its own list, which is inside
#                                of an overall list
#                              - avoids add_program having to know the ordering (list indices) of entries
#                                in a list inside of the overall list
#
#    12/30/2018 (pf)   - deleted prob_size_in_list() utility function
#                      - modified display_program()
#                                 choose_program()
#                                 display_timings()
#                                 manually_add_timings()
#                                 generate_and_add_timings()
#                                 choose_program_and_display_timings()
#                                 delete_program_timings()
#                                 plot_timings()
#                           - accomodates modifications to main.get_programs() (and db.get_programs())
#                                                          main.get_timings()  (and db.get_timings())
#                               - where data is returned from them with each field's values having their own
#                                 separate list rather than each data row having its own list, which is inside
#                                 of the overall list
#                               - avoids the calling functions (listed above) having to know the ordering (list indices)
#                                 of entries in a list inside of an overall list
#                      - modified top_menu(): except BLANK line to exit program (instead of 0 before)
#                                 
# (pf) Patrick Flynn
#
# ======================================================================================

# standard modules
import os
import sys

# third-party modules
import matplotlib.pyplot as plt
#import traceback   (used with "print(traceback.format_exc())")

# custom modules
import db_exceptions as dbe

# ======================================================================================
#
#    Utility functions
#
# ======================================================================================

# -----------------------------------------------------------------

def yes_or_no(prompt):
    """ Prompts for a yes or no answer

        In:  prompt     - the prompt for the yes/no input
        Out: True/False - is answer a yes?
    """

    answer = input(prompt + " (y/n): ").lower().strip()
    while not(answer == "y" or answer == "yes" or answer == "n" or answer == "no"):
        print("")
        print("Input yes or no")
        answer = input(prompt + " (y/n): ").lower().strip()
    if answer[0] == "y":
        return True
    else:
        return False

# end function: yes_or_no

# -----------------------------------------------------------------

def get_ints_from_input(prompt) :
    """ Prompts for an input string of integers and returns a list of integers

        In:  prompt    - the prompt for the input
        Out: ints_list - list of integers input by the user
                         (empty list indicates no entry or entry error)
    """

    ints_string = input(prompt)
    ints_string_list = ints_string.strip().split()

    ints_list = []
    for int_string in ints_string_list :
      try :
         int_value = int(int_string)
      except ValueError as ex :
         print('Error: "%s" cannot be converted to an integer!' % (int_string))
         return []
      ints_list.append(int_value)

    return ints_list

# end function: get_ints_from_input

# -----------------------------------------------------------------

def get_floats_from_input(prompt) :
    """ Prompts for an input string of floats and returns a list of floats

        In:  prompt      - the prompt for the input
        Out: floats_list - list of floats input by the user
                           (empty list indicates no entry or entry error)

    """

    floats_string = input(prompt)
    floats_string_list = floats_string.strip().split()

    floats_list = []
    for float_string in floats_string_list :
      try :
         float_value = float(float_string)
      except ValueError as ex :
         print('Error: "%s" cannot be converted to a float!' % (float_string))
         return []
      floats_list.append(float_value)

    return floats_list

# end function: get_floats_from_input

# -----------------------------------------------------------------

# ======================================================================================
#
#    Core User Interface functions
#
# ======================================================================================

# -----------------------------------------------------------------

def top_menu() :
    """ Top text menu of the pycnumanal application

        In:  nothing
        Out: nothing
    """

    while 1 :
        print("")
        print("(1) Add a program to the database")
        print("(2) Delete a program from the database")
        print("(3) Display all programs in the database")
        print("(4) Manually add a program's timings to the database")
        print("(5) Automatically generate and add a program's timings to the database")
        print("(6) Display a program's timings in the database")
        print("(7) Delete all of a program's timings")
        print("(8) Plot timings for programs")
        print("")

        # user inputs the menu option #
        selection_list = get_ints_from_input("Enter menu option number (BLANK line to exit) : ")

        # check to see if BLANK entry, or the required ONE entry was not input or the there was an entry error
        if selection_list == [] :
            print()
            return
        elif len(selection_list) > 1 :
            continue
        else :
            selection = selection_list[0]

        if selection == 0 :    # exit program
            print()
            return
        
        elif selection == 1 :  # add a program
            add_program()

        elif selection == 2 :  # delete a program (and its timings)
            delete_program()

        elif selection == 3 :  # display all programs
            display_programs()

        elif selection == 4 :  # manually add timings for a program
            manually_add_timings()

        elif selection == 5 :  # automatically generate and add timings 
                               # for a program
            generate_and_add_timings()

        elif selection == 6 :  # display a program's timings
            choose_program_and_display_timings()

        elif selection == 7 :  # delete all of a program's timings
            delete_program_timings()
            
        elif selection == 8 :  # plot timings for program(s)
            plot_timings()

        else :                 # bad entry
            print("\nBAD ENTRY!")

# end function: top_menu

# -----------------------------------------------------------------

def display_programs() :
    """ Displays all the programs in the database

        In:  nothing
        Out: prog_names        - program names (list)
             descriptions      - program descriptions (list)
             cmd_line_prefixes - command line prefixes (list)        
    """

    try :
        [prog_names, descriptions, cmd_line_prefixes] = main.get_programs()
    except dbe.DB_Error as e :
        print(e)
        # print(traceback.format_exc())
        return []

    print()

    # check if no programs were found
    if len(prog_names) == 0 :
        print("No programs in database")
    else : # display all programs found
        print
        print("\t\tPrograms in database")
        print()
        print("    Name                 Description                    Command line prefix")
        print("    -------------------- ------------------------------ --------------------")

        for k in range(0,len(prog_names)) :
            print("{:>2d}) {:<20s} {:<30s} {:<20s}".format(k+1, prog_names[k], descriptions[k], cmd_line_prefixes[k]))

        print

    return [prog_names, descriptions, cmd_line_prefixes]

# end function: display_programs

# -----------------------------------------------------------------

def choose_program() :
    """ Choose a program from the database

        In:  nothing
        Out: prog_name - name of chosen program
             (return "" (empty string) means no program chosen, for whatever reason)
    """

    [prog_names, descriptions, cmd_line_prefixes] = display_programs()
    print()

    # check if no programs were found
    if len(prog_names) == 0 :
        prog_name = ""  # empty string is indicator that no programs found
    else :
        # choose the program
        prog_num = get_ints_from_input("Choose the program # (BLANK to cancel): ")
        
        # was the required single program # inputed or was there an entry error?
        if prog_num == [] or len(prog_num) > 1 :
            prog_name = ""
        else :
            prog_num = prog_num[0]
            # is program # not in the correct range? (1 - # of programs)
            if prog_num < 1 or prog_num > len(prog_names) :
                prog_name = ""
                print("Invalid program #")
            else :
                # extract program name for chosen program
                prog_name = prog_names[prog_num-1]
        
    return prog_name

# end function: choose_program
    
# -----------------------------------------------------------------

def add_program() :
    """ Add a new program to the database

        In:  nothing
        Out: nothing
    """

    [prog_names, descriptions, cmd_line_prefixes] = display_programs()
    print()

    # loop in case of attempt to add a duplicate program
    while 1 :
    
        # user inputing new program info
        print("Enter BLANK line to cancel")        
        new_prog_name       = input("New program name : ").strip()
        if new_prog_name == "" : return

        # is program already in the database?
        if new_prog_name in prog_names :
            k = prog_names.index(new_prog_name)
            print("PROGRAM IS ALREADY IN THE DATABASE. Delete it if you want to change its info.")
            print("Program : ", prog_names[k])
            print("Description : ", descriptions[k])
            print("Command line prefix : ", cmd_line_prefixes[k])
            print()
            continue

        new_prog_desc       = input("Description : ").strip()
        if new_prog_desc == "" : return

        new_cmd_line_prefix = input("Command line prefix (e.g. \"l2vecnorm\") : ").strip()
        if new_cmd_line_prefix == "" : return
        else:
            # see if there is an executable file of that name
            filepath = './' + new_cmd_line_prefix
            if not os.path.isfile(filepath) :
                print("That executable file doesn't exist in current directory!")
                if not yes_or_no("Do you want to add the program anyway?") :
                    return

        main.add_program(new_prog_name, new_prog_desc, new_cmd_line_prefix)
        print()
        print("Program \"{}\" added.".format(new_prog_name))
        
        break

# end function: add_program

# -----------------------------------------------------------------

def delete_program() :
    """ Delete a program (and its timings)

        In:  nothing
        Out: nothing
    """

    prog_name = choose_program()

    # check if no program was chosen
    if prog_name == "":
        return
    else :
        main.delete_program(prog_name)
        print()
        print("Program \"{}\" deleted.".format(prog_name))
        
# end function: delete_program

# -----------------------------------------------------------------

def display_timings(prog_name, prob_sizes, timings) :
    """ Display all of a program's timings in the database

        In:  prog_name  - name of the program displaying timings for (string)
             prob_sizes - the program's problems sizes (list)
             timings    - the program's timings
        Out: nothing
    """

    print()
    print("     \"" + prog_name + "\" timings in database")
    print()
    print("  Problem size   Timing")
    print("  ------------   ---------------")

    for k in range(0, len(prob_sizes)) :
        print("  {:<12d}   {:>15.6f}".format(prob_sizes[k], timings[k]))

    print()

# end function: display_timings

# -----------------------------------------------------------------

def manually_add_timings() :
    """ Manually add a program's timings to the database

        In:  nothing
        Out: nothing
    """

    prog_name = choose_program()

    # check if no program was chosen
    if prog_name == "":
        return
    else :
        [prob_sizes, timings]  = main.get_timings(prog_name)
        
        # check if no timings were found
        if len(prob_sizes) == 0 :
            print()
            print(prog_name, "has no timings in database")
        else :
            display_timings(prog_name, prob_sizes, timings)

        # each loop is a manual entry of a program size and its accompanying timing
        while 1 :
            print()

            prob_size_input = get_ints_from_input("Enter a new problem size (positive integer, BLANK line to exit) : ")

            # check if user did not enter the required ONE entry or there was an input error
            if prob_size_input == [] or len(prob_size_input) > 1 :
                return
            elif prob_size_input[0] <= 0 :
                print("Problem size needs to be > 0")
                return
            else :
                prob_size = prob_size_input[0]

                # is problem size already in database for the chosen program?
                if prob_size in prob_sizes :
                    print("Problem size already in database for the chosen program")
                    continue
                
                timing_input = get_floats_from_input("Enter a timing (nonnegative decimal, BLANK line to exit) : ")
                
                # check if user did not enter the required ONE entry or there was an input error
                if timing_input == [] or len(timing_input) > 1 :
                    return
                elif timing_input[0] < 0 :
                    print("Timing needs to be >= 0")
                    return                
                else :
                    main.add_timing(prog_name, prob_size, timing_input[0])
                    print("Timing added to database")

# end function: manually_add_timings

# -----------------------------------------------------------------

def generate_and_add_timings() :
    """ Generate and add program's timings to the database

        In:  nothing
        Out: nothing
    """

    prog_name = choose_program()

    # check if no program was selected
    if prog_name == "":
        return
    else :
        # check if external executable program exists in current directory
        cmd_line_prefix = main.get_cmd_line_prefix(prog_name)
        filepath = './' + cmd_line_prefix
        if not os.path.isfile(filepath) :
            print("The \"{}\" external executable file doesn't exist in current directory!".format(cmd_line_prefix))
            return
        
        [prob_sizes, timings]  = main.get_timings(prog_name)
        
        # check if no timings were found for the program
        if len(prob_sizes) == 0 :
            print()
            print(prog_name, "has no timings in database")
        else :
            display_timings(prog_name, prob_sizes, timings)

        print()
            
        # user inputs the program sizes to generate timings for
        prob_sizes_input = get_ints_from_input("Enter problem sizes to generate timings for (e.g., 10 20 30 40, BLANK to cancel): ")

        # check if user entered anything or there was an input error
        if prob_sizes_input == [] :
            return
        else :
            for prob_size in prob_sizes_input :
                if prob_size <= 0 :
                    print("Problem size of {} is invalid".format(prob_size,))
                else :
                    # is problem size already in database for the chosen program?
                    if prob_size in prob_sizes :
                        print("Problem size {} already in database for the chosen program. SKIPPING".format(prob_size))
                        continue
                    
                    timing = main.generate_and_add_timing(prog_name, prob_size)
                    print("Timing for problem size {} = {:>.6f} seconds".format(prob_size, timing))
            print()
                
# end function: generate_and_add_timings

# -----------------------------------------------------------------

def choose_program_and_display_timings() :
    """ Choose a program and display its timings

        In:  nothing
        Out: nothing
    """

    prog_name = choose_program()

    # check if no program was selected
    if prog_name == "":
        return
    else :
        [prob_sizes, timings]  = main.get_timings(prog_name)
        
        # check if no timings were found
        if len(prob_sizes) == 0 :
            print()
            print(prog_name, "has no timings in database")
        else :
            display_timings(prog_name, prob_sizes, timings)

# end function: choose_and_display_timings

# -----------------------------------------------------------------
def delete_program_timings() :
    """ Delete all of a program's timings

        In:  nothing
        Out: nothing
    """

    prog_name = choose_program()

    # check if no program was selected
    if prog_name == "":
        return
    else :
        # get timings that are being deleted
        [prob_sizes, timings]  = main.get_timings(prog_name)
        
        # check if any timings were found
        num_timings = len(prob_sizes)
        if num_timings == 0 :
            print()
            print(prog_name, "has no timings in database")
        else :
            main.delete_program_timings(prog_name)
            print("{}'s {} timings deleted".format(prog_name, num_timings))
            
# end function: delete_program_timings

# -----------------------------------------------------------------

def plot_timings() :
    """ Plot timings for a program

        In:  nothing
        Out: nothing
    """
    
    [prog_names, descriptions, cmd_line_prefixes] = display_programs()
    if len(prog_names) == 0: return

    print()

    # user inputs the program #'s to plot timings for
    prog_nums_input = get_ints_from_input("Enter program #'s to plot timings for (e.g., 2 3 4, BLANK to cancel): ")

    # check for blank entry or input error
    if prog_nums_input == [] :
        return
    else :
       
        # looping through chosen programs to make sure have at least
        # one set of program's timings to plot
        valid_prog_names   = []
        valid_prob_sizes   = []
        valid_prog_timings = []
        for k in range(0,len(prog_nums_input)) :

            prog_num = prog_nums_input[k]
            
            # is program # in the correct range? (1 - # of overall programs)
            if prog_num < 1 or prog_num > len(prog_names) :
                print("{} is not a valid program #".format(prog_num))
                continue
            
            # get current program's program name
            prog_name = prog_names[prog_num-1]
            
            # get current program's timings
            [prob_sizes, timings] = main.get_timings(prog_name)
            
            # check if current program has any timings
            if len(prob_sizes) == 0 :
                print("Program {} (#{}) has no timings".format(prog_name, prog_num))
                continue
            else :
                # add current program's name and timings to prog_names and progs_timing_info,
                # thus indicating that the current program has timings
                valid_prog_names.append(prog_name)
                valid_prob_sizes.append(prob_sizes)
                valid_prog_timings.append(timings)

        # check to see if ended up with any chosen programs
        # that actually have timings
        if len(valid_prog_names) == 0 :
            print("None of the programs have timings")
        else :
            # start up the plot
            fig = plt.figure()
            title = 'Timing vs Problem Size'
            fig.canvas.set_window_title(title) 

            # plotting the timing curves for the chosen programs that actually have timings
            for prob_sizes, timings in zip(valid_prob_sizes, valid_prog_timings) :
            
                # plot the current program's timings
                plt.plot(prob_sizes, timings, 'o-')

            # add overall plotting embellishments 
            plt.xlabel('problem size')
            plt.ylabel('timing (seconds)')
            plt.title(title)
            plt.legend(valid_prog_names)
            plt.show()

# end function: plot_timings

# -----------------------------------------------------------------

import pycnumanal as main
