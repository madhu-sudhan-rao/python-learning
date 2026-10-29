# Adding elements into list

# Initialize an empty list
a = []

# adds to end of the list
a.append(10)
print(a)

a.insert(0, 5)
print(a)

a.extend([12,23,121])
print(a)

# updating elements into list
a[1] = 25
print(a)

# removing elements into list

a.remove(25)
print(a)

popped_val = a.pop(1)
print(popped_val)
print(a)

del a[0]
print(a)