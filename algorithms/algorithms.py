# Definition of the algorithms

#---------Linear search--------------#
def linear_search(list1, target1):
    for index, i in enumerate(list1):
        if i == target1:
            return index
    return -1

#---------Binary search--------------#
def binary_search(list2, low, high, target2):
    if high >= low:
        mid = (high + low) // 2
        if list2[mid] == target2:
            return mid
        elif list2[mid] > target2:
            return binary_search(list2, low, mid - 1, target2)
        else:
            return binary_search(list2, mid + 1, high, target2)
    else:
        return -1
