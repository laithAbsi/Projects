from MoeChams1 import ellipse_area
from MoeChams1 import rectangle_area
from MoeChams1 import trapezoid_area

def is_valid_shape(in_value):
    if in_value == 'ellipse' or 'rectangle' or 'trapezoid' or 'done':
        return True
    elif in_value != 'ellipse' or 'rectangle' or 'trapezoid' or 'done':
        return False

def main():
        myList = []
        repeat = True
        while repeat:
            userinp = input('what shape would you like to calculate? ')
            if is_valid_shape(userinp):
                if userinp == 'ellipse':
                    major = float(input('what is the length of the major? '))
                    minor = float(input('what is the length of the minor? '))
                    ellipseArea = ellipse_area(major, minor)
                    myList.append(round(ellipseArea, 2))

                if userinp == 'rectangle':
                    base = float(input('whats is the length of the base? '))
                    height = float(input('what is the height? '))
                    recArea = rectangle_area(base, height)
                    myList.append(round(recArea, 2))

                if userinp == 'trapezoid':
                    top = float(input('what is the length of the top? '))
                    bottom = float(input('what is the length of the bottom? '))
                    height = float(input('what is the height? '))
                    trapArea = trapezoid_area(top, bottom, height)
                    myList.append(round(trapArea, 2))

                if userinp == 'done':
                    repeat = False


        print(sorted(myList))

main()