

shopName = input('Please enter the shop name: ')
ringQty = int(input('Please enter the quantity of rings: '))
glassesQty = int(input('Please enter the quantity of glasses: '))

print('Shop name is {}'.format(shopName))
print('Ring inventory is {}'.format(ringQty))
print('Glasses inventory is {}'.format(glassesQty))

print('Inventory Total: {}'.format(ringQty+glassesQty))