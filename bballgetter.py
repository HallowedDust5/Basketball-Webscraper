
from bs4 import BeautifulSoup as bs 
import requests,json
master_player_data =[]
LETTERS = 'abcdefghijklmnopqrstuvwxyz'
with open("master_player_data","r") as f:
    master_player_data = json.loads(f.read())

for letter in LETTERS[20:]:
    SITE_URL = r"https://www.basketball-reference.com"
    URL = fr"https://www.basketball-reference.com/players/{letter}/"
    site = bs(
        requests.get(URL).text,
        'html.parser'
    )
    table = site.table



    player_data = []
    for tr in table.find_all('tr')[1:]:
        tr_data = []
        name = tr.th.a.contents[0]
        link = tr.th.a['href']
        try:
            weight = [td.contents for td in tr if td["data-stat"]=="weight"][0][0]
        except :
            weight = [td.contents for td in tr if td["data-stat"]=="weight"][0]

        
        

        tr_data.append(name)
        tr_data.append(SITE_URL+link)
        tr_data.append(weight)


        player_data.append(tr_data)




    for player in player_data:
        name = player[0]
        link = player[1]

        player_site = bs(
        requests.get(link).text,
        'html.parser'
        )
        ft =[]
        try:
            ft = [span.next_sibling.next_sibling.next_sibling.contents[0] for span in player_site.find_all("span") if span.has_attr("data-tip") and span["data-tip"]=="Free Throw Percentage"][0]
        except:
            pass
        player.append(ft)




    for player in player_data:
        master_player_data.append({"name":player[0],"weight":player[2],"Free Throw Percentage":player[3]})


with open("master_player_data","w") as f:
     f.write(json.dumps(master_player_data))


