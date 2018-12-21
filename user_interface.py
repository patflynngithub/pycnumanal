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
#    - very little error checking
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
#                      - improved some comments
#                      - plot_timings() now checks if any programs found
#
#    12/21/2018 (pf)   - improved top_menu()'s handling of incorrect menu option user input
#                      - improved manually_add_timings()'s handling of incorrect menu option user input
#
# (pf) Patrick Flynn
#
# ======================================================================================

import matplotlib.pyplot as plt

# ======================================================================================
#
#    Utility functions
#

# -----------------------------------------------------------------

def get_ints_from_input(prompt) :
    """ Prompts for an input string of integers and returns a list of integers

        In:  prompt    - the prompt for the input
        Out: ints_list - list of integers input by the user (could be an empty list)
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
        Out: floats_list - list of floats input by the user (could be an empty list)
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
        selection_list = get_ints_from_input("Enter menu option number (0 to exit) : ")

        # check to see if any input or invalid input
        if selection_list == [] or len(selection_list) > 1 :
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
        Out: progs - all programs in database (list of tuples)
    """

    progs = main.get_programs()
    print()

    # check if any programs were found
    if len(progs) == 0 :
        print("No programs in database")
    else : # display all programs found
        print
        print("\t\tPrograms in database")
        print()
        print("    Name                 Description                    Command line prefix")
        print("    -------------------- ------------------------------ --------------------")

        k = 1
        for prog_info in progs :
            print("{:>2d}) {:<20s} {:<30s} {:<20s}".format(k, prog_info[0], prog_info[1], prog_info[2]))
            k = k + 1

        print

    return progs

# end function: display_programs

# -----------------------------------------------------------------

def choose_program() :
    """ Choose a program from the database

        In:  nothing
        Out: prog_name - name of chosen program
             (return "" means no program chosen, for whatever reason)
    """

    progs = display_programs()
    print()

    # check if any programs were found
    if len(progs) == 0 :
        prog_name = ""  # empty string is indicator that no programs found
    else :
        # choose the program
        prog_num = get_ints_from_input("Choose the program #: ")
        # is it a single program #?
        if prog_num == [] or len(prog_num) > 1 :
            prog_name = ""
        else :
            prog_num = prog_num[0]
            # is program # in the correct range? (1 - # of programs)
            if prog_num < 1 or prog_num > len(progs) :
                prog_name = ""
            else :
                # extract desired information for chosen program
                prog_info = progs[prog_num-1]
                prog_name = prog_info[0]
        
    return prog_name

# end function: choose_program
    
# -----------------------------------------------------------------

def add_program() :
    """ Add a new program to the database

        In:  nothing
        Out: nothing
    """

    display_programs()
    print()
    
    # user inputs new program info
    print("Enter BLANK line to cancel")
    
    prog_name       = input("New program name : ").strip()
    if prog_name == "" : return

    prog_desc       = input("Description : ").strip()
    if prog_desc == "" : return

    cmd_line_prefix = input("Command line prefix (e.g. \"l2vecnorm\") : ").strip()
    if cmd_line_prefix == "" : return

    main.add_program(prog_name, prog_desc, cmd_line_prefix)
    print()
    print("Program \"{}\" added.".format(prog_name))

# end function: add_program

# -----------------------------------------------------------------
def delete_program() :
    """ Delete a program (and its timings)

        In:  nothing
        Out: nothing
    """

    prog_name = choose_program()

    # check if a program was selected
    if prog_name == "":
        return
    else :
        main.delete_program(prog_name)
        print()
        print("Program \"{}\" deleted.".format(prog_name))
        
# end function: delete_program

# -----------------------------------------------------------------

def display_timings(prog_name, timings) :
    """ Display all of a program's timings in the database

        In:  prog_name - name of the program displaying timings for (string)
             timings   - all timings for the given program (list of 2-tuples)
        Out: nothing
    """

    print()
    print("     \"" + prog_name + "\" timings in database")
    print()
    print("  Problem size   Timing")
    print("  ------------   ---------------")

    for timing_info in timings :
        print("  {:<12d}   {:>15.6f}".format(timing_info[0], timing_info[1]))

    print()

# end function: display_timings

# -----------------------------------------------------------------

