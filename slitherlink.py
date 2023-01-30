########################################################################################
# Solves slitherlink puzzles from the website https://www.puzzle-loop.com/             #
# Enter the entries for the puzzle into a rectangular array (use e for an empty entry) #
# Errors will occur if entries is not a rectangular array                              #
# The original and solved puzzles are both displayed                                   #
########################################################################################

# Import libraries
import numpy as np
import sys
import copy
from itertools import chain

# Assigns None to e
e = None

# Fill in entries
entries = np.array([
                    [e, 3, 3, 3, e],
                    [1, 2, 0, e, e],
                    [2, e, 2, e, e],
                    [2, e, e, 1, e],
                    [3, 1, 2, 2, e]
                   ])



#####################################################################################
# The entries are stored in an m by n rectangular array                             #
# The dots are stored in an m+1 by n+1 array                                        #
# The links are first split by orientation by horizontal (0) and vertical (1)       #
# The horizontal links are stored in an m+1 by n array                              #
# The vertical links are stored in an m by n+1 array                                #
# Links are recorded by None (no value), 1 (link), 0 (contradiction), -1 (no link)  #
#####################################################################################

#####################
# Display functions #
#####################

# Displays the puzzle with specified links
def  display(links):
    for i in range(m):
        for j in range(n):
            sys.stdout.write("\u25CF")
            if links[0][i][j] == 1:
                sys.stdout.write(" \u2501\u2501\u2501 ")
            elif links[0][i][j] == -1:
                sys.stdout.write("  x  ")
            else:
                sys.stdout.write("     ")
    
        sys.stdout.write("\u25CF\n")

        for j in range(n):
            if links[1][i][j] == 1:
                sys.stdout.write("\u275A")
            elif links[1][i][j] == -1:
                sys.stdout.write("x")
            else:
                sys.stdout.write(" ")
            if entries[i][j] != None:
                sys.stdout.write("  {}  ".format(entries[i][j]))
            else:
                sys.stdout.write("     ")
        
        if links[1][i][n] == 1:
            sys.stdout.write("\u275A\n")
        elif links[1][i][n] == -1:
            sys.stdout.write("x\n")
        else:
            sys.stdout.write("\n")

    for j in range(n):
        sys.stdout.write("\u25CF")
        if links[0][m][j] == 1:
            sys.stdout.write(" \u2501\u2501\u2501 ")
        elif links[0][m][j] == -1:
            sys.stdout.write("  x  ")
        else:
            sys.stdout.write("     ")
    
    sys.stdout.write("\u25CF\n\n")



####################
# Factor functions #
####################

#################
# Entry factors #
#################

def factor_entry(links, components, i, j):
    if not entries[i][j] == None:
        u = links[0][i][j]
        d = links[0][i+1][j]
        l = links[1][i][j]
        r = links[1][i][j+1]
        if entries[i][j] == 0:
            table = [
                        [-1, -1, -1, -1],
                    ]
        if entries[i][j] == 1:
            table = [
                        [1, -1, -1, -1],
                        [-1, 1, -1, -1],
                        [-1, -1, 1, -1],
                        [-1, -1, -1, 1],
                    ]
        if entries[i][j] == 2:
            table = [
                        [1, 1, -1, -1],
                        [1, -1, 1, -1],
                        [1, -1, -1, 1],
                        [-1, 1, 1, -1],
                        [-1, 1, -1, 1],
                        [-1, -1, 1, 1]
                    ]
        if entries[i][j] == 3:
            table = [
                        [1, 1, 1, -1],
                        [1, 1, -1, 1],
                        [1, -1, 1, 1],
                        [-1, 1, 1, 1]
                    ]
        if not u == None:
                table = [row for row in table if row[0] == u]
        if not d == None:
                 table = [row for row in table if row[1] == d]
        if not l == None:
            table = [row for row in table if row[2] == l]
        if not r == None:
            table = [row for row in table if row[3] == r]
        if len(table) == 1:
            add_edge(links, components, 0, i, j, table[0][0])
            add_edge(links, components, 0, i+1, j, table[0][1])
            add_edge(links, components, 1, i, j, table[0][2])
            add_edge(links, components, 1, i, j+1, table[0][3])



###############
# Dot factors #
###############

