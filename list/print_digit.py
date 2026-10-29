digit = ['Zero', 'One','Two', 'Three', 'Four', 'Five', 'Six','Seven', 'Eight', 'Nine']



def print_digit_in_words(num):
    num = str(num)
    
    for n in num:
        print(digit[int(n)], end=' ')
    
print_digit_in_words(1234)