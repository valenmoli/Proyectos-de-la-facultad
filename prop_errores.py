'''PROPAGACION DE ERRORES'''

''' Area de un cilindro  '''
###      4pi^2.hr^3      ###
def area_cil(lst_1, lst_2):
    err=lst_2[0]
    
    altu=lst_1[0]
    diam=lst_1[1]
    
    cal = (2*(3.1415)*(diam/2))*((diam/2)+altu)
    
    prop_err = 2*(3.1415)*(diam*err + (1/2)*altu*err)
    
    res = ('({:.2f} +- {:.2f})'.format(cal, prop_err))
    
    return res

'''Volumen de un cilindro'''
###    vol = r^2.pi.h    ###
def volumen_cil(lst_1, lst_2):
    err=lst_2[0]
    
    altu=lst_1[0]
    diam=lst_1[1]
    
    cal = ((diam**2)/4)*(altu)*(3.1415)
    
    prop_err = (3.1415/2)*((diam*0.01)+(2*diam*0.07*altu))

    res = ('({:.2f} +- {:.2f})'.format(cal, prop_err))

    return res 

''' Area de una esfera  '''
###       4.pi.r^2      ###
def area_esf(lst_1, lst_2):
    err=lst_2[0]
    
    diam=lst_1[0]
    
    cal = (3.1415)*(diam**2)
    prop_err = (3.1415)*prop_errores('Pot', 2, err, [diam])
    
    res = ('({:.2f} +- {:.2f})'.format(cal, prop_err))
    
    return res

'''Volumen de una esfera'''
###  vol = (4/3).pi.r^3 ###
def volumen_esf(lst_1,lst_2):
    err=lst_2[0]
    
    diam=lst_1[0]
    
    cal = (4/3)*(3.1415)*((diam**3)/8)
    prop_err = (3.1415/6)*prop_errores('Pot', 3, err, [diam])
    
    res = ('({:.2f} +- {:.2f})'.format(cal, prop_err))
    
    return res

def prop_errores(tipo, n, err, med):
    if tipo=='Pot':
        res = n*med[0]**(n-1)*err
    
    return res

def medidas(dic):
    lst_regla=[]
    lst_micro=[]
    lst_calib=[]
    
    lst_err_regla=[]
    lst_err_micro=[]
    lst_err_calib=[]
    
    for i in dic.keys():
        if i=='Cilindro':
            for r in dic[i].keys():
                for j in dic[i][r].keys():
                    if r=='Regla':
                        lst_regla.append(dic[i][r][j][0])
                        lst_err_regla.append(dic[i][r][j][1])
                    elif r=='Micrometro':
                        lst_micro.append(dic[i][r][j][0])
                        lst_err_micro.append(dic[i][r][j][1])
                    elif r=='Calibre':
                        lst_calib.append(dic[i][r][j][0])
                        lst_err_calib.append(dic[i][r][j][1])
                        
            vol_regla=volumen_cil(lst_regla,lst_err_regla)
            vol_micro=volumen_cil(lst_micro,lst_err_micro)
            vol_calib=volumen_cil(lst_calib,lst_err_calib)
            
            area_regla=area_cil(lst_regla,lst_err_regla)
            area_micro=area_cil(lst_micro,lst_err_micro)
            area_calib=area_cil(lst_calib,lst_err_calib)
            
            print()
            print('|CILINDRO:')
            print('|Volumen Cil. Regla: {}mm^3'.format(vol_regla))
            print('|Volumen Cil. Micro: {}mm^3'.format(vol_micro))
            print('|Volumen Cil. Calib: {}mm^3'.format(vol_calib))
            print()
            print('|Area Cil. Regla: {}mm^2'.format(area_regla))
            print('|Area Cil. Micro: {}mm^2'.format(area_micro))
            print('|Area Cil. Calib: {}mm^2'.format(area_calib))
    
        elif i=='Esfera':
            for r in dic[i].keys():
                for j in dic[i][r].keys():
                    if r=='Regla':
                        lst_regla.append(dic[i][r][j][0])
                        lst_err_regla.append(dic[i][r][j][1])
                    elif r=='Micrometro':
                        lst_micro.append(dic[i][r][j][0])
                        lst_err_micro.append(dic[i][r][j][1])
                    elif r=='Calibre':
                        lst_calib.append(dic[i][r][j][0])
                        lst_err_calib.append(dic[i][r][j][1])
            
            vol_regla=volumen_esf(lst_regla,lst_err_regla)
            vol_micro=volumen_esf(lst_micro,lst_err_micro)
            vol_calib=volumen_esf(lst_calib,lst_err_calib)
            
            area_regla=area_esf(lst_regla,lst_err_regla)
            area_micro=area_esf(lst_micro,lst_err_micro)
            area_calib=area_esf(lst_calib,lst_err_calib)
            
            print()
            print('|ESFERA:')
            print('|Volumen Esf. Regla: {}mm^3'.format(vol_regla))
            print('|Volumen Esf. Micro: {}mm^3'.format(vol_micro))
            print('|Volumen Esf. Calib: {}mm^3'.format(vol_calib))
            print()
            print('|Area Esf. Regla: {}mm^2'.format(area_regla))
            print('|Area Esf. Micro: {}mm^2'.format(area_micro))
            print('|Area Esf. Calib: {}mm^2'.format(area_calib))

def main():
    dic_1={'Cilindro':{'Regla':{'Altura':[20,1],'Diametro':[7,1]},
                       'Micrometro':{'Altura':[20.00,0.01],'Diametro':[7.98,0.07]},
                       'Calibre':{'Altura':[20.01,0.02],'Diametro':[7.92,0.03]}}}
    
    dic_2={'Esfera':{'Regla':{'Diametro':[15,1]},
                     'Micrometro':{'Diametro':[15.01,0.04]},
                     'Calibre':{'Diametro':[15.05,0.03]},}}
    
    medidas(dic_1)
    medidas(dic_2)

main()