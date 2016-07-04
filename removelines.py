##########################
# Remove linhas filtro
###########################

import csv
import os

#orig = open('C:/Users/Pedro/peso.csv', 'r')
#modi = open('C:/Users/Pedro/peso2.csv', 'w')

#header
#modi.write(orig.readline())

# data lines
#for line in orig:
#    if line.split(',')[2] <=75:
#        modi.write(line)

#orig.close()
#modi.close()

b=150.3
b = float(b)
print b
a=5
print a


import csv

with open('C:/Users/Pedro/remote.csv', 'r') as f_input, open('C:/Users/Pedro/remotevel30.csv', 'wb') as f_output:
    csv_input = csv.reader(f_input)
    csv_output = csv.writer(f_output)

    # Write the header
    csv_output.writerow(next(csv_input))

    for cols in csv_input:
        print cols[a]
        if float(cols[5]) > b:    # Keep weights <= 75
            csv_output.writerow(cols)
            
#csv_input.close()
#csv_output.close()

