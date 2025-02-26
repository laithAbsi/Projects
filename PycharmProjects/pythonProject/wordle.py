import pprint
pretty = pprint.PrettyPrinter()
posn = list()  # list of dictionaries.

alph = 'abcdefghijklmnopqrstuvwxyz'


for i in range(5):
    newDict = dict()
    for letter in alph:
        newDict[letter] = set()

    posn.append(newDict)

#pretty.pprint(posn)
with open('wordlelist', 'r') as fh:

    for word in fh:
        word = word.strip()
        for i in range(5):

           currentLetter = word[i]
           posn[i][currentLetter].add(word)



# This code was not explained in class.

input = input('Enter guess, with . for unknowns: ')

all_possibles = []

# go through each letter of the input.
# if the letter is not a period, find the
# words that have that letter in that position.
# add to all_possibles.
for i in range(len(input)):
    currLetter = input[i]
    if currLetter != '.':
        d = posn[i][currLetter]
        # d is the set of all words with letter "currLetter"
        # in position i
        all_possibles.append(d) # add set to the list.

# if one letter appeared in the user input..
if len(all_possibles) > 0:

    # take intersection of all words in all sets
    # these are words that satisfy all constraints.

    valid = all_possibles[0]
    for i in range(1, len(all_possibles)):
        valid = valid & all_possibles[i]

    # print all remaining words.
    # this could be printed more nicely, I guess.
    print(valid)