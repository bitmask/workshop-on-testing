
def parse_levels_file(levels_file):
    """
    Parses the eggnog levels file that contains the definitions of orthologous groups and creates the levels dictionary that will be used in the other functions in this package, which it returns.

    The levels dictionary contains three keys
    - name (str) -- the human readable name of the level
    - members (array of int) -- the taxids of the organisms that are at this level
    - size (int) -- the number of members at this level

    @param levels_file filename of the eggnog levels file
    @return levels dictionary
    """

    levels = {}
    try:
        f = open(levels_file, 'r')
        not_first_line = False
        for line in iter(f.readline, ''):
            if not_first_line:
                elements = line.split("\t")
                members_str = elements[7].rstrip('\n').split(" ")
                members_int = [int(mem) for mem in members_str]
                entry = {'name': elements[2], 'members': members_int, 'size': int(elements[3])}
                levels[int(elements[0])] = entry
            else:
                not_first_line = True
    except IOError:
        print 'cannot open', levels_file
        raise
    return levels


def get_members(l, levels):
    """ 
    @param l The level to get the members for (int)
    @param levels The hash of all levels read by parse_levels_file

    @return All members for the given level (array of ints)
    """
    return levels[int(l)]['members']

def get_size(l, levels):
    """
    @param l The level to get the size for (int)
    @param levels The hash of all levels read by parse_levels_file
    
    @return The size of the given level == number of members (int)
    """
    return levels[int(l)]['size']

def get_name(l, levels):
    """
    @param l The level to get the name for (int)
    @param levels The hash of all levels read by parse_levels_file
    
    @return The human readable name of the given level (str)
    """
    return levels[int(l)]['name']

def smallest_group(members, groups):
    '''
    Given a set of members, find the smallest group that contains them all.  
    Members must be values in the groups dictionary.  
    This is a helper function called by find_level() that returns the most recent / smallest level that includes the query organism and all organisms.  The calling function will place either all the members of the specified level/taxid/orthologous group or all the organisms that have been selected by the user, whichever was specified, into the members list.  
    An exception will be thrown if a valid level can not be found.
    @param members A list of the members to find the smallest containing group for
    @param groups A dictionary with groups as the keys and members as values (see get_members function for format)
    @return The smallest group containing all members
    '''
    debug = 0

    if debug:
        print "looking for the smallest group containing: " + str(members)
    minsize = float("inf")
    bestgroup = ''

    for g in groups:
        group_contents = get_members(g, groups)
        #if debug:
            #print "group members for " + str(g) + " size " + str(get_size(g, groups))
            #print str(group_contents)
        if set(members) == set(members).intersection(set(group_contents)): # if all organisms are members of the group
            size = get_size(g, groups)
            if debug:
                print "all are in " + get_name(g, groups)
            if size < minsize:
                if debug:
                    print "updated size to " + str(size) + " and bestgroup to " + str(g)
                minsize = size
                bestgroup = g
    if bestgroup == '':
        raise Exception('Cannot find any valid group for members')
    else:
        return int(bestgroup)


def find_level(query_org, search_level, search_orgs, levels_file):
    """
    Return the most recent / smallest level that includes all of query_org and search_orgs.
    Either query_org or search_orgs must be specified, and not both.

    find_level calls most_recent_level; most_recent_level should not need to be called directly

    Exceptions are raised if
     - both search_level and search_orgs are specified
     - neither search_level or search_orgs are specified
     - a number is given as the orthologous group (search_level), which is not a valid orthologous group == not present in the levels hash

    @param query_org User submitted query organism (int)
    @param search_level User submitted orthologous group to evaluate conservation within (int)
    @param search_orgs User submitted list of organisms to evaluate conservation within (list of ints)
    @param levels The hash of all levels read by parse_levels_file

    @return The taxid of the orthologous group to used for multiple alignment (int)
    """

    levels = parse_levels_file(levels_file)

    if search_level:
        # verify that the specified level is a valid level
        if search_level in levels:
            # find the smallest level that includes the query_org as well as all members of the specified level
            found = smallest_group(get_members(search_level, levels) + [query_org], levels)
            if found:
                return found
        else:
            raise Exception("can't find level " + str(search_level) + " in list of orthologous groups")

    elif search_orgs is not None and len(search_orgs) > 0:
        # search_orgs is specifed, so we need to find the smallest level that includes all the spceified organisms, and the query organism
        return smallest_group(search_orgs + [query_org], levels)

    else:
        raise Exception("must specify either level or list of organisms")



