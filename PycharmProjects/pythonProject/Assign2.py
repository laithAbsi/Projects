# Laith Al-Absi. This code analyzes a list of names given by the user and tells the user if any two names
#                 sound alike based on their soundex code.


def asking_user_for_list_of_names():
    """
    function that asks the user for the list of names.
    :return: returns a list of names given by the user.
    """
    final = []
    print('Enter names, one on each line. Type DONE to quit entering names.')

    while True:

        userInp = input()
        if userInp == 'DONE':
            break
        final.append(userInp)
        final = sorted(final)

    return final


def replace_letters_with_digits(name):
    """
    this function replaces the letters in every name in the list given by the user to numbers.
    :param name: names in the list given by the user.
    :return: returns a list of tha names converted to numbers.
    """

    letters1 = "aeiouyhw"
    letters2 = "bfpv"
    letters3 = "cgjkqsxz"
    letters4 = "dt"
    letters5 = "l"
    letters6 = "mn"
    letters7 = "r"
    result = ""
    for l in name:
        if l in letters1:
            result += '0'
        elif l in letters2:
            result += '1'
        elif l in letters3:
            result += '2'
        elif l in letters4:
            result += '3'
        elif l in letters5:
            result += '4'
        elif l in letters6:
            result += '5'
        elif l in letters7:
            result += '6'
    return result


def removing_consecutive_digits(digits):
    """
    this function gets rid of repeated numbers in the soundex of each name in the list given by the user.
    :param digits:
    :return: returns a list of soundex codes without any repeated numbers
    """
    res = digits[0]
    for idx in range(1, len(digits)):
        if digits[idx] == res[-1]:
            pass
        else:
            res += digits[idx]

    return res


def removing_the_zeros(digits):
    """
    this function removes any zeros in the soundex code of each name in the list given by the user.
    :param digits: soundex code of the names in the list given by the user.
    :return: returns a list of soundex codes that does not include any zeros.
    """

    result = ""
    for idx in range(0, len(digits)):
        if digits[idx] != '0':
            result += digits[idx]

    return result


def soundex(name):
    """
    this function gets the soundex code of every name in the list of names given by the user.
    :param name: names in the list given by the user
    :return: returns a list of every soundex code for every name in the list given by the user.
    """
    # step1
    name = name.lower()
    # step 2
    F = name[0]
    # step 3
    digits = replace_letters_with_digits(name)
    # step 4
    digits2 = removing_consecutive_digits(digits)
    # step 5
    digits3 = removing_the_zeros(digits2)
    # step 6
    F_digit = replace_letters_with_digits(F)
    if len(digits2) == 0:
        digits3 = '0000'
    if F_digit == digits3[0]:
        digits3 = F + digits3[1::]
    else:
        digits3 = F + digits3
    # step 7
    final_code = digits3 + '0000'
    final_code = final_code[0:4]
    return final_code


def main():
    namelist = asking_user_for_list_of_names()
    name_code_list = []
    for name in namelist:
        code = soundex(name)
        name_code_list.append((code, name))
    identical_code_list = []

    for idx1 in range(0, len(name_code_list)):
        first_code_name = name_code_list[idx1]
        for idx2 in range(idx1 + 1, len(name_code_list)):
            second_code_name = name_code_list[idx2]
            if first_code_name[0] == second_code_name[0]:
                identical_code_list.append((first_code_name[1], second_code_name[1]))

    for name_name in identical_code_list:
        print('{} and {} have the same Soundex encoding.'.format(name_name[0], name_name[1]))


main()
