def remove2ndInstancev5(any_list):
    """
    use set to remove the 2nd instance of the repeated item first shows
    preconditions: input a list
    postconditions: return the list without the 2nd instance\
                    or return a the orginal list if no item repeates
    """
    print(any_list)
    for i in range(len(any_list)):
        if any_list[i] in any_list[i + 1:]:
            ii = any_list.index(any_list[i], i + 1)
            return any_list[:ii] + any_list[ii + 1:]
    print('no repeated items')
    return any_list


def remove2ndInstanceV6(any_list):
    """
    modified on the version 5.
    preconditons: input a list
    postconditions: return the list without the 2nd instance whose value has\
                    fisrt appear twice.
                    if the no items in the list repeates,\
                    return the original list.
    """
    print(any_list)

    # the sec_instance list stores the iindex of 2nd instances
    sec_instance = []

    # for every elements of the any_list,\
    # check if a 2nd instance appear after it\
    # and stores its index in the sec_instance list
    for i in range(len(any_list)):
        if any_list[i] in any_list[i + 1:]:
            ii = any_list.index(any_list[i], i + 1)
            sec_instance.append(ii)

    # if sec_instance remains empty then no item repeats
    if sec_instance == []:
        print('No item repeates.')
        return any_list
    else:
        index = min(sec_instance)
        return any_list[:index] + any_list[index + 1:]


