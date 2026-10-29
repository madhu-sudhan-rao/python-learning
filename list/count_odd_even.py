def count_odd_even(array):
    odd_c = 0
    even_c = 0
    for num in array:
        if(num % 2 == 0):
            even_c += 1
        else:
            odd_c += 1
            
    return list({odd_c, even_c})

print(count_odd_even([2, 3, 4, 5, 6]))