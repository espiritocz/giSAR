import csv
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import resources_rc

def format_rwt_file(filename,self):
    # Atualiza a caixa
    self.dlg.lineEdit.setText(filename)
    # Abre o ficheiro
    uploadfile = open (filename)
    x = uploadfile.read()
    # Ler as primeiras strings 
    # Ficheiro SAR PROZ : Options for time series generation
    # Ficheiro STAMPS : ID,SVET, LVET
    strtype=x[0:6]
    
    if strtype == 'Option':
        self.dlg.filetype.setText('Loaded By: SAR-PROZ')
        # Nome da Layer
        nameloadfile ='SAR-PROZ'
        #filename =C:/Users/Pedro/../00_SARPROZ/OK_PHA_RESIDUALS.csv
               
        name = filename.split('/')
        last_name = name[-1]
        #last name = OK_PHA_RESIDUALS.csv
        SPR_file = filename.replace(last_name,"SPR.csv")
        #SPR_file =C:/Users/Pedro/Desktop/PROJ_FILES/00_SARPROZ/SPR.csv
        
        pos = x.find("ID,")
        xx  = x[pos:]
        outputfile = open (SPR_file, 'w')
        outputfile.write (xx)
        
        uploadfile.close ()
        outputfile.close()

    else:
        self.dlg.filetype.setText('Loaded By: STAMPS')
        #Nome da Layer
        nameloadfile='StAMPs'
        name = filename.split('/')
        last_name = name[-1]
        #last name = Phyton.csv
        STP_file = filename.replace(last_name,"SPR.csv")
        #SPR_file =C:/Users/Pedro/Desktop/PROJ_FILES/00_SARPROZ/SPR.csv
        
        pos = x.find("ID,")
        xx  = x[pos:]
        
        outputfile = open (STP_file, 'w')
        outputfile.write (xx)
        
        uploadfile.close ()
        outputfile.close()
    
    return nameloadfile

def creat_rwt_files(layer,filename,last,lyr):
    idCOHER  = layer.fieldNameIndex('COHER')  # id da coluna ID
    idHEIG   = layer.fieldNameIndex('HEIGHT')
    idRHEIG  = layer.fieldNameIndex('SIGMA HEIGHT')
    idVEL    = layer.fieldNameIndex('VEL')
    
    if idHEIG == 5: 
        #print " Existe Heigh"
        output_file = open(filename.replace(last,"QGHEIGH.csv"), 'w')
        line= 'LAT,LON,HEIGHT\n'
        unicode_line = line.encode('utf-8')
        output_file.write(unicode_line)
        for f in lyr.getFeatures():
            line= '%s, %s, %f \n' % (f['LAT'], f['LON'], f['HEIGHT'])
            unicode_line = line.encode('utf-8')
            output_file.write(unicode_line)
        output_file.close()
        
    if idVEL == 8: 
        #print " Existe VEL"
            output_file = open(filename.replace(last,"QGVEL.csv"), 'w')
            line= 'LAT,LON,VEL,COHER\n'
            unicode_line = line.encode('utf-8')
            output_file.write(unicode_line)
            for f in lyr.getFeatures():
                line= '%s, %s, %f, %f \n' % (f['LAT'], f['LON'], f['VEL'], f['COHER'])
                unicode_line = line.encode('utf-8')
                output_file.write(unicode_line)
            output_file.close()
    if idCOHER == 11: 
        output_file = open(filename.replace(last,"QGCOHER.csv"), 'w')
        line= 'LAT,LON,COHER\n'
        unicode_line = line.encode('utf-8')
        output_file.write(unicode_line)
        for f in lyr.getFeatures():
            line= '%s, %s, %f \n' % (f['LAT'], f['LON'], f['COHER'])
            unicode_line = line.encode('utf-8')
            output_file.write(unicode_line)
        output_file.close()
        
    if idRHEIG == 7: 
        output_file = open(filename.replace(last,"QGRHEIG.csv"), 'w')
        line= 'LAT,LON,SIGMA HEIGHT\n'
        unicode_line = line.encode('utf-8')
        output_file.write(unicode_line)
        for f in lyr.getFeatures():
            line= '%s, %s, %f \n' % (f['LAT'], f['LON'], f['SIGMA HEIGHT'])
            unicode_line = line.encode('utf-8')
            output_file.write(unicode_line)
        output_file.close()
         
    return [idCOHER,idHEIG,idRHEIG,idVEL ]
    
