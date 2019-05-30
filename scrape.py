#!/usr/bin/env python3

import requests
import sys
import json
from bs4 import BeautifulSoup

def get_tier_list(lane):
    """
    gets a tier list from a specified lane
    lane options:
            "TOP"
            "JUNGLE"
            "MID"
            "ADC"
            "SUPPORT"
    """
    lane = lane.upper()
    data = requests.get("https://na.op.gg/champion/statistics")
    soup = BeautifulSoup(data.text, "html.parser")
    ranks = soup.find("table", {"class": "champion-index-table tabItems"})
    tbodyclass = "tabItem champion-trend-tier-" + lane
    tbody = ranks.find("tbody", {"class": tbodyclass})

    place, name, win_rate, ban_rate = [],[],[],[]

    for tr in tbody.find_all("tr"):
        raw = tr.find_all("td")
        data = {}
        place.append(raw[0].text.strip())
        name.append(raw[3].find("a").find("div").text.strip())
        win_rate.append(raw[4].text.strip())
        ban_rate.append(raw[5].text.strip())

    return place, name, win_rate, ban_rate


def disp_tier_list_head(lane):
    """
    Displays table headers and lables for tier lists
    """
    if (lane == "all"):
        for i in ["top", "jungle", "mid", "adc", "support"]:
            disp_tier_list_head(i)
    else:
        print("\n"+ lane.upper() + " TIER LIST\n\nTier\t\tName\t\tWin Rate\tBan Rate")
        place, name, win_rate, ban_rate = get_tier_list(lane)

        disp_tier_list(place, name, win_rate, ban_rate, lane)


def disp_tier_list(place, name, win_rate, ban_rate, lane):
    """
    Displays data returned from tier lists
    """
    for i in range(0,len(place)):
            if len(name[i]) >= 8:
                    print(place[i] + "\t\t" +  name[i] + "\t" +  win_rate[i] + "\t\t" + ban_rate[i])
            else:
                    print(place[i] + "\t\t" +  name[i] + "\t\t" +  win_rate[i] + "\t\t" + ban_rate[i])


def get_skill_order(lane, name):
    """
    Gets skill order of specific champion and lane
    """
    data = requests.get("https://na.op.gg/champion/" + name + "/statistics/" + lane)
    soup = BeautifulSoup(data.text, "html.parser")
    skills = soup.find("table", {"class": "champion-skill-build__table"})
    tbody = skills.find("tbody")
    tr = tbody.find_all("tr")[1]
    skill_table = []
    for td in tr.find_all("td"):
        if td.text.strip() == 'Q' or td.text.strip() == 'W' or  td.text.strip() == 'R' or td.text.strip() == 'E':
            skill_table.append(td.text.strip())

    return skill_table


def disp_skill_order(lane, name):
    """
    Displays skill order of a specific champion and lane
    """
    skills = get_skill_order(lane, name)
    outstring = ""
    for i in skills:
        outstring = outstring + i + "->"
    print(outstring[:-2])


def help_message():
    """
    Deals with invalid argument input
    """
    print("USAGE:\n\t\"-t {lane}\" or \"-t all\" to get tier list\n\t\"-so {champion} {lane}\" to get skill order")


def main():
    try:
        if sys.argv[1] == "-t" and sys.argv[2] in ["top", "TOP", "adc", "ADC", "mid", "MID", "jungle", "JUNGLE", "all", "ALL", "support", "SUPPORT"]:
            disp_tier_list_head(sys.argv[2])
        elif sys.argv[1] == "-so":
            disp_skill_order(sys.argv[3], sys.argv[2])
        else:
            help_message()

    except requests.exceptions.ConnectionError:
        print("\nCONNECTION ERROR - check connection and try again")

    except:
        help_message()


if __name__ == "__main__":
    main()
