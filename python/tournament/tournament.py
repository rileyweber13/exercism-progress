"""
takes text of format 'Allegoric Alaskans;Blithering Badgers;win' and converts
it to a human-readable table that looks like this:

Team                           | MP |  W |  D |  L |  P
Allegoric Alaskans             |  1 |  1 |  0 |  0 |  3
Blithering Badgers             |  1 |  0 |  0 |  1 |  0
"""

from operator import itemgetter

def build_results_dict(tournament_results):
    """
    builds results. Returns an object of the following form:
    {
        team-1: {
            matches_played: int,
            wins: int,
            draws: int,
            losses: int,
            points: int,
        }
        team-2: {
            ...
        }

        ...

        team-n: {
            ...
        }
    }
    """
    if tournament_results == '':
        return {}

    team_stats_dict = {}
    array_of_input = []
    lines = tournament_results.split('\n')
    for line in lines:
        array_of_input.append(line.split(';'))

    for result in array_of_input:
        for team in result[0:2]:
            if team not in team_stats_dict:
                team_stats_dict[team] = {'matches_played': 0,
                                         'wins': 0,
                                         'draws': 0,
                                         'losses': 0,
                                         'points': 0,}

        if result[2] == "win":
            team_stats_dict[result[0]]['wins'] += 1
            team_stats_dict[result[0]]['points'] += 3
            team_stats_dict[result[1]]['losses'] += 1
        elif result[2] == "loss":
            team_stats_dict[result[0]]['losses'] += 1
            team_stats_dict[result[1]]['wins'] += 1
            team_stats_dict[result[1]]['points'] += 3
        elif result[2] == "draw":
            team_stats_dict[result[0]]['draws'] += 1
            team_stats_dict[result[1]]['draws'] += 1
            team_stats_dict[result[0]]['points'] += 1
            team_stats_dict[result[1]]['points'] += 1

        team_stats_dict[result[0]]['matches_played'] += 1
        team_stats_dict[result[1]]['matches_played'] += 1
    return team_stats_dict

def convert_stats_dict_to_sorted_array(team_stats):
    """
    justification: it's easy to build this data using a dictionary of
    dictionaries, but you can't sort a dictionary. Converting to a list later
    is significantly easier than trying to have an array of objects form the
    beginning

    takes a dict of team stats dicts, as returned by build_results_dict.
    returns an array of objects of the following format:
    {
        team_name: String,
        matches_played: int,
        wins: int,
        draws: int,
        losses: int,
        points: int,
    }
    """
    stats_array = []
    for team in team_stats:
        stats_array.append({
            'team_name': team,
            'matches_played': team_stats[team]['matches_played'],
            'wins': team_stats[team]['wins'],
            'draws': team_stats[team]['draws'],
            'losses': team_stats[team]['losses'],
            'points': team_stats[team]['points'],
        })

    # we want list sorted first by points and then by team_name.
    # Counter-intuitively, this means we have to first sort by team_name to
    # make sure list is alphabetized and then sort by points.
    stats_array.sort(key=itemgetter('team_name'))
    stats_array.sort(key=itemgetter('points'), reverse=True)
    # below lines also work, but need a python function call
    # stats_array.sort(key=lambda k: k['team_name'])
    # stats_array.sort(key=lambda k: k['points'], reverse=True)
    return stats_array

def build_table(team_stats):
    """
    returns string representing human-readable table of results using the
    object returned from convert_stats_dict_to_sorted_array
    """
    table = '{0:<31s}| {1:>2s} | {2:>2s} | {3:>2s} | {4:>2s} | {5:>2s}' \
            .format('Team', 'MP', 'W', 'D', 'L', 'P')
    stats_array = convert_stats_dict_to_sorted_array(team_stats)
    for team in stats_array:
        table += '\n'
        table += '{0:<31}| {1:>2} | {2:>2} | {3:>2} | {4:>2} | {5:>2}' \
                .format(team['team_name'], team['matches_played'],
                        team['wins'], team['draws'], team['losses'],
                        team['points'])
    return table

def tally(tournament_results):
    """
    wrapper function to do all the work
    """
    stats = build_results_dict(tournament_results)
    return build_table(stats)
