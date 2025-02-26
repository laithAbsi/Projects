
starts = dict()

alphabet = 'abcdefghijklmnopqrstuvwxyz'



for letter in alphabet:

    starts[letter] = set()

with open('wordlelist', 'r') as fh:

    for word in fh:
        word = word.strip()
        # add to the dictionary

        letter = word[0]
        starts[letter].add(word)       # starts[letter] is out set.


print(starts['a'])













