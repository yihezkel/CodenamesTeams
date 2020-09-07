import random
from dataclasses import dataclass
from pprint import pprint


@dataclass
class Player:
    name: str
    playTime: float = 1
    excludeSpymaster: int = 0
    isSpymaster: int = 0

    def __key(self):
        return (self.name)

    def __hash__(self):
        return hash(self.__key())

    def __repr__(self):
        return "{0}{1}".format(self.name, " ***Spymaster***" if self.isSpymaster == 1 else "")


# Names must be unique
# Mark anyone only joining some of the time with how much of the time they'll play
dmTeam = {Player("AmitSh"), Player("Ariel", playTime=.4), Player("Asaf", excludeSpymaster=1), Player("Boaz"),
          Player("Keren"), Player("Lea", playTime=.7), Player("Nir"), Player("Ohad", playTime=.5, excludeSpymaster=1),
          Player("Ran"), Player("Vladik"), Player("Yihezkel"), Player("Yochai")}
expandedTeam = dmTeam.union(
    {Player("AmitOf"), Player("Gil"), Player("Noam"), Player("Omer"), Player("Oren"), Player("Ron"), Player("Roy"),
     Player("Sagiv"), Player("Sivan"), Player("Tomer"), Player("Yahav"), Player("Zohar")})
# If expandedTeam is not guaranteed to include the entire set of dmTeam:
#expandedTeam = {"AmitOf", "AmitSh", "Ariel", "Asaf", "Boaz", "Gil", "Keren", "Lea", "Nir", "Noam", "Ohad", "Omer",
#                "Oren", "Ran", "Ron", "Roy", "Sagiv", "Sivan", "Tomer", "Vladik", "Yahav", "Yihezkel", "Yochai",
#                "Zohar"}

def calcPlayerData(players):
    sumPlayTime = 0
    potentialSpymasters = set()

    for player in players:
        sumPlayTime += player.playTime
        if player.excludeSpymaster == 0 and player.playTime == 1:
            potentialSpymasters.add(player)
    return (sumPlayTime, potentialSpymasters)


def assignTeams(players):
    redTeam = []
    blueTeam = []
    teamPlayTime = {id(redTeam): 0, id(blueTeam): 0}
    players = sorted(players, reverse=True, key=lambda x: x.playTime)
    remainingPlaytime, potentialSpymasters = calcPlayerData(players)

    if len(potentialSpymasters) < 2:
        print("Not enough potential spymasters")
        return
    spymasters = random.sample(potentialSpymasters, 2)
    redSpymaster = spymasters.pop(random.randint(0, 1))
    blueSpymaster = spymasters[0]
    redSpymaster.isSpymaster = 1
    blueSpymaster.isSpymaster = 1
    redTeam.append(redSpymaster)
    blueTeam.append(blueSpymaster)
    print("Player {0} has been randomly assigned to red as Spymaster".format(redSpymaster.name))
    print("Player {0} has been randomly assigned to blue as Spymaster".format(blueSpymaster.name))
    teamPlayTime[id(redTeam)] += redSpymaster.playTime
    teamPlayTime[id(blueTeam)] += blueSpymaster.playTime
    remainingPlaytime -= (blueSpymaster.playTime + redSpymaster.playTime)

    for player in players:
        if player != redSpymaster and player != blueSpymaster:
            assignToTeam = redTeam
            if (teamPlayTime[id(redTeam)] - teamPlayTime[id(blueTeam)]) + player.playTime > remainingPlaytime:
                print("Player {0} with playtime {1} has been manually assigned to blue because red already has a playtime surplus of {2} and only {3} remains".format(player.name, player.playTime, round(teamPlayTime[id(redTeam)] - teamPlayTime[id(blueTeam)], 1), round(remainingPlaytime, 1)))
                assignToTeam = blueTeam
            elif (teamPlayTime[id(blueTeam)] - teamPlayTime[id(redTeam)]) + player.playTime <= remainingPlaytime:
                if random.randint(0, 1) == 0:
                    print("Player {0} with playtime {1} has been randomly assigned to blue because blue has a playtime surplus of just {2} and plenty ({3}) remains".format(player.name, player.playTime, round(teamPlayTime[id(blueTeam)] - teamPlayTime[id(redTeam)], 1), round(remainingPlaytime, 1)))
                    assignToTeam = blueTeam
                else:
                    print("Player {0} with playtime {1} has been randomly assigned to red because blue has a playtime surplus of just {2} and plenty ({3}) remains".format(player.name, player.playTime, round(teamPlayTime[id(blueTeam)] - teamPlayTime[id(redTeam)], 1), round(remainingPlaytime, 1)))
            else:
                print("Player {0} with playtime {1} has been manually assigned to red because blue already has a playtime surplus of {2} and only {3} remains".format(player.name, player.playTime, round(teamPlayTime[id(blueTeam)] - teamPlayTime[id(redTeam)], 1), round(remainingPlaytime, 1)))
            assignToTeam.append(player)
            teamPlayTime[id(assignToTeam)] += player.playTime
            remainingPlaytime -= player.playTime

    return (sorted(redTeam, key=lambda x: x.name), sorted(blueTeam, key=lambda x: x.name))


if __name__ == '__main__':
    redTeam, blueTeam = assignTeams(dmTeam)
    pprint('--------------------------------------')
    pprint('Red Team: {0}'.format(redTeam))
    pprint('Blue Team: {0}'.format(blueTeam))
