import numpy
import typer
import random
import logging
import itertools
from collections import defaultdict


def generate_schedule(teams, games_per_pair=4, total_matchdays=23):
    # Create all possible matchups
    all_pairs = list(itertools.combinations(teams, 2))
    all_trios = list(itertools.combinations(teams, 3))

    # Track match occurrences
    matchups = {frozenset(pair): 0 for pair in all_pairs}

    # Ensure even distribution of match types
    team_trio_count = defaultdict(int)
    team_pair_count = defaultdict(int)

    schedule = []

    # Generate all 23 Spieltage
    for spieltag in range(total_matchdays):
        matchday = []
        used_teams = set()

        # Sort teams by least trio appearances
        available_trios = sorted(all_trios, key=lambda trio: sum(team_trio_count[t] for t in trio))
        random.shuffle(available_trios)  # Add randomness

        trios_added = 0
        for trio in available_trios:
            if not any(team in used_teams for team in trio):
                if all(matchups[frozenset((trio[i], trio[j]))] < games_per_pair for i in range(3) for j in
                       range(i + 1, 3)):
                    matchday.append(trio)
                    used_teams.update(trio)
                    for t in trio:
                        team_trio_count[t] += 1
                    for i in range(3):
                        for j in range(i + 1, 3):
                            matchups[frozenset((trio[i], trio[j]))] += 1
                    trios_added += 1
                    if trios_added == 2:
                        break

        # If we fail to get two trios, restart the matchday
        if trios_added < 2:
            continue

        # Sort remaining teams by least pair appearances
        remaining_teams = [t for t in teams if t not in used_teams]
        available_pairs = sorted(itertools.combinations(remaining_teams, 2),
                                 key=lambda pair: sum(team_pair_count[t] for t in pair))
        random.shuffle(available_pairs)  # Add randomness

        pairs_added = 0
        for pair in available_pairs:
            if matchups[frozenset(pair)] < games_per_pair:
                matchday.append(pair)
                matchups[frozenset(pair)] += 1
                for t in pair:
                    team_pair_count[t] += 1
                pairs_added += 1
                if pairs_added == 2:
                    break

        # If we fail to get two pairs, restart the matchday
        if pairs_added < 2:
            continue

        schedule.append(matchday)

        # If we reach Spieltag 23, ensure all matchups are used exactly 4 times
        if spieltag == total_matchdays - 1:
            missing_games = [pair for pair, count in matchups.items() if count < games_per_pair]
            while missing_games:
                for match in missing_games[:4]:  # Add up to 4 missing matches
                    matchday.append(tuple(match))
                    matchups[frozenset(match)] += 1
                missing_games = [pair for pair, count in matchups.items() if count < games_per_pair]

    return schedule

def prints_console(data):
    logging.info(data)
    print(data)

def print_schedule(schedule):
    for i, matchday in enumerate(schedule, 1):
        prints_console(f"------ match day {i} ------")
        for match in matchday:
            prints_console("-".join(map(str, match)))
        print()


# Define teams

def main(team1: str = typer.Option(...,help="Give name of team 1", prompt=True),
         team2: str = typer.Option(...,help="Give name of team 2", prompt=True),
         team3: str = typer.Option(...,help="Give name of team 3", prompt=True),
         team4: str = typer.Option(...,help="Give name of team 4", prompt=True),
         team5: str = typer.Option(...,help="Give name of team 5", prompt=True),
         team6: str = typer.Option(...,help="Give name of team 6", prompt=True),
         team7: str = typer.Option(...,help="Give name of team 7", prompt=True),
         team8: str = typer.Option(...,help="Give name of team 8", prompt=True),
         team9: str = typer.Option(...,help="Give name of team 9", prompt=True),
         team10: str = typer.Option(...,help="Give name of team 10", prompt=True),
         ):
    logging.basicConfig(filename='gameplan.txt', level=logging.DEBUG, format='')

    teams = [team1,team2,team3,team4,team5,team6,team7,team8,team9,team10]
    game_schedule = generate_schedule(teams)
    print_schedule(game_schedule)


if __name__ == "__main__":
    typer.run(main)

