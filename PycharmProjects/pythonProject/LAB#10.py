
class Player:
    def __init__(self, id, team):
        self.__id = id
        self.__team = team
    def __repr__(self):
        return '{} ({})'.format()

class Pitcher:
    def __init__(self, id, team, wins, losses, ERA):
        super().__init__(id, team)
        self.wins = wins
        self.losses = losses
        self.ERA = ERA

    def __repr__(self):
        P = super().__repr__()
        return '{} {} W, {} L, ERA: {}'.format(P, self.wins, self.losses, self.ERA)

    def __lt__(self, other):
        return self.ERA <= other.ERA

    def getWins(self):
        return self.wins

class Batter(Player):
    def __init__(self, id, team, hits, HR, batting):
        super().__init__(id, team)
        self.hits = hits
        self.HR = HR
        self.battingAverage = batting

    def __repr__(self):
        P = super().__repr__()
        return '{} {} hits, {} HRs, Average: {}'.format(P, self.hits, self.HR, self.battingAverage)

    def __lt__(self, other):
        return self.battingAverage <= other.battingAverage

    def getHits(self):
        return self.hits


def readPitchers():
    all_pitchers = []
    best_pitchers = []
    with open('pitchers.txt','r') as pit:

        for p in pit:
            data = p.split('\t')
            pObj = Pitcher(data[0],data[1],int(data[2]),int(data[3]),float(data[4]))
            all_pitchers.append(pObj)

    all_pitchers.sort()

    for player in best_pitchers:
        x = player.getWins()
        if x >= 5:
            best_pitchers.append(player)

    best_pitchers.sort()

    return all_pitchers

def readBatters():
    all_batters = []
    best_batters = []
    with open('batters.txt','r') as bat:
        for b in bat:
            data = b.split('\t')
            bObj = Batter(data[0],data[1],int(data[2]),int(data[3]),float(data[4]))
            all_batters.append(bObj)
    all_batters.sort()

    for player in all_batters:
        x = player.getHits()
        if x >= 5:
            best_batters.append(player)
    best_batters.sort()

    return all_batters

def main():
    all_pitchers = readPitchers()
    print(all_pitchers)
    all_batters = readBatters()
    print(all_batters)\

main()










