headers = []
tickets = []

def toSeconds(time):
  entries = time.split(':')
  if (len(entries) == 3):
    return int(entries[0]) * 60 * 60 + int(entries[1]) * 60 + int(entries[2])
  return 0

with open('files/FreshDesk_tickets_after2.csv', 'r') as f:
  for line in f:
    arr = line.replace('\n', '').split(';')
    if (len(headers) == 0):
      headers = arr
    else:
      tickets.append(arr)
      
resolutionTimeIndex = headers.index("Resolution time (in hrs)")
ticketIdIndex = headers.index("Ticket ID")
priorityIndex = headers.index("Priority")
typeIndex = headers.index("Type")
sourceIndex = headers.index("Source")
contactIdIndex = headers.index("Contact ID")
slaStatusIndex = headers.index("Resolution status")
customerInteractionsIndex = headers.index("Customer interactions")
createdIndex = headers.index("Created time")

totalResolutionTime = 0
totalCustomerInteractions = 0
resolutionTimesByPriority = {}
ticketsByType = {}
ticketsByPriority = {}
ticketsBySource = {}
ticketsByDomain = {}
ticketsBySlaStatus = {}
resolutionTimesByMonth = {}
  
tickets = filter(lambda x : int(x[resolutionTimeIndex].split(':')[0]) < 1000 and x[typeIndex] != "", tickets)

for t in tickets:
  ticketId = t[ticketIdIndex]
  priority = t[priorityIndex]
  type = t[typeIndex]
  source = t[sourceIndex]
  domain = t[contactIdIndex].split('@')[1]
  slaStatus = t[slaStatusIndex]
  customerInteractions = int(t[customerInteractionsIndex])
  resolutionTime = toSeconds(t[resolutionTimeIndex])
  totalResolutionTime += resolutionTime
  totalCustomerInteractions += customerInteractions
  month = t[createdIndex].split('-')[1]
  
  if (priority not in resolutionTimesByPriority):
    resolutionTimesByPriority[priority] = [resolutionTime]
  else:
    resolutionTimesByPriority[priority].append(resolutionTime)
    
  if (type not in ticketsByType):
    ticketsByType[type] = 1
  else:
    ticketsByType[type] += 1

  if (type != "Info"):
    if (priority not in ticketsByPriority):
      ticketsByPriority[priority] = 1
    else:
      ticketsByPriority[priority] += 1
    
    if (source not in ticketsBySource):
      ticketsBySource[source] = 1
    else:
      ticketsBySource[source] += 1

    if (domain not in ticketsByDomain):
      ticketsByDomain[domain] = 1
    else:
      ticketsByDomain[domain] += 1

    if (slaStatus not in ticketsBySlaStatus):
      ticketsBySlaStatus[slaStatus] = 1
    else:
      ticketsBySlaStatus[slaStatus] += 1

    if (month not in resolutionTimesByMonth):
      resolutionTimesByMonth[month] = { "Low": [], "Medium": [], "High": [], "Urgent": [], "Total": []}

    resolutionTimesByMonth[month][priority].append(resolutionTime)
    resolutionTimesByMonth[month]["Total"].append(resolutionTime)
  
#print "===== RESOLUTION TIME ====="
#print "Total: %.2f" % (totalResolutionTime / len(tickets) / 60.0 / 60.0)
'''
for p in resolutionTimesByPriority.keys():
  arr = resolutionTimesByPriority[p]
  print "%s: %.2f (%d)" % (p, sum(arr) / float(len(arr)) / 60.0 / 60.0, len(arr))
'''  
print "===== TICKETS BY TYPE ====="
for t in ticketsByType.keys():
  print "%s: %d" % (t, ticketsByType[t])
  
print "Total: %d" % len(tickets)

print "===== TICKETS BY PRIORITY ====="
for p in ticketsByPriority.keys():
  print "%s: %d" % (p, ticketsByPriority[p])
  
print "Total: %d" % len(tickets)

print "===== TICKETS BY SOURCE ====="
for t in ticketsBySource.keys():
  print "%s: %d" % (t, ticketsBySource[t])
  
print "===== TICKETS BY DOMAIN ====="
for t in ticketsByDomain.keys():
  print "%s: %d" % (t, ticketsByDomain[t])
  
  
print "===== TICKETS BY SLA STATUS ====="
for t in ticketsBySlaStatus.keys():
  print "%s: %d" % (t, ticketsBySlaStatus[t])
  
print "===== CUSTOMER INTERACTIONS ====="
print "Average: %.2f" % (totalCustomerInteractions / float(len(tickets)))

print "===== RESOLUTION TIMES BY MONTH ====="

totalTicketsByMonth = {}

for month in resolutionTimesByMonth.keys():
  totalTicketsByMonth[month] = sum(map(lambda x : len(x), resolutionTimesByMonth[month].values()[:-1]))
  for priority in resolutionTimesByMonth[month]:
    
    if (len(resolutionTimesByMonth[month][priority]) > 0):
      resolutionTimesByMonth[month][priority] = sum(resolutionTimesByMonth[month][priority]) / float(len(resolutionTimesByMonth[month][priority])) / 60.0 / 60.0
    else:
      resolutionTimesByMonth[month][priority] = 0
    
for month in sorted(resolutionTimesByMonth):
  lowTime = resolutionTimesByMonth[month]["Low"]
  medTime = resolutionTimesByMonth[month]["Medium"]
  highTime = resolutionTimesByMonth[month]["High"]
  urgentTime = resolutionTimesByMonth[month]["Urgent"]
  totalTime = resolutionTimesByMonth[month]["Total"]
  amount = totalTicketsByMonth[month]
  
  print month, lowTime, medTime, highTime, urgentTime, totalTime, amount