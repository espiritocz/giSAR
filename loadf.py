##########################
# Remove colunas 
###########################

import csv

out= open("C:/Users/Pedro/remote.csv") 
rdr= csv.reader(out)

result= open("C:/Users/Pedro/remotevel.csv","w")
wtr= csv.writer ( result,delimiter=',',lineterminator='\n')

for row in rdr:
    wtr.writerow( (row[3], row[4], row[8],row[13]) )
out.close()
result.close()

#nameloadfile="""C:/Users/Pedro/remotevel.csv"""
#InFlnm = nameloadfile
#InDrPth=filename
#InFlPth="file:///"+InDrPth
#uri1 = InFlPth+"?delimiter=%s&xField=%s&yField=%s&crs=epsg:4326" % (",","LON","LAT")

InFlnm='Heigt Values2222'
InDrPth='C:/Users/Pedro/remotevel.csv'
InFlPth="file:///"+InDrPth
uri1 = InFlPth+"?delimiter=%s&xField=%s&yField=%s" % (",","LON","LAT")
lyr = QgsVectorLayer(uri1, InFlnm, "delimitedtext")

##uri += """type=csv&"""
#uri += """delimiter=","&"""
##uri += """trimFields=Yes&"""
#uri += """xField="LONG"&"""
#uri += """yField="LAT"&"""
#uri += """crs=epsg:4326"""

uri = InFlPth+"?delimiter=%s&xField=%s&yField=%s&crs=epsg:4326" % (",","LON","LAT")
layer=QgsVectorLayer(uri,"pedro","delimitedtext")
QgsMapLayerRegistry.instance().addMapLayers([layer])