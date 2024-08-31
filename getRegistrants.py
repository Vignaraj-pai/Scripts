import csv
import json

def csv_to_dict(file_name):
    with open(file_name, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        return [row for row in csv_reader]

def openCsvFile(fileName='registration.csv'):
    with open(fileName, 'r') as f:
        reader = csv.reader(f)
        return list(reader)[1:]

def getTeams(registrants=[]):
    teams = {}
    for row in registrants:
      if teams.get(row[0]) == None:
        teams[row[0]] = [{
          'Team Name': row[1],
          'isTeamLeader': row[2] == 'team leader',
          'Name': row[3],
          'Email': row[4],
          'Phone': row[5],
        }]
      else:
        teams[row[0]].append({
          'Team Name': row[1],
          'isTeamLeader': row[2] == 'team leader',
          'Name': row[3],
          'Email': row[4],
          'Phone': row[5],
        })
      
    return teams
  
def formatTeams(teams={}):
    formattedTeams = []
    for team in teams:
        formattedTeams.append({
            'Team Name': teams[team][0]['Team Name'],
            # select from the team members list the one that is the team leader
            'Leader': [{'Name': member['Name'], 'Email': member['Email'], 'Phone': member['Phone']} for member in teams[team] if member['isTeamLeader'] == True][0],
            'Members': [{'Name': member['Name'], 'Email': member['Email'], 'Phone': member['Phone']} for member in teams[team] if member['isTeamLeader'] == False]
        })
        
    return formattedTeams
  

def dumpTeamsJson(teams=[]):
    with open('teams.json', 'w') as f:
        f.write(json.dumps(teams))
        
def dumpTeamsCsv(teams=[]):
    with open('teams.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Team Name', 'Member 1 Name', 'Member 2 Name', 'Member 3 Name', 'Member 1 Contact Number'])
        for team in teams:
            writer.writerow([team['Team Name'], team['Leader']['Name'], team['Members'][0]['Name'] if len(team['Members']) > 0 else '', team['Members'][1]['Name'] if len(team['Members']) > 1 else '', team['Leader']['Phone']])


if __name__ == '__main__':
    registrants = openCsvFile('registration.csv')
    print('Number of registrants:', len(registrants))
    teams = getTeams(registrants)
    formattedTeams = formatTeams(teams)
    print('Number of teams:', len(formattedTeams))
    dumpTeamsJson(formattedTeams)
    dumpTeamsCsv(formattedTeams)