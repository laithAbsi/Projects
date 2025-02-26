


floats = [2.3, 5.5, 6.3, 7.4, 3.8]
number = 3
def averagePref(L,x):
    total = 0
    avg = None
    for i in range(x):
        try:
             total += L[i]
        except IndexError:
            print('the index is out of range')
        try:
            avg = total / x
        except ZeroDivisionError:
            print('cannot divide by zero')
            exit(10)
    return avg

output = averagePref(floats, number)

print(output)