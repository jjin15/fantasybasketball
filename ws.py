#!/usr/bin/python3
import urllib.request as request
from bs4 import BeautifulSoup
import re
import pymysql
db = pymysql.connect(host='localhost', user='root', passwd='fdsa', db='bdata')
cursor = db.cursor()
cursor.execute("delete from players;")
base_url = 'http://www.espn.com/nba/team/stats/_/name/'

teams_url = 'http://www.espn.com/nba/teams'
html_teams = request.urlopen(teams_url)

soup_teams = BeautifulSoup(html_teams, "html.parser")
urls = soup_teams.find_all(href=re.compile('/nba/teams/stats'))
team_urls = [base_url+(url['href'])[-3:] + '/year/2016' for url in urls]
for team in team_urls:
  print(team)
  team_name_input = team[42:45]
  html_ind_teams = request.urlopen(team)
  soup_team = BeautifulSoup(html_ind_teams, "html.parser")
  roster = soup_team.find_all('tr', class_=re.compile('player'))
  roster_game_stats = roster[:int(len(roster)/2)]
  players = []
  for row in roster_game_stats:
  	for data in row:
  		players.append(data.get_text())
  	players.append(team_name_input)
  playerList = []
  index = 0
  while index < len(players):
  	playerList.append(players[index:index+16])
  	index = index + 16
  pindex = 0
  while pindex < len(playerList):
  	playerList[pindex][0]=playerList[pindex][0].split(',',1)[0]
  	i = 1
  	while i < len(playerList[pindex]) - 1:
  		playerList[pindex][i] = float(playerList[pindex][i])
  		i += 1
  	pindex+=1

  sql = """INSERT INTO players(name, gp, gs, min, ppg, oreb, dreb, reb, ast, stl, blk, tov, fls, ato, per, team) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
  cursor.executemany(sql, playerList)
  db.commit();
db.close()