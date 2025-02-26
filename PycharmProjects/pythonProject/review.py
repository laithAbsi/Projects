



def myfunction(myParam):
    print('you sent in {}'.format(myParam))
    return 2*myParam


print(myfunction(200))

def addOdd(low, high) :
 sum = 0
 for i in range(low, high+1):
    if i % 2 == 1:
        sum = sum + i
 return sum

out = addOdd(1, 11)
print(out)

def sumDigits(n):
 sum = 0
 while n > 0:
    d = n % 10
    sum = sum + d
    n = n // 10
 return sum

x = sumDigits(767)
print(x)