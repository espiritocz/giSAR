import csv

#b=150.3
#b = float(b)

###############################################################
# Open the original file 
#out= open("C:/Users/Pedro/remote.csv") 
#rdr= csv.reader(out)

#result= open("C:/Users/Pedro/remotemix1.csv","w")
#wtr= csv.writer ( result,delimiter=',',lineterminator='\n')

#for row in rdr:
#    wtr.writerow( (row[0], row[3], row[4],row[5],row[13]) )
#out.close()
#result.close()
heigcol=[0]
latcol=[1]
total = heigcol+latcol
print total

##################################################################

with open('C:/Users/Pedro/remote.csv') as infile:  # Use 'with' to close files automatically
    reader = csv.reader(infile)
    headers = reader.next()  # Read first line

    # Figure out which columns have '-' in them (assume these are dates)
    date_columns = [col for col, header in enumerate(headers) if '-' in header]

    # Add our desired other columns
    print date_columns
    all_columns = [0, 2] + date_columns

    with open('C:/Users/Pedro/remotemix1.csv', 'w') as outfile:

        writer = csv.writer(outfile, delimiter=',', lineterminator='\n')

        # print headers
        writer.writerow([headers[i] for i in all_columns])

        # print data
        for row in reader:  # Read remaining data from our input CSV
            writer.writerow([row[i] for i in all_columns])

infile.close()
outfile.close()


filtervalue =103
# remotemix =[ID,LAT,LONG,HEIG,DATA1,DATA2,....]
height_col=1
f_input=open('C:/Users/Pedro/remotemix1.csv', 'r')
f_output=open('C:/Users/Pedro/remotemix.csv', 'wb') 
csv_input = csv.reader(f_input)
csv_output = csv.writer(f_output)

# Write the header
csv_output.writerow(next(csv_input))

for cols in csv_input:
    if float(cols[height_col]) > filtervalue:  
        csv_output.writerow(cols)
        
f_input.close()
f_output.close()      