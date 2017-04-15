import re
import csv
import time
import requests
from bs4 import BeautifulSoup

#------------------------------------------------------------

def user_main():
    create_nba_dict = get_wiki_names_and_symbols()
    create_user_symbol = user_team_name(create_nba_dict)
    team_stats = merge_urls(create_user_symbol)
    csv_file = create_csv(team_stats)
    print('\n')
    print ("We just created a file with all of your team's stats!")
    print('\n' * 2)
    user = input("Would you like to see all team's stats? (yes/no) ")
    if user == 'yes':
        auto_main()
    else:
        pass

def get_wiki_names_and_symbols():
    baseurl = 'https://en.wikipedia.org/wiki/Wikipedia:WikiProject_National_Basketball_Association/National_Basketball_Association_team_abbreviations'
    r = requests.get(baseurl)
    soup = BeautifulSoup(r.text,'lxml')
    lines = soup.find_all('tr')[1:]
    NBAdict = {}
    for line in lines:
        tName = line.a.get('title').lower()
        tSym = line.td.string.lower()
        if tName == 'new orleans pelicans':
            NBAdict[tName] = tSym[:-1]
        elif tName == 'utah jazz':
            NBAdict[tName] = tName[:4]
        else:
            NBAdict[tName] = tSym[:]

    return NBAdict


def user_team_name(NBAdict): #return string and symbol matching input
    inp = input('Enter Name of NBA Team: ').lower()
    if len(inp) < 5:
        if inp!= 'utah' and inp!='jazz' and inp != 'nets' and inp!='heat':
            inp = input('Please Enter at least 5 characters ').lower()
        else:
            pass
    keys = NBAdict.keys()
    test =''
    for word in keys:
        test = test + ' ' + word
    if inp not in test or (len(inp) < 5 and (inp!= 'utah' and inp!='jazz' and inp!='nets' and inp!='heat')):
        while inp not in test or len(inp) < 5:
            inp = input('Try Again! Hint - Try just typing part of the teams name (ex. rockets): ').lower()
    inp_sym =''
    for key in keys:
        if inp == key or inp in key:
            inp_sym = NBAdict[key]

    return inp_sym


def merge_urls(inp_sym): #will need to split team name and add - between each word, and add symbol
    base_url = 'http://www.espn.com/nba/team/stats/_/name/{}'#url.format(symb,name) **name not acutally needed but would look good to include
    r = requests.get(base_url.format(inp_sym))
    soup = BeautifulSoup(r.text, 'lxml')
    table = soup.find_all('tr')[2:16]
    keep = []
    stats = {}
    player_list = []
    for player in table:
        if player.a:
            if len(player.a.string) > 4:
                keep.append(player.a.string)
            else:
                pass
    for player in table:
        if player.a:
            if len(player.a.string) > 4:
                may = player.find_all('td')[1:]
                stats[player.a.string] = {}
                stats[player.a.string]['GP'] = may[0].string
                stats[player.a.string]['GS'] = may[1].string
                stats[player.a.string]['MPG'] = may[2].string
                stats[player.a.string]['PPG'] = may[3].string
                stats[player.a.string]['OFFR'] = may[4].string
                stats[player.a.string]['DEFR'] = may[5].string
                stats[player.a.string]['RPG'] = may[6].string
                stats[player.a.string]['APG'] = may[7].string
                stats[player.a.string]['SPG'] = may[8].string
                stats[player.a.string]['BPG'] = may[9].string
                stats[player.a.string]['TPG'] = may[10].string
                stats[player.a.string]['FPG'] = may[11].string
                stats[player.a.string]['A/TO'] = may[12].string
                stats[player.a.string]['PER'] = may[13].string
                player_list.append(stats)
                stats = {}
            else:
                continue
    return player_list


def create_csv(player_list, filename = 'Player_Stats_On_Desired_Team.csv', fieldnames=["Player Name","GP", "GS","MPG","PPG","OFFR","DEFR", "RPG","APG","SPG","BPG","TPG","FPG","A/TO","PER"]):
    with open(filename, 'w+', newline='') as f:
        row_writer = csv.DictWriter(f, delimiter=',', quotechar='"', extrasaction='ignore',
                                    fieldnames=fieldnames)
        row_writer.writeheader()

        players_on_team = []
        for name in player_list:
            for pname in name.keys():
                players_on_team.append(pname)

        player_entry_count = 0
        line =[]
        for dicts in player_list:
            line.append(players_on_team[player_entry_count])
            newlist = []
            for i in dicts.values():
                newlist.append(i)
                for j in i.values():
                    line.append(j)
            player_entry_count += 1
            name_writer = csv.DictWriter(f, delimiter=',', quotechar='"', extrasaction='ignore',
                                         fieldnames=line)
            name_writer.writeheader()
            line = []
    return


#---------------------------------------------------



def auto_main():

    nba_dict = get_wiki_names_and_symbols()
    population = read_from_csv(nba_dict)
    write = create_pair(population)

    with open('Team Divisions.csv', 'w') as f:
        row_writer = csv.DictWriter(f, delimiter=',', quotechar='"', extrasaction='ignore',
                                    fieldnames=['Team', 'Division'])
        row_writer.writeheader()

        for item in nba_dict.values():
            symbols = merge_urls(item)
            #all_teams = create_csv(symbols,filename='Player Stats {}.csv'.format(item.upper()))
            print("We just created a file for", item.upper(), "stats")
            standings = get_records(item)
            output = dict_to_list(standings)
            new_writer = csv.DictWriter(f, delimiter=',', quotechar='"', extrasaction='ignore', fieldnames=output)
            new_writer.writeheader()

    print ("Gathering team records...", '\n')
    time.sleep(5)
    print("We just made a file with all team's records!")
    #print (essay)

def read_from_csv(NBAdict):

    country = 5
    pop = 4
    city = 0
    list_city_pop =[]

    with open("worldCities.csv",'r') as f:
        reader = csv.reader(f)
        for row in reader:
            for item in NBAdict.keys():
                if row[country] == 'United States of America' or row[city] == 'Toronto':
                    if row[city].lower() in item and row[city] != 'York':
                        list_city_pop.append([row[city], row[pop]])
    return (list_city_pop)

def create_pair(list_city_pop):
    with open('Team City Populations.csv', 'w') as f:
        row_writer = csv.DictWriter(f, delimiter=',', quotechar='"', extrasaction='ignore',
                                    fieldnames=['City', 'Population'])
        row_writer.writeheader()
        for item in list_city_pop:
            iWrite = csv.DictWriter(f, delimiter=',', quotechar='"', extrasaction='ignore', fieldnames=item)
            iWrite.writeheader()

def get_records(inp_sym):
    base_url = 'http://www.espn.com/nba/team/stats/_/name/{}'  # url.format(symb,name) **name not acutally needed but would look good to include
    r = requests.get(base_url.format(inp_sym))
    soup = BeautifulSoup(r.text, 'lxml')
    table = soup.find_all(class_ = 'sub-title')
    record_pair = {}
    for item in table:
        #record = re.search(r'[0-9]{2}-[0-9]{2}', item.string) #this was to get the record, but that dissappeared from page, so had to adjust project
        record_pair[inp_sym] = item.string
        return record_pair

def dict_to_list(record_pair):
    list_for_out = []
    for item in record_pair:
        list_for_out.append(item)
    for chunk in record_pair.values():
        list_for_out.append(chunk)
    return list_for_out


user_main()
#auto_main()


