from reverse_string import *

def palindrome(str):
    if (str == reverse_string(str)):
        return True
    return False

print(palindrome('madam'))