def factor_intersection(links, components, i, j):
    
    # Top left corner
    if (i == 0) and (j == 0):
        # u = links[1][i-1][j]
        d = links[1][i][j]
        # l = links[0][i][j-1]
        r = links[0][i][j]
        table = [
                    [None, 1, None, 1],
                    [None, -1, None, -1]
                ]
        # if not u == None:
        #     table = [row for row in table if row[0] == u]
        if not d == None:
            table = [row for row in table if row[1] == d]
        # if not l == None:
        #     table = [row for row in table if row[2] == l]
        if not r == None:
            table = [row for row in table if row[3] == r]
        if len(table) == 1:
            # add_edge(links, components, 1, i-1, j, table[0][0])
            add_edge(links, components, 1, i, j, table[0][1])
            # add_edge(links, components, 0, i, j-1, table[0][2])
            add_edge(links, components, 0, i, j, table[0][3])

    # Top edge
    if (i == 0) and (0 < j < n):
        # u = links[1][i-1][j]
        d = links[1][i][j]
        l = links[0][i][j-1]
        r = links[0][i][j]
        table = [
                    [None, 1, 1, -1],
                    [None, 1, -1, 1],
                    [None, -1, 1, 1],
                    [None, -1, -1, -1]
                ]
        # if not u == None:
        #     table = [row for row in table if row[0] == u]
        if not d == None:
            table = [row for row in table if row[1] == d]
        if not l == None:
            table = [row for row in table if row[2] == l]
        if not r == None:
            table = [row for row in table if row[3] == r]
        if len(table) == 1:
            # add_edge(links, components, 1, i-1, j, table[0][0])
            add_edge(links, components, 1, i, j, table[0][1])
            add_edge(links, components, 0, i, j-1, table[0][2])
            add_edge(links, components, 0, i, j, table[0][3])

    # Top right corner
    if (i == 0) and (j == n):
        # u = links[1][i-1][j]
        d = links[1][i][j]
        l = links[0][i][j-1]
        # r = links[0][i][j]
        table = [
                    [None, 1, 1, None],
                    [None, -1, -1, None]
                ]
        # if not u == None:
        #     table = [row for row in table if row[0] == u]
        if not d == None:
            table = [row for row in table if row[1] == d]
        if not l == None:
            table = [row for row in table if row[2] == l]
        # if not r == None:
        #    table = [row for row in table if row[3] == r]
        if len(table) == 1:
            # add_edge(links, components, 1, i-1, j, table[0][0])
            add_edge(links, components, 1, i, j, table[0][1])
            add_edge(links, components, 0, i, j-1, table[0][2])
            # add_edge(links, components, 0, i, j, table[0][3])

    # Left edge
    if (0 < i < m) and (j == 0):
        u = links[1][i-1][j]
        d = links[1][i][j]
        # l = links[0][i][j-1]
        r = links[0][i][j]
        table = [
                    [1, 1, None, -1],
                    [1, -1, None, 1],
                    [-1, 1, None, 1],
                    [-1, -1, None, -1]
                ]
        if not u == None:
            table = [row for row in table if row[0] == u]
        if not d == None:
            table = [row for row in table if row[1] == d]
        # if not l == None:
        #     table = [row for row in table if row[2] == l]
        if not r == None:
            table = [row for row in table if row[3] == r]
        if len(table) == 1:
            add_edge(links, components, 1, i-1, j, table[0][0])
            add_edge(links, components, 1, i, j, table[0][1])
            # add_edge(links, components, 0, i, j-1, table[0][2])
            add_edge(links, components, 0, i, j, table[0][3])
        
    # Center
    if (0 < i < m) and (0 < j < n):
        u = links[1][i-1][j]
        d = links[1][i][j]
        l = links[0][i][j-1]
        r = links[0][i][j]
        table = [
                    [1, 1, -1, -1],
                    [1, -1, 1, -1],
                    [1, -1, -1, 1],
                    [-1, 1, 1, -1],
                    [-1, 1, -1, 1],
                    [-1, -1, 1, 1],
                    [-1, -1, -1, -1]
                ]
        if not u == None:
            table = [row for row in table if row[0] == u]
        if not d == None:
            table = [row for row in table if row[1] == d]
        if not l == None:
            table = [row for row in table if row[2] == l]
        if not r == None:
            table = [row for row in table if row[3] == r]
        if len(table) == 1:
            add_edge(links, components, 1, i-1, j, table[0][0])
            add_edge(links, components, 1, i, j, table[0][1])
            add_edge(links, components, 0, i, j-1, table[0][2])
            add_edge(links, components, 0, i, j, table[0][3])

    # Right edge
    if (0 < i < m) and (j == n):
        u = links[1][i-1][j]
        d = links[1][i][j]
        l = links[0][i][j-1]
        # r = links[0][i][j]
        table = [
                    [1, 1, -1, None],
                    [1, -1, 1, None],
                    [-1, 1, 1, None],
                    [-1, -1, -1, None]
                ]
        if not u == None:
            table = [row for row in table if row[0] == u]
        if not d == None:
            table = [row for row in table if row[1] == d]
        if not l == None:
            table = [row for row in table if row[2] == l]
        # if not r == None:
        #     table = [row for row in table if row[3] == r]
        if len(table) == 1:
            add_edge(links, components, 1, i-1, j, table[0][0])
            add_edge(links, components, 1, i, j, table[0][1])
            add_edge(links, components, 0, i, j-1, table[0][2])
            # add_edge(links, components, 0, i, j, table[0][3])

    # Bottom left corner
    if (i == m) and (j == 0):
        u = links[1][i-1][j]
        # d = links[1][i][j]
        # l = links[0][i][j-1]
        r = links[0][i][j]
        table = [
                    [1, None, None, 1],
                    [-1, None, None, -1]
                ]
        if not u == None:
            table = [row for row in table if row[0] == u]
        # if not d == None:
        #     table = [row for row in table if row[1] == d]
        # if not l == None:
        #     table = [row for row in table if row[2] == l]
        if not r == None:
           table = [row for row in table if row[3] == r]
        if len(table) == 1:
            add_edge(links, components, 1, i-1, j, table[0][0])
            # add_edge(links, components, 1, i, j, table[0][1])
            # add_edge(links, components, 0, i, j-1, table[0][2])
            add_edge(links, components, 0, i, j, table[0][3])

    # Bottom edge
    if (i == m) and (0 < j < n):
        u = links[1][i-1][j]
        # d = links[1][i][j]
        l = links[0][i][j-1]
        r = links[0][i][j]
        table = [
                    [1, None, 1, -1],
                    [1, None, -1, 1],
                    [-1, None, 1, 1],
                    [-1, None, -1, -1]
                ]
        if not u == None:
            table = [row for row in table if row[0] == u]
        # if not d == None:
        #     table = [row for row in table if row[1] == d]
        if not l == None:
            table = [row for row in table if row[2] == l]
        if not r == None:
            table = [row for row in table if row[3] == r]
        if len(table) == 1:
            add_edge(links, components, 1, i-1, j, table[0][0])
            # add_edge(links, components, 1, i, j, table[0][1])
            add_edge(links, components, 0, i, j-1, table[0][2])
            add_edge(links, components, 0, i, j, table[0][3])

    # Bottom right corner
    if (i == m) and (j == n):
        u = links[1][i-1][j]
        # d = links[1][i][j]
        l = links[0][i][j-1]
        # r = links[0][i][j]
        table = [
                    [1, None, 1, None],
                    [-1, None, -1, None]
                ]
        if not u == None:
            table = [row for row in table if row[0] == u]
        # if not d == None:
        #     table = [row for row in table if row[1] == d]
        if not l == None:
            table = [row for row in table if row[2] == l]
        # if not r == None:
        #     table = [row for row in table if row[3] == r]
        if len(table) == 1:
            add_edge(links, components, 1, i-1, j, table[0][0])
            # add_edge(links, components, 1, i, j, table[0][1])
            add_edge(links, components, 0, i, j-1, table[0][2])
            # add_edge(links, components, 0, i, j, table[0][3])



