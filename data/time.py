from datetime import datetime

fd_headers = []
fd_entries = []

with open('files/FreshDesk_time_after2.csv', 'r') as f:
  for line in f:
    if (len(fd_headers) == 0):
      fd_headers = line.decode(errors="ignore").encode().replace('\n', '').replace('\r', '').split(';')
    else:
      fd_entries.append(line.decode(errors="ignore").encode().replace('\n', '').replace('\r', '').split(';'))
    
dateIndex = fd_headers.index("Created at")
hoursIndex = fd_headers.index("Hours")
projectIndex = fd_headers.index("Project")
agentIndex = fd_headers.index("Agent")

dates = {}
entriesByDate = {}

for e in fd_entries:
  date = datetime.strptime(e[dateIndex][:10], '%Y-%m-%d').strftime('%d.%m.%Y')
  [hours, mins, secs] = e[hoursIndex].split(":")
  hours = float(hours) + float(mins) / 60
  project = e[projectIndex]
  agent = e[agentIndex].split(" ")[0]
  
  if (date not in dates):
    dates[date] = {}
  if (agent not in dates[date]):
    dates[date][agent] = []
  dates[date][agent].append(project)
  if (date not in entriesByDate):
    entriesByDate[date] = {}
  if (agent not in entriesByDate[date]):
    entriesByDate[date][agent] = 0
  entriesByDate[date][agent] += 1

toggl_headers = []
toggl_entries = []

with open('files/toggl_after.csv', 'r') as f:
  for line in f:
    if (len(toggl_headers) == 0):
      toggl_headers = line.decode(errors="ignore").encode().replace('\n', '').split(';')
    else:
      toggl_entries.append(line.decode(errors="ignore").encode().replace('\n', '').split(';'))
  
userIndex = toggl_headers.index("User")
projectIndex = toggl_headers.index("Project/Time entry")
dateIndex = toggl_headers.index("Start date")
taskIndex = toggl_headers.index("Task")

project = ""

for e in toggl_entries:
  user = e[userIndex].split(" ")[0]
  if (user == "" and e[projectIndex] != "Total"):
    project = e[projectIndex].split(' - ')[1]
  elif e[projectIndex] != "Total":
    date = e[dateIndex]
    task = e[taskIndex]
    if (date not in dates):
      dates[date] = {}
    if (user not in dates[date]):
      dates[date][user] = []
    dates[date][user].append(project)
    if (date not in entriesByDate):
      entriesByDate[date] = {}
    if (user not in entriesByDate[date]):
      entriesByDate[date][user] = 0
    entriesByDate[date][user] += 1

print "===PROJECTS==="
projectCounts = {}

for d in sorted(dates.keys()):
  for agent in dates[d].keys():
    if (agent not in projectCounts):
      projectCounts[agent] = []
    if agent == "Ilari":
      print d, set(dates[d][agent])
    projectCounts[agent].append(len(set(dates[d][agent])))
    
for agent in projectCounts.keys():
  print agent, sum(projectCounts[agent]) / float(len(projectCounts[agent]))

print "===ENTRIES==="
entryCounts = {}
entryCountsByMonth = {}
for d in sorted(entriesByDate.keys()):
  month = d[3:5]
  if (month not in entryCountsByMonth):
    entryCountsByMonth[month] = []
  for user in entriesByDate[d]:
    if (user not in entryCounts):
      entryCounts[user] = []
    entryCounts[user].append(entriesByDate[d][user])
    if (user in ["Markus", "Kaarlo", "Marcus", "Lassi", "Marco", "Juha"]):
      entryCountsByMonth[month].append(entriesByDate[d][user])
  
for user in entryCounts.keys():
  print user, sum(entryCounts[user]) / float(len(entryCounts[user]))
  
for month in sorted(entryCountsByMonth.keys()):
  if (len(entryCountsByMonth[month]) > 0):
    print month, sum(entryCountsByMonth[month]) / float(len(entryCountsByMonth[month]))
  else:
    print month, 0