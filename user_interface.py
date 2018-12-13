# user_interface.py: pycnumanal text-based user interface system
# 
#    VERSION 0.13
#
#    - text-based menus for:
#
#         - add a program to the database
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
#                      - modified generate_and_add_timings() to have just one line of input
#                        for multiple problem sizes
#
# (pf) Patrick Flynn
#
# ---------------------------------------------------------

import matplotlib.pyplot as plt

# ---------------------------------------------------------

def top_menu() :
    """ Top text menu of the pycnumanal application

        In:  nothing
        Out: nothing
    """

    while 1 :
        print("")
        print("(1) Add a program to the database")
        print("(2) Display all programs in the database")
        print("(3) Manually add a program's timings to the database")
        print("(4) Automatically generate and add a program's timings to the database")
        print("(5) Display a program's timings in the database")
        print("(6) Delete all of a program's timings")
        print("(7) Plot timings for programs")
        print("")

        selection = input("Enter selection number (0 to exit) : ")

        if selection == "0" :    # exit program
            print()
            return

        elif selection == "1" :  # add a program
            add_program()

        elif selection == "2" :  # display all programs
            display_programs()

        elif selection == "3" :  # manually add timings for a program
            manually_add_timings()

        elif selection == "4" :  # automatically generate and add timings 
                                 # for a program
            generate_and_add_timings()

        elif selection == "5" :  # display a program's timings
            choose_program_and_display_timings()

        elif selection == "6" :  # delete all of a program's timings
            delete_program_timings()
            
        elif selection == "7" :  # plot timings for program(s)
            plot_timings()

        else : 
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
    """

    progs = display_programs()
    print()

    # check if any programs were found
    if len(progs) == 0 :
        prog_name = ""  # empty string is indicator that no programs found
    else :
        # choose the program
        prog_num = int( input("Choose the program #: "))

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
    prog_name       = input("New program name : ")
    prog_desc       = input("Description : ")
    cmd_line_prefix = input("Command line prefix (e.g. \"l2vecnorm\") : ")

    main.add_program(prog_name, prog_desc, cmd_line_prefix)

# end function: add_program

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

    # check if any programs were found
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
            prob_size = int( input("Enter problem size (positive integer, 0 to exit) : ") )
            if prob_size == 0 :
                break
            else :
                timing    = float( input("Enter timing (nonnegative decimal) : ") )
                main.add_timing(prog_name, prob_size, timing)

# end function: manually_add_timings

# -----------------------------------------------------------------

def generate_and_add_timings() :
    """ Generate and add program's timings to the database

        In:  nothing
        Out: nothing
    """

    prog_name = choose_program()

    # check if any programs were found
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
        prob_sizes_input = input("Enter problem sizes to generate timings for (e.g., 10 20 30 40): ")
        prob_sizes_input = prob_sizes_input.strip()

        # check if user entered anything
        if prob_sizes_input == "" :
            return
        else :
            prob_sizes = prob_sizes_input.split()
            for prob_size_string in prob_sizes :
                timing = main.generate_and_add_timing(prog_name, int(prob_size_string))
                print("Timing for problem size {} = {:>.6f} seconds".format(prob_size_string, timing))
            print()
                
# end function: generate_and_add_timings

# -----------------------------------------------------------------

def choose_program_and_display_timings() :
    """ Choose a program and display its timings

        In:  nothing
        Out: nothing
    """

    prog_name = choose_program()

    # check if any programs were found
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

    # check if any programs were found
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
    print()

    # choose the programs to plot
    prog_nums = []
    while 1 :
        prog_num = int( input("Enter a program # to plot timings for (0 to stop) : ") )
        if prog_num == 0 : break
        prog_nums.append(prog_num)

    # start up the plot
    fig = plt.figure()
    title = 'Timings vs Problem Size'
    fig.canvas.set_window_title(title) 

    # plot each program's timings by looping through
    # the chosen programs
    prog_names = []
    for prog_num in prog_nums :

        # get current program's info
        prog_info = progs[prog_num-1]
        prog_name = prog_info[0]
 
        timings_info = main.get_timings(prog_name)
        
        # check if current program has any timings
        if len(timings_info) == 0 :  # no timings were found for current program
            print("\nNo timings in database for " + prog_name + " program\n")
            return

        # add current program's name to the list of chosen programs that timings were found for
        prog_names.append(prog_name)

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