################
# Loop factors #
################

def factor_loop(links, components):
    for component in components:
        for index_1 in range(len(component)):
            for index_2 in range(index_1):
                i_1 = component[index_1][0]
                j_1 = component[index_1][1]
                i_2 = component[index_2][0]
                j_2 = component[index_2][1]
                if (i_1 == i_2) and (j_1 == j_2 + 1) and (not links[0][i_1][j_1-1] == 1):
                    add_edge(links, components, 0, i_1, j_1 - 1, -1)
                if (i_1 == i_2) and (j_1 == j_2 - 1) and (not links[0][i_1][j_1] == 1):
                    add_edge(links, components, 0, i_1, j_1, -1)
                if (i_1 == i_2 + 1) and (j_1 == j_2) and (not links[1][i_1-1][j_1] == 1):
                    add_edge(links, components, 1, i_1-1, j_1, -1)
                if (i_1 == i_2 - 1) and (j_1 == j_2) and (not links[1][i_1][j_1] == 1):
                    add_edge(links, components, 1, i_1, j_1, -1)



###################
# Other functions #
###################

def add_edge(links, components, orientation, i, j, sign):
    if (sign == 1) and (not links[orientation][i][j] == 1):
        if orientation == 0:
            i_1 = i
            j_1 = j
            i_2 = i
            j_2 = j + 1
        if orientation == 1:
            i_1 = i
            j_1 = j
            i_2 = i + 1
            j_2 = j
        index_1 = 0
        while [i_1, j_1] not in components[index_1]:
            index_1 += 1
        index_2 = 0
        while [i_2, j_2] not in components[index_2]:
            index_2 += 1
        if not index_1 == index_2:
            components += [components[index_1] + components[index_2]]
            del components[np.max([index_1, index_2])]
            del components[np.min([index_1, index_2])]
    links[orientation][i][j] = sign

def arc_consistency(links, components):
    for iteration in range((m+1)*(n+1)):
        for i in range(m):
            for j in range(n):
                factor_entry(links, components, i, j)
        for i in range(m+1):
            for j in range(n+1):
                factor_intersection(links, components, i, j)
        factor_loop(links, components)



################
# Main program #
################

# Shape of entries with m rows and n columns
m, n = entries.shape

# Initializes and displays links as undetermined (None value in every entry)
solution_links = [[[None for j in range(n)] for i in range(m+1)], [[None for j in range(n+1)] for i in range(m)]]
solution_components = list(chain.from_iterable([[[[i,j]] for j in range(n+1)] for i in range(m+1)]))
display(solution_links)
# print(solution_components)
# print(len(solution_components))

# Propogates constraints with arc_consistency and then displays links
arc_consistency(solution_links, solution_components)
display(solution_links)
# print(solution_components)
# print(len(solution_components))
