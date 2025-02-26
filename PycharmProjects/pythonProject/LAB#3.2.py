

accountTotal = int(input('Enter your bank balance:'))
numMonths = 0
while accountTotal > 20:
 numMonths = numMonths+1
 accountTotal -= 1
 print('Your account currently has ${}'.format(accountTotal))


print('Your balance has reached $20 after {} months'.format(numMonths))