def update_rwt_form(layer,self,filename):
    
    # Cria uma layer
    name = filename.split('/')
    last_name = name[-1]
    SPR_file = filename.replace(last_name,"SPR.csv")
    InFlnm='RWT_LAYER'
    InDrPth=SPR_file
    InFlPth="file:///"+InDrPth
    uri1 = InFlPth+"?delimiter=%s&xField=%s&yField=%s&crs=epsg:4326" % (",","LON","LAT")
    layer = QgsVectorLayer(uri1, InFlnm, "delimitedtext")
        
    #idCOHER = list_id[0]
    #idHEIG  = list_id[1]
    #idRHEIG = list_id[2]
    #idVEL   = list_id[3]
    idCOHER  = layer.fieldNameIndex('COHER')  # id da coluna ID
    idHEIG   = layer.fieldNameIndex('HEIGHT')
    idRHEIG  = layer.fieldNameIndex('SIGMA HEIGHT')
    idVEL    = layer.fieldNameIndex('VEL')
    
    # Max and min values
    maxheight    = layer.maximumValue (idHEIG) # Valor maximo dessa layer
    minheight    = layer.minimumValue (idHEIG) # Valor minimo dessa layer
    maxcoherence = layer.maximumValue (idCOHER) # Valor maximo dessa layer
    mincoherence = layer.minimumValue (idCOHER) # Valor minimo dessa laye
    maxresheig   = layer.maximumValue (idRHEIG) # Valor maximo dessa layer
    minresheig   = layer.minimumValue (idRHEIG) # Valor minimo dessa laye
    maxlosvel    = layer.maximumValue (idVEL) # Valor maximo dessa layer
    minlosvel    = layer.minimumValue (idVEL) # Valor minimo dessa laye
    
    # convert to string
    minheight= "%s" % minheight
    maxheight= "%s" % maxheight
    mincoherence= "%s" % mincoherence
    maxcoherence= "%s" % maxcoherence
    minresheig= "%s" % minresheig
    maxresheig= "%s" % maxresheig
    minlosvel= "%s" % minlosvel
    maxlosvel= "%s" % maxlosvel
    #minlosvel = '--'
    self.dlg.minlosvel.setText(minlosvel)
    #maxlosvel = '--'
    self.dlg.maxlosvel.setText(maxlosvel)
    #minheight = '23'
    self.dlg.minheight.setText(minheight)
    #maxheight = '23'
    self.dlg.maxheight.setText(maxheight)
    #mincoherence = '23'
    self.dlg.mincoherence.setText(mincoherence)
    #maxcoherence = '23'
    self.dlg.maxcoherence.setText(maxcoherence)
    mintemp = '--'
    self.dlg.mintemp.setText(mintemp)
    maxtemp = '--'
    self.dlg.maxtemp.setText(maxtemp)
    #minresheig = '--'
    self.dlg.minresheig.setText(minresheig)
    #maxresheig = '--'
    self.dlg.maxresheig.setText(maxresheig)

def read_filter_form(self):
    # Max and min values read from form
    maxheightread      = float(self.dlg.maxheight.text()) 
    minheightread      = float(self.dlg.minheight.text()) 
    maxcoherenceread   = float(self.dlg.maxcoherence.text()) 
    mincoherenceread   = float(self.dlg.mincoherence.text()) 
    maxresheigread     = float(self.dlg.maxresheig.text()) 
    minresheigread     = float(self.dlg.minresheig.text()) 
    maxlosvelread      = float(self.dlg.maxlosvel.text()) 
    minlosvelread      = float(self.dlg.minlosvel.text())
    labelcoherenceread = float(self.dlg.labelcoherence.text())
    
    return [labelcoherenceread,maxlosvelread,minlosvelread,maxresheigread,minresheigread]

def creat_rwt_los_csvfiles(nameloadfile,filename,form_values):
    name=filename.split('/')
    #VelFlnm='LOSVEL'
    last_name=name[-1] #last name = OK_PHA_RESIDUALS.csv
    
    #nameloadfile='SAR-PROZ'
    
