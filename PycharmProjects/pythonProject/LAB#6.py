
YEAR = 0
LEAGUE = 1
TEAM = 2
GAMES_PLAYED = 3
GAMES_WON = 4
GAMES_LOST = 5
WON_WS = 6
RUNS = 7
AT_BAT = 8
HITS = 9
DOUBLES = 10
TRIPLES = 11
HOME_RUNS = 12
ATTENDANCE = 13
NON_INT_COLS = [LEAGUE,TEAM,WON_WS]


highest = 0
all_data = []
with open('Teams (1).csv', 'r') as fh:
    headers = fh.readline()
    for line in fh:
        data = line.strip().split(',')

        for i in range(len(data)):
            if i not in NON_INT_COLS:
                data[i] = int(data[i])
            elif i == WON_WS:
                data[i] = (data[i] == 'Y')
        all_data.append(data)

    for i in all_data:
        homeruns = int(i[12])
        if homeruns > highest:
            highest = homeruns
            team = i[2]
            year = i[0]
    total = []
    for j in all_data:
        if int(j[0]) == 1999:
            total.append(j[13])





print('the team with the most home runs in a season is {}. with {} home runs. in the year {}.'.format(team,highest,year))
print('the total attendance at all games in 1999 is {} attendees.'.format(sum(total)))






