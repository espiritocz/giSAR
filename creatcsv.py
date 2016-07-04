def read_rwt_file(filename,self):
    # Atualiza a caixa
    self.dlg.lineEdit.setText(filename)
    # Abre o ficheiro
    upload_file = open (filename)
    x = upload_file.read()
    # Ler as primeiras strings 
    # Ficheiro SAR PROZ : Options for time series generation
    # Ficheiro STAMPS : ID,SVET, LVET
    strtype=x[0:6]
    
    if strtype == 'Option':
        self.dlg.filetype.setText('Loaded By: SAR-PROZ')
        # Nome da Layer
        nameloadfile ='SAR-PROZ'
        
        print 'Nome de ficheiro:',filename
        # Limpar o cabecalho do ficheiro  e criacao de novo
        new_filename = filename
        
        pos = x.find("ID,")
        xx  = x[pos:]
        arq = open (new_filename, 'w')
        arq.write (xx)
        upload_file.close ()
    else:
        self.dlg.filetype.setText('Loaded By: STAMPS')
        #Nome da Layer
        nameloadfile='StAMPs'
        new_filename=filename


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
    
#def update_rwt_form(layer,self):
    
    #idCOHER = list_id[0]
    #idHEIG  = list_id[1]
    #idRHEIG = list_id[2]
    #idVEL   = list_id[3]
#    idCOHER  = layer.fieldNameIndex('COHER')  # id da coluna ID
#    idHEIG   = layer.fieldNameIndex('HEIGHT')
#    idRHEIG  = layer.fieldNameIndex('SIGMA HEIGHT')
#    idVEL    = layer.fieldNameIndex('VEL')
#    
#    # Max and min values
#    maxheight    = layer.maximumValue (idHEIG) # Valor maximo dessa layer
#    minheight    = layer.minimumValue (idHEIG) # Valor minimo dessa layer
#    maxcoherence = layer.maximumValue (idCOHER) # Valor maximo dessa layer
#    mincoherence = layer.minimumValue (idCOHER) # Valor minimo dessa laye
#    maxresheig   = layer.maximumValue (idRHEIG) # Valor maximo dessa layer
#    minresheig   = layer.minimumValue (idRHEIG) # Valor minimo dessa laye
#    maxlosvel    = layer.maximumValue (idVEL) # Valor maximo dessa layer
#    minlosvel    = layer.minimumValue (idVEL) # Valor minimo dessa laye
#    
#    # convert to string
#    minheight= "%s" % minheight
#    maxheight= "%s" % maxheight
#    mincoherence= "%s" % mincoherence
#    maxcoherence= "%s" % maxcoherence
#    minresheig= "%s" % minresheig
#    maxresheig= "%s" % maxresheig
#    minlosvel= "%s" % minlosvel
#    maxlosvel= "%s" % maxlosvel
#    #minlosvel = '--'
#    self.dlg.minlosvel.setText(minlosvel)
#    #maxlosvel = '--'
#    self.dlg.maxlosvel.setText(maxlosvel)
#    #minheight = '23'
#    self.dlg.minheight.setText(minheight)
#    #maxheight = '23'
#    self.dlg.maxheight.setText(maxheight)
#    #mincoherence = '23'
#    self.dlg.mincoherence.setText(mincoherence)
#    #maxcoherence = '23'
#    self.dlg.maxcoherence.setText(maxcoherence)
#    mintemp = '--'
#    self.dlg.mintemp.setText(mintemp)
#    maxtemp = '--'
#    self.dlg.maxtemp.setText(maxtemp)
#    #minresheig = '--'
#    self.dlg.minresheig.setText(minresheig)
#    #maxresheig = '--'
#    self.dlg.maxresheig.setText(maxresheig)