#!/usr/bin/python

'''
IMPORTS:
	angr.Project: Used to create angr project
	claripy.BVS: Passing command line arguments
'''
from angr import Project
from claripy import BVS


def solve():
    '''
    Function Solve:
    1. Create the angr project
    2. Remove Lazy Solves
    3. Set up command line arguments
    4. Explore
    5. Print flag from found path


	Python v2.7.12
	angr v7.7.9.8.post1
	
    Performance:
    Pylint score: 10/10
    Runtime: ~6 seconds
    '''

    # Create the angr project
    proj = Project('./challenge', load_options={"auto_load_libs":False})
    initial_state = proj.factory.entry_state()

    # Discard lazy solves to speed up angr
    initial_state.options.discard("LAZY_SOLVES")

    # Program wants 31 command line arguments
    # The first argument is the program: ./challenge
    # The rest or the arguments are each one byte of the flag
    argument_list = ['./challenge']
    for i in range(0, 30):
        argument_list.append(BVS("argv{}".format(i), 8))

    # Pass arguments to program
    initial_state = proj.factory.entry_state(args=argument_list)

    # Create the path group
    path_group = proj.factory.simgr(initial_state)

    # Address of call to sym.success__ in main. 
    successAddress = 0x400c70

    # Find a path to the desired address
    path_group.explore(find=successAddress)

    # Get first found path
    found = path_group.found[0]

    # For every argument find the value used in the path
    flag = ""
    for arg in argument_list[1:]:
        flag += found.state.se.eval(arg, cast_to=str)

    # Print the result
    print flag

if __name__ == '__main__':
    solve()
