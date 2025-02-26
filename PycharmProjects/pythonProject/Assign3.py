# Laith Al Absi. This program determines the winner of an election using the IRV system.

def func1_read_data():
    """
    this function reads the file.
    :return: returns a list of the data in the file.
    """
    total_num_candidate = 0

    filename = input('Enter the name of the file: ')
    all_data = []
    with open(filename) as fh:
        for line in fh:
            line = line.strip()
            person = line.split(',')
            new_person = []
            for vote in person:
                if vote.isnumeric():
                    new_person.append(int(vote))
                    total_num_candidate = max(total_num_candidate, int(vote))
            all_data.append(new_person)

    return all_data, total_num_candidate


def func2_Percentage_of_Candidate_for_each_round(all_data, total_num_candidates):
    """
    this function calculates the percent of votes each candidate has.
    :param all_data:
    :return: returns a list of vote percent of each candidate.
    """
    counters = [-10 for i in range(total_num_candidates)]

    for i in range(len(all_data)):
        if len(all_data[i]) != 0:

            vote = all_data[i][0]
            if counters[vote-1] == -10:
                counters[vote-1] = 1
            else:
                counters[vote-1] += 1

    total_votes = 0
    for candidate_i_vote in counters:
        if candidate_i_vote > 0:
            total_votes += candidate_i_vote

    for i in range(len(counters)):
        counters[i] /= total_votes
        counters[i] *= 100

    return counters


def func3_Winner(percentages):
    """
    this function determines the winner of the election.
    :param percentages:
    :return: returns the winner of the election.
    """
    for percent in percentages:
        if percent > 50:
            winner = percentages.index(percent) + 1
            return winner
    return 0


def func4_Loser(percentages):
    """
    this function determines the loser of the election.
    :param percentages:
    :return: returns the loser.
    """
    min_percentage = 1000000
    for percent in percentages:

        if percent < 0:
            continue
        if percent < min_percentage:
            min_percentage = percent
    Losers_list = []
    candidateID = 1
    for percent in percentages:
        if percent == min_percentage:
            Losers_list.append(candidateID)
        candidateID += 1
    return Losers_list[-1]


def Eliminating_losers(all_data, loser):
    """
    this function eliminates the loser from the list of votes.
    :param all_data:
    :param loser:
    :return: returns a list excluding the loser.
    """
    for i in range(len(all_data)):
        if loser in all_data[i]:
            all_data[i].remove(loser)
    return all_data


def main():
    all_data, total_num_candidates = func1_read_data()
    mylist = []
    while True:
        percentages = func2_Percentage_of_Candidate_for_each_round(all_data, total_num_candidates)
        winner = func3_Winner(percentages)

        loser = func4_Loser(percentages)
        mylist.append(loser)
        all_data = Eliminating_losers(all_data, loser)

        if winner != 0:
            if winner != loser:
                mylist.append(winner)
            break

    return mylist


output = main()

myString = ''
for i in output[0:-1]:
    myString += str(i) + ', '

elimination_order = 'Elimination order: ' + myString + str(output[-1])
print(elimination_order)
