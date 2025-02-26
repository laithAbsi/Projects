

def pigLatin(word):

    word = word.lower()
    consonants = 'bcdfghjklmnpqrstvwxyz'
    posn = None
    for i in range(0, len(word)):
        if word[i] not in consonants:
            posn = i
            break

    if posn == 0:
        word = word + 'yay'
        return word

    elif 0 < posn < len(word):
        word = word[posn:len(word)] + word[0:posn] + 'ay'
        return word

mylist = ['pig', 'computer', 'science', 'scram', 'Western', 'Ontario', 'apple']

for w in mylist:

    out = pigLatin(word=w)
    print('{} in Pig Latin is {}'.format(w, out))