#    if nameloadfile=='SAR-PROZ':
    
    SPR_file = filename.replace(last_name,"SPR.csv")
        #SPR_file =C:/Users/Pedro/Desktop/PROJ_FILES/00_SARPROZ/SPR.csv
        
    SPRwf_file = filename.replace(last_name,"SPRvwf.csv")
        #SPR_file =C:/Users/Pedro/Desktop/PROJ_FILES/00_SARPROZ/SPRwf.csv
        
    SPRf_file = filename.replace(last_name,"SPRvf.csv")
        #SPR_file =C:/Users/Pedro/Desktop/PROJ_FILES/00_SARPROZ/SPRwf.csv
        
        #latcol    = [3]
        #longcol   = [4]
        #velcol    = [8]
        #cohercol  = [11]
        
        #totalcol  = latcol+longcol+velcol+cohercol
                
    with open(SPR_file) as infile:  # Use 'with' to close files automatically
        reader = csv.reader(infile)
        headers = reader.next()  # Read first line
            # Figure out which columns have '-' in them (assume these are dates)
        date_columns = [col for col, header in enumerate(headers) if '-' in header]
            
        lat_col = [col for col, header in enumerate(headers) if 'LAT' in header]
        long_col = [col for col, header in enumerate(headers) if 'LON' in header]
        vel_col = [col for col, header in enumerate(headers) if 'VEL' in header]
        coher_col = [col for col, header in enumerate(headers) if 'COHER' in header]
            #vel_col =vel_col[0]
        vel_col= [vel_col[0]]
        print lat_col
        print long_col
        print vel_col
        print coher_col
            
        totalcol  = lat_col+long_col+vel_col+coher_col
            # Add our desired other columns
            #print date_columns
            #all_columns = [0, 2] + date_columns
        all_columns = totalcol + date_columns
            #print all_columns
            
        with open(SPRwf_file,'w') as outfile:
            writer = csv.writer(outfile, delimiter=',', lineterminator='\n')
                # print headers
            writer.writerow([headers[i] for i in all_columns])
                # print data
            for row in reader:  # Read remaining data from our input CSV
                writer.writerow([row[i] for i in all_columns])
        
    infile.close()
    outfile.close()
        
    #filtervalue =103
    
    maxlosvelread      = form_values[1]  
    minlosvelread      = form_values[2]
    labelcoherenceread = form_values[0]
    
    # remotemix =[LAT,LONG,VEL,COHER,DATA1,DATA2,....]
    vel_col=2
    coher_col =3
    
    f_input=open(SPRwf_file, 'r')
    f_output=open(SPRf_file, 'wb') 
    csv_input = csv.reader(f_input)
    csv_output = csv.writer(f_output)
    # Write the header
    csv_output.writerow(next(csv_input))
    
    for cols in csv_input:
        if float(cols[coher_col]) > labelcoherenceread and float(cols[vel_col]) < maxlosvelread and float(cols[vel_col]) > minlosvelread:  
            csv_output.writerow(cols)
    f_input.close()
    f_output.close()  
    
def creat_vel_layer(nameloadfile,filename):
    name=filename.split('/')
    last_name=name[-1] #last name = OK_PHA_RESIDUALS.csv
    
#    nameloadfile='SAR-PROZ'
#    if nameloadfile=='SAR-PROZ':
    velfile = filename.replace(last_name,"SPRvf.csv")
    VelFile="file:///"+velfile
    VelFlnm='LOSVEL-MAP'
    urivel = VelFile+"?delimiter=%s&xField=%s&yField=%s&crs=epsg:4326" % (",","LON","LAT")
    VelLayer = QgsVectorLayer(urivel, VelFlnm, "delimitedtext")
    VelLayer.isValid()
    QgsMapLayerRegistry.instance().addMapLayer(VelLayer)
        
    targetField = 'VEL'
    classes = 8
    mode = QgsGraduatedSymbolRendererV2.EqualInterval
    symbol = QgsSymbolV2.defaultSymbol(VelLayer.geometryType())
    colorRamp = QgsVectorGradientColorRampV2.create({'color1' : '255,0,0,255', 'color2' : '0,0,255,255', 'stops':'0.25;255,180,0,255:0.50;0,255,0,255:0.75;0,212,212,255'})
    renderer = QgsGraduatedSymbolRendererV2.createRenderer(VelLayer, targetField, classes, mode, symbol, colorRamp)
    VelLayer.setRendererV2(renderer)
        

def creat_rwt_heigh_csvfiles(nameloadfile,filename,form_values):
    
    name=filename.split('/')
    last_name=name[-1] #last name = OK_PHA_RESIDUALS.csv
    
