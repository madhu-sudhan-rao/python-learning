def get_min(array):
    return min(array)
def get_max(array):
    return max(array)


def get_min_manual(array):
    minimum = array[0]
    for num in array:
        if(num < minimum):
            minimum = num
    return minimum

def get_max_manual(array):
    maximum = array[0]
    for num in array:
        if(num > maximum):
            maximum = num
    return maximum

print(get_max([1,2,3,4,5]))
print(get_max_manual([1,2,3,4,5]))
print(get_min([1,2,3,4,5]))
print(get_min_manual([1,2,3,4,5]))