def manually_add_timings() :
    """ Manually add a program's timings to the database

        In:  nothing
        Out: nothing
    """

    prog_name = choose_program()

    # check if a program was chosen
    if prog_name == "":
        return
    else :
        timings  = main.get_timings(prog_name)
        
        # check if any timings were found
        if len(timings) == 0 :
            print()
            print(prog_name, "has no timings in database")
        else :
            display_timings(prog_name, timings)

        while 1 :
            # user manually inputs a new program size amd timing for the program
            print()

            prob_size_list = get_ints_from_input("Enter a new problem size (positive integer, BLANK line to exit) : ")

            # check if user entered anything, there was an input error,
            # or more than one program # was entered
            if prob_size_list == [] or len(prob_size_list) > 1 :
                return
            elif prob_size_list[0] <= 0 :
                print("Problem size needs to be > 0")
                return
            else :
                timing_list = get_floats_from_input("Enter a timing (nonnegative decimal, BLANK line to exit) : ")
                
                # check if user entered anything, there was an input error,
                # or more than one timing was entered
                if timing_list == [] or len(timing_list) > 1 :
                    return
                elif timing_list[0] < 0 :
                    print("Timing needs to be >= 0")
                    return                
                else :
                    main.add_timing(prog_name, prob_size_list[0], timing_list[0])
                    print("Timing manually added to database")

# end function: manually_add_timings

# -----------------------------------------------------------------

def generate_and_add_timings() :
    """ Generate and add program's timings to the database

        In:  nothing
        Out: nothing
    """

    prog_name = choose_program()

    # check if a program was selected
    if prog_name == "":
        return
    else :
        timings  = main.get_timings(prog_name)
        
        # check if any timings were found
        if len(timings) == 0 :
            print()
            print(prog_name, "has no timings in database")
        else :
            display_timings(prog_name, timings)

        print()
            
        # user inputs the program sizes to generate timings for
        prob_sizes_list = get_ints_from_input("Enter problem sizes to generate timings for (e.g., 10 20 30 40, BLANK to cancel): ")

        # check if user entered anything or there was an input error
        if prob_sizes_list == [] :
            return
        else :
            for prob_size in prob_sizes_list :
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

    # check if a program was selected
    if prog_name == "":
        return
    else :
        timings  = main.get_timings(prog_name)
        
        # check if any timings were found
        if len(timings) == 0 :
            print()
            print(prog_name, "has no timings in database")
        else :
            display_timings(prog_name, timings)

# end function: choose_and_display_timings

# -----------------------------------------------------------------
def delete_program_timings() :
    """ Delete all of a program's timings

        In:  nothing
        Out: nothing
    """

    prog_name = choose_program()

    # check if a program was selected
    if prog_name == "":
        return
    else :
        # get timings that are being deleted
        timings  = main.get_timings(prog_name)
        
        # check if any timings were found
        num_timings = len(timings)
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
    
    progs = display_programs()
    if len(progs) == 0: return
    print()

    # user inputs the program #'s to plot timings for
    prog_nums_list = get_ints_from_input("Enter program #'s to plot timings for (e.g., 2 3 4): ")

    # check for blank entry or incorrect input
    if prog_nums_list == [] :
        return
    else :
        
        # looping through chosen programs to make sure have at least
        # one set of program timings to plot
        prog_names = []
        progs_timing_info = []
        for prog_num in prog_nums_list :

            # is program # in the correct range? (1 - # of programs)
            if prog_num < 1 or prog_num > len(progs) :
                print("{} is not a valid program #".format(prog_num))
                continue
            
            # get current program's program name
            prog_info = progs[prog_num-1]
            prog_name = prog_info[0]
            
            timings_info = main.get_timings(prog_name)
            
            # check if current program has any timings
            if len(timings_info) == 0 :
                print("Program {} (#{}) has no timings".format(prog_name, prog_num))
            else :
                # add current program's name and timings to prog_names and progs_timing_info,
                # thus indicating that the current program has timings
                prog_names.append(prog_name)
                progs_timing_info.append(timings_info)

        # check to see if ended up with any entered programs
        # that have timings
        if len(prog_names) == 0 :
            print("None of the programs have timings")
        else :
            # start up the plot
            fig = plt.figure()
            title = 'Timings vs Problem Size'
            fig.canvas.set_window_title(title) 

            # plotting the timing curves for the chosen programs
            for timings_info in progs_timing_info :
                # organize current program's timings info for plotting
                sizes   = [timing[0] for timing in timings_info]
                timings = [timing[1] for timing in timings_info]
            
                # plot the current program's timings
                plt.plot(sizes, timings, 'o-')

            # add overall plotting embellishments 
            plt.xlabel('problem size')
            plt.ylabel('timing (seconds)')
            plt.title(title)
            plt.legend(prog_names)
            plt.show()

# end function: plot_timings

# -----------------------------------------------------------------

import pycnumanal as main
