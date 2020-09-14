import random
from dataclasses import dataclass
from pprint import pprint

from colorama import Fore, Back, Style


@dataclass
class Player:
    name: str
    play_time: float = 1
    exclude_spymaster: int = 0
    is_spymaster: int = 0

    def __key(self):
        return (self.name)

    def __hash__(self):
        return hash(self.__key())

    def __repr__(self):
        if self.is_spymaster == 1:
            return Style.BRIGHT + "*{0} (Spymaster)*".format(self.name)
        else:
            return Style.NORMAL + "{0}".format(self.name)

# Names must be unique
# Mark anyone only joining some of the time with how much of the time they'll play
dmTeam = {Player("AmitSh"), Player("Ariel", play_time=.4), Player("Asaf", exclude_spymaster=1), Player("Boaz"),
          Player("Keren"), Player("Lea", play_time=.7), Player("Nir"), Player("Ohad", play_time=.5, exclude_spymaster=1),
          Player("Ran"), Player("Vladik"), Player("Yihezkel"), Player("Yochai")}
#expandedTeam = dmTeam.union(
#    {Player("AmitOf"), Player("Gil"), Player("Noam"), Player("Omer"), Player("Oren"), Player("Ron"), Player("Roy"),
#     Player("Sagiv"), Player("Sivan"), Player("Tomer"), Player("Yahav"), Player("Zohar")})
# If expandedTeam is not guaranteed to include the entire set of dmTeam:
expandedTeam = {Player("Ran"), Player("Keren"), Player("Boaz"), Player("Yahav", play_time=.3), Player("Asaf"),
     Player("Amit"), Player("Yihezkel", exclude_spymaster=1)}

def calc_player_data(players):
    sum_play_time = 0
    potential_spymasters = set()

    for player in players:
        sum_play_time += player.play_time
        if player.exclude_spymaster == 0 and player.play_time == 1:
            potential_spymasters.add(player)
    return (sum_play_time, potential_spymasters)


def assign_teams(players):
    red_team = []
    blue_team = []
    team_play_time = {id(red_team): 0, id(blue_team): 0}
    players = sorted(players, reverse=True, key=lambda x: x.play_time)
    remaining_playtime, potential_spymasters = calc_player_data(players)

    if len(potential_spymasters) < 2:
        print("Not enough potential spymasters")
        return
    spymasters = random.sample(potential_spymasters, 2)
    red_spymaster = spymasters.pop(random.randint(0, 1))
    blue_spymaster = spymasters[0]
    red_spymaster.is_spymaster = 1
    blue_spymaster.is_spymaster = 1
    red_team.append(red_spymaster)
    blue_team.append(blue_spymaster)
    print("Player {0} has been randomly assigned to red as Spymaster".format(red_spymaster.name))
    print("Player {0} has been randomly assigned to blue as Spymaster".format(blue_spymaster.name))
    team_play_time[id(red_team)] += red_spymaster.play_time
    team_play_time[id(blue_team)] += blue_spymaster.play_time
    remaining_playtime -= (blue_spymaster.play_time + red_spymaster.play_time)

    for player in players:
        if player != red_spymaster and player != blue_spymaster:
            assign_to_team = red_team
            if (team_play_time[id(red_team)] - team_play_time[id(blue_team)]) + player.play_time > remaining_playtime:
                print("Player {0} with playtime {1} has been manually assigned to blue because red already has a playtime surplus of {2} and only {3} remains".format(player.name, player.play_time, round(team_play_time[id(red_team)] - team_play_time[id(blue_team)], 1), round(remaining_playtime, 1)))
                assign_to_team = blue_team
            elif (team_play_time[id(blue_team)] - team_play_time[id(red_team)]) + player.play_time <= remaining_playtime:
                if random.randint(0, 1) == 0:
                    print("Player {0} with playtime {1} has been randomly assigned to blue because blue has a playtime surplus of just {2} and plenty ({3}) remains".format(player.name, player.play_time, round(team_play_time[id(blue_team)] - team_play_time[id(red_team)], 1), round(remaining_playtime, 1)))
                    assign_to_team = blue_team
                else:
                    print("Player {0} with playtime {1} has been randomly assigned to red because blue has a playtime surplus of just {2} and plenty ({3}) remains".format(player.name, player.play_time, round(team_play_time[id(blue_team)] - team_play_time[id(red_team)], 1), round(remaining_playtime, 1)))
            else:
                print("Player {0} with playtime {1} has been manually assigned to red because blue already has a playtime surplus of {2} and only {3} remains".format(player.name, player.play_time, round(team_play_time[id(blue_team)] - team_play_time[id(red_team)], 1), round(remaining_playtime, 1)))
            assign_to_team.append(player)
            team_play_time[id(assign_to_team)] += player.play_time
            remaining_playtime -= player.play_time

    return (sorted(red_team, key=lambda x: x.name), sorted(blue_team, key=lambda x: x.name))


if __name__ == '__main__':
    redTeam, blueTeam = assign_teams(expandedTeam)
    pprint('--------------------------------------')
    print(Fore.RED + "Red Team:  {0}".format(redTeam))
    print(Fore.BLUE + 'Blue Team: {0}'.format(blueTeam))
