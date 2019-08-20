lines = []

with open('files/FreshDesk_Tickets_Created_20180101-20181231.xls') as f:
  for line in f:
    parsed = line.replace('\n', '')
    if (len(parsed) > 10):
      lines.append(parsed)

with open('files/FreshDesk_tickets.csv', 'w+') as out:
  for line in lines:
    if ('</ss:Row>' in line):
      out.write('\n')
    elif ('<ss:Cell>' in line):
      out.write(line.split('>')[2].split('<')[0].replace(";", " ") + ";")