#    nameloadfile='SAR-PROZ'
#	
#    if nameloadfile=='SAR-PROZ':
    SPR_file = filename.replace(last_name,"SPR.csv")
        #SPR_file =C:/Users/Pedro/Desktop/PROJ_FILES/00_SARPROZ/SPR.csv
        
    SPRwf_file = filename.replace(last_name,"SPRhwf.csv")
        #SPR_file =C:/Users/Pedro/Desktop/PROJ_FILES/00_SARPROZ/SPRwf.csv
        
    SPRf_file = filename.replace(last_name,"SPRhf.csv")
        #SPR_file =C:/Users/Pedro/Desktop/PROJ_FILES/00_SARPROZ/SPRwf.csv
        
        #latcol    = [3]
        #longcol   = [4]
        #velcol    = [8]
        #cohercol  = [11]
        
        #totalcol  = latcol+longcol+velcol+cohercol
                
    with open(SPR_file) as infile:  # Use 'with' to close files automatically
        reader = csv.reader(infile)
        headers = reader.next()  # Read first line
            # Figure out which columns have '-' in them (assume these are dates)
        date_columns = [col for col, header in enumerate(headers) if '-' in header]
            
        lat_col   = [col for col, header in enumerate(headers) if 'LAT' in header]
        long_col  = [col for col, header in enumerate(headers) if 'LON' in header]
        heigh_col   = [col for col, header in enumerate(headers) if 'HEIGHT' in header]
        coher_col = [col for col, header in enumerate(headers) if 'COHER' in header]
        heigh_col= [heigh_col[0]] # Read the first column with string HEIGHT 
            
        totalcol  = lat_col+long_col+heigh_col+coher_col
        all_columns = totalcol + date_columns

        with open(SPRwf_file,'w') as outfile:
            writer = csv.writer(outfile, delimiter=',', lineterminator='\n')
                # print headers
            writer.writerow([headers[i] for i in all_columns])
                # print data
            for row in reader:  # Read remaining data from our input CSV
                writer.writerow([row[i] for i in all_columns])
        
        infile.close()
        outfile.close()
        
    #[labelcoherenceread,maxlosvelread,minlosvelread,maxresheigread,minresheigread]
    
    maxresheigread     = form_values[3]  
    minresheigread     = form_values[4]
    labelcoherenceread = form_values[0]
    print maxresheigread 
    print minresheigread 
    
    # remotemix =[LAT,LONG,HEIGH,COHER,DATA1,DATA2,....]
    heig_col=2
    coher_col =3
    
    f_input=open(SPRwf_file, 'r')
    f_output=open(SPRf_file, 'wb') 
    csv_input = csv.reader(f_input)
    csv_output = csv.writer(f_output)
    # Write the header
    csv_output.writerow(next(csv_input))
    
    for cols in csv_input:
        #if float(cols[coher_col]) > labelcoherenceread and float(cols[heig_col]) < maxresheigread and float(cols[heig_col]) > minresheigread:  
        if float(cols[coher_col]) > labelcoherenceread: 
            csv_output.writerow(cols)
    f_input.close()
    f_output.close() 


def creat_heigh_layer(nameloadfile,filename):
    name=filename.split('/')
    last_name=name[-1] #last name = OK_PHA_RESIDUALS.csv

#    if nameloadfile=='SAR-PROZ':
    velfile = filename.replace(last_name,"SPRhf.csv")
    VelFile="file:///"+velfile
    VelFlnm='HEIGHT-MAP '
    urivel = VelFile+"?delimiter=%s&xField=%s&yField=%s&crs=epsg:4326" % (",","LON","LAT")
    VelLayer = QgsVectorLayer(urivel, VelFlnm, "delimitedtext")
    VelLayer.isValid()
    QgsMapLayerRegistry.instance().addMapLayer(VelLayer)
        
    targetField = 'HEIGHT'
    classes = 8
    mode = QgsGraduatedSymbolRendererV2.EqualInterval
    symbol = QgsSymbolV2.defaultSymbol(VelLayer.geometryType())
    colorRamp = QgsVectorGradientColorRampV2.create({'color1' : '16,50,13,255', 'color2' : '255,255,255,255', 'stops':'0.25;251,255,0,255:0.50;177,148,43,255:0.75;95,65,13,255'})
    renderer = QgsGraduatedSymbolRendererV2.createRenderer(VelLayer, targetField, classes, mode, symbol, colorRamp)
    VelLayer.setRendererV2(renderer)