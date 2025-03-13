import numpy
import typer
import random
import logging
from collections import defaultdict


def prints_console(data):
    logging.info(data)
    print(data)

def generate_schedule(teams, games_per_pair=4):
    matchups = defaultdict(int)  # save how often teams played against each other
    schedule = []  # all gamedays

    total_games_needed = games_per_pair * (len(teams) * (len(teams) - 1) // 2)
    current_games = 0

    team_3_count = defaultdict(int)
    team_2_count = defaultdict(int)
    while current_games < total_games_needed:
        if len(schedule) <= 21:
            random.shuffle(teams)
            matchday = []
            used_teams = set()

            # create groups of three
            sorted_teams = sorted(teams, key=lambda t: team_3_count[t])
            for _ in range(2):
                trio = [t for t in sorted_teams if t not in used_teams][:3]
                if len(trio) == 3 and matchups[frozenset([trio[0], trio[1]])]<4 and matchups[frozenset([trio[0], trio[2]])]<4 and matchups[frozenset([trio[1], trio[2]])]<4:
                    matchday.append(tuple(trio))
                    used_teams.update(trio)
                    for t in trio:
                        team_3_count[t] += 1

                    for i in range(3):
                        for j in range(i + 1, 3):
                            matchups[frozenset([trio[i], trio[j]])] += 1
                            current_games += 1
                else:
                    while len(trio) != 3 or matchups[frozenset([trio[0], trio[1]])]>=4 or matchups[frozenset([trio[0], trio[2]])]>=4 or matchups[frozenset([trio[1], trio[2]])]>=4:
                        random.shuffle(sorted_teams)
                        trio = [t for t in sorted_teams if t not in used_teams][:3]
                        if len(trio) == 3 and matchups[frozenset([trio[0], trio[1]])] < 4 and matchups[frozenset([trio[0], trio[2]])] < 4 and matchups[frozenset([trio[1], trio[2]])] < 4:
                            matchday.append(tuple(trio))
                            used_teams.update(trio)
                            for t in trio:
                                team_3_count[t] += 1
                            for i in range(3):
                                for j in range(i + 1, 3):
                                    matchups[frozenset([trio[i], trio[j]])] += 1
                                    current_games += 1
                            break

            # create the two pairs for a matchday
            remaining_teams = [t for t in teams if t not in used_teams]
            sorted_remaining_teams = sorted(remaining_teams, key=lambda t: team_2_count[t])
            for i in range(0, len(sorted_remaining_teams), 2):
                if i + 1 < len(sorted_remaining_teams):
                    if matchups[frozenset([sorted_remaining_teams[i], sorted_remaining_teams[i+1]])] + matchups[frozenset([sorted_remaining_teams[i], sorted_remaining_teams[i+1]])] < 4:
                        pair = (sorted_remaining_teams[i], sorted_remaining_teams[i + 1])
                        matchday.append(pair)
                        matchups[frozenset(pair)] += 1
                        current_games += 1

                        team_2_count[pair[0]] += 1
                        team_2_count[pair[1]] += 1
                    '''else:
                        while matchups[frozenset(remaining_teams[i], remaining_teams[i+1])] + matchups[frozenset(remaining_teams[i], remaining_teams[i+1])] < 4:
                            random.shuffle(remaining_teams)
                            trio = [t for t in teams if t not in used_teams][:3]
                            if len(trio) == 3 and matchups[frozenset([trio[0], trio[1]])] < 4 and matchups[
                                frozenset([trio[0], trio[2]])] < 4 and matchups[frozenset([trio[1], trio[2]])] < 4:
                                matchday.append(tuple(trio))
                                used_teams.update(trio)
                                for i in range(3):
                                    for j in range(i + 1, 3):
                                        matchups[frozenset([trio[i], trio[j]])] += 1
                                        current_games += 1
                                break'''
            schedule.append(matchday)

        elif len(schedule) == 22:
            invalid_pairs = {pair: count for pair, count in matchups.items() if count != 4}

            # create gameday 23
            if invalid_pairs:
                games_to_insert = []
                #extra_matchday = []
                for pair, count in invalid_pairs.items():
                    missing_games = 4 - count  # Anzahl der fehlenden Spiele
                    for _ in range(missing_games):
                        games_to_insert.append(tuple(pair))
                for matchday in schedule:
                    three_teams_groups = {frozenset(group) for group in matchday if len(group)==3}
                    two_team_pairs = [group for group in matchday if len(group)==2]
                    if len(two_team_pairs) <=1:
                        for game in games_to_insert[:]:
                            if not any(set(game) & three_group for three_group in three_teams_groups):
                                matchday.append(game)
                                games_to_insert.remove(game)

                schedule.append(games_to_insert)
                prints_console("\nmatch day 23:")
                for match in games_to_insert:
                    prints_console("-".join(map(str, match)))
        elif len(schedule) == 23:
            return schedule

def print_schedule(schedule):
    for i, matchday in enumerate(schedule, 1):
        prints_console(f"------ match day {i} ------")
        for match in matchday:
            prints_console("-".join(map(str, match)))
        print()

'''
def main(team1: str = typer.Option(help="Give name of team 1"),
         team2: str = typer.Option(help="Give name of team 2"),
         team3: str = typer.Option(help="Give name of team 3"),
         team4: str = typer.Option(help="Give name of team 4"),
         team5: str = typer.Option(help="Give name of team 5"),
         team6: str = typer.Option(help="Give name of team 6"),
         team7: str = typer.Option(help="Give name of team 7"),
         team8: str = typer.Option(help="Give name of team 8"),
         team9: str = typer.Option(help="Give name of team 9"),
         team10: str = typer.Option(help="Give name of team 10"),
         ):
'''
logging.basicConfig(filename='gameplan.txt', level=logging.DEBUG, format='')
t1 = "SVW"
t2 = "FCSP"
t3 = "LFC"
t4 = "BVB"
t5 = "S04"
t6 = "SGD"
t7 = "FCB"
t8 = "VfB"
t9 = "Union"
t10 = "FCK"
teams = [t1,t2,t3,t4,t5,t6,t7,t8,t9,t10]
game_schedule = generate_schedule(teams)
print_schedule(game_schedule)


#if __name__ == "__main__":
#    main()