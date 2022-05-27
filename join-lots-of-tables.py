# github.com/stuwares 27/05/22
# tamerocket.com
# TODO: Refactor to remove the temp files and just go straight from lists
# TODO: Put the JOIN text into a variable to make it easier to swap between left, right etc
# TODO: Move hard-coded db specific stuff .ID etc into variables

#####################################################
# Need to join a load of tables on the same column? #
#         Don't hate your life, use me!             #
#                                                   #
#                                                   #
# > Takes in a line delimited text file tables.txt  #
#                                                   #
# > Left joins every table on the ID column of the  #
#   first table in tables.txt                       #
#                                                   #
# > Creates a randomly generated alias for every    #
#   table!                                          #
#                                                   #
# > Creates a SELECT .* for every alias too!        #
#####################################################


import os
import string
import random 

####################
# Global variables #
#    ...eww        #
####################

S = 6 # number of characters in the random alias. 6 should be fine to avoid duplication but can be increased as needed.
toCut = S + 3 # lenth of alias + .*
toKeep = toCut + 1 # number needed to cut just the table name + alias
ran = '' # for the random strings
lastEight = '' # [alias].* TODO remove this step and just trim the line break in one line
tableAndAlias = '' # store the table_name <space> alias
aliasList = [] # list of every alias
tableList = [] # list of every table_name <space> alias - Table names are always stored in the same string as their alias
counter = 0 # stores the index number while looping to build the final query


###########################################
# Generate a random alias for every table #
# and a [alias].* for every alias         #
###########################################

# creates a random alias after every table name, and puts a copy of the alias + .* at the end of each line
with open('tables.txt', 'r') as istr:
    with open('step1alias.txt', 'w') as ostr:
        for line in istr:
            ran = ''.join(random.choices(string.ascii_lowercase, k = S))
            line = line.rstrip('\n') + ' ' + ran + ' ' + ran + '.*'
            print(line, file=ostr)


# Cut the alias.* from the end of each line and put them into a comma delimited list
with open('step1alias.txt', 'r') as inst:
    with open('step2aliaslist.txt', 'w') as oust:
        for line in inst:
            lastEight = line[len(line) - toCut:]
            lastEight = lastEight.rstrip('\n')
            aliasList.append(lastEight)

        print(','.join(aliasList), file=oust)


# cut the table name and alias from each line and put into a comma delimited list
with open('step1alias.txt', 'r') as tabin:
    with open('step3tablelist.txt', 'w') as tabout:
        for line in tabin:
            tableAndAlias = line[:len(line) - toKeep]
            tableList.append(tableAndAlias)

        print(','.join(tableList), file=tabout)

####################
# Create the query #
####################

# from first_table alias
# left join next_table nextalias
# on alias.ID = nextalias.ID
# left join thrid_table thirdalias
# on nextalias.ID = thirdalias.ID
# .... etc

with open('bigquery.txt', 'w') as bigquery:
    bigquery.write('SELECT\n')
    bigquery.write(','.join(aliasList) + '\n')
    bigquery.write('FROM\n')
    for name in aliasList:

        if (counter <= len(tableList) - 1):
            if (counter == 0):
                bigquery.write(tableList[counter] + '\n')
                bigquery.write('LEFT JOIN ' + tableList[counter + 1] + '\n')
                bigquery.write('ON ' + aliasList[counter][:-2] + '.ID = ' + aliasList[counter + 1][:-2] + '.ID\n' )
                counter = counter + 2
            else:
                bigquery.write('LEFT JOIN ' + tableList[counter] + '\n')
                bigquery.write('ON ' + aliasList[0][:-2] + '.ID = ' + aliasList[counter][:-2] + '.ID\n' )
                counter = counter + 1
        
    # Optional WHERE, default will use the alias of the first table in tables.txt to filter on ID, but edit/remove as needed!
    bigquery.write('\nWHERE ' + aliasList[0][:-2] + '.ID = ' '--replace me with employee id number')  

# clean up temp files
if os.path.exists('step1alias.txt'):
    os.remove('step1alias.txt')

if os.path.exists('step2aliaslist.txt'):
    os.remove('step2aliaslist.txt')

if os.path.exists('step3tablelist.txt'):
    os.remove('step3tablelist.txt')
