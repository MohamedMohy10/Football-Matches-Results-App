import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime


# get details
match_details = []
def get_league_details(league_list):
    league_title = league_list.find("div", {'class':'title'}).find("h2").text.strip() # educational: or use .contents[] (less efficient)
    matches = league_list.find("div", {'class':'ul'}).find_all("div", {'class':'item'})
    
    # looping through matches
    for match in matches:
        # team names
        team_1 = match.find("div", {'class':'teams teamA'}).text.strip()
        team_2 = match.find("div", {'class':'teams teamB'}).text.strip()
        
        # result
        match_scores = match.find('div', {'class':'MResult'}).find_all('span',{'class':'score'})
        result = f'{match_scores[0].text.strip()} - {match_scores[1].text.strip()}'
        
        # match time
        match_time = match.find('div', {'class':'MResult'}).find('span', {'class':'time'}).text.strip()
        
        # match channel
        match_channel = match.find('div', {'class':'channel icon-channel'})
        if not match_channel:
            match_channel = " "
        else:
            match_channel = match_channel.text.strip()
        # match status
        match_state = match.find('div', {'class':'matchStatus'}).text.strip()
        
        # league phase
        league_phase = match.find('div', {'class':'date'}).text.strip()

        match_details.append(
            {
                'League': league_title,
                'Phase': league_phase,
                'First team': team_1,
                'Second team': team_2,
                'Result': result,
                'Time': match_time,
                'State': match_state,
                'Channel': match_channel
            }
        )
        
# main program function:
def main(page):
    
    # read page contents
    src = page.content
    soup = BeautifulSoup(src, "lxml")
    
    league_list = soup.find_all("div", {'class':'matchCard'})

    for league in league_list:
        get_league_details(league)
    
    return(match_details)

# Create csv file from the obtained data

def create_csv(data):
    
    df = pd.DataFrame(data)
    fdate = date.replace('/', '-') #formatting the date as file names connot contain slashes
    df.to_csv(f"{fdate} Matches_Results.csv", index=False)
    print('==> file created ^_^')
    

# ====================== Tests ====================:
# Function to validate the date format
def validate_date(date):
    try:
        # Check if the date is in the required format
        datetime.datetime.strptime(date, "%m/%d/%Y")
        return True
    except ValueError:
        return False
# ============================================== Main Body ==================
# inputs
date = input("Enter date (MM/DD/YYYY):")
# Validate the date format
if not validate_date(date):
    print("Invalid date format. Please enter the date in MM/DD/YYYY format.")
else:
    try:
        page = requests.get(f"https://www.yallakora.com/match-center/%D9%85%D8%B1%D9%83%D8%B2-%D8%A7%D9%84%D9%85%D8%A8%D8%A7%D8%B1%D9%8A%D8%A7%D8%AA?date={date}#")
        data = main(page)
        create_csv(data)
    except requests.exceptions.ConnectionError:
        print("Couldn't connect :( .. The website is currently down OR Check your internet connection")


