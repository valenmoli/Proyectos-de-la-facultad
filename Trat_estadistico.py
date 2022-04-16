def valor_medio(lst):
    r=0
    for i in lst:
        r+=i

    res=r/len(lst)

    return res

def desv_estandar(val_med, lst):
    r=0
    for i in lst:
        r+=(i-val_med)**2
    
    j=r/(len(lst)-1)
    res=j**(1/2)
    
    return res

def desv_estandar_prom(des_est, lst):
    res = des_est/(len(lst)**(1/2))
    
    return res

def error_absoluto(des_prm, ap_nom):
    res = ((des_prm)**2+(ap_nom)**2)**(1/2)
    
    return res

def error_relativo(err_abs, val_med):
    res = err_abs/val_med
    
    return res

def error_porcentual(err_rel):
    res = err_rel*100
    
    return res

def trat_estadistico(lst, ap_nom, medida, dic):
    val_med = valor_medio(lst)
       
    if dic['Ap. Nom'][0]==1:  
        val_med= int('{:.0f}'.format(val_med))
    elif dic['Ap. Nom'][0]==0.01 or dic['Ap. Nom'][0]==0.02:  
        val_med= float('{:.2f}'.format(val_med))
                
    des_est = desv_estandar(val_med, lst)
    des_prm = desv_estandar_prom(des_est, lst)
    err_abs = error_absoluto(des_prm, ap_nom)
    err_rel = error_relativo(err_abs, val_med)
    err_prc = error_porcentual(err_rel)
    
    print('|'+medida+':')
    print('|Valor medio:      {:.2f}'.format(val_med))
    print('|Desv. Estandar:   {:.4f}'.format(des_est))
    print('|Desv. Est. Prom:  {:.4f}'.format(des_prm))
    print('|Error Absoluto:   {:.4f}'.format(err_abs))
    print('|Error Relativo:   {:.4f}'.format(err_rel))
    print('|Error Rel. Porc.: {:.2f}%'.format(err_prc))
    print()

def procesar(dic):
    lst_diam=[]
    lst_altu=[]
    
    for i in dic.keys():       
        for r in dic[i]:           
            if i == 'Diametro':
                lst_diam.append(r)             
            elif i=='Altura':
                lst_altu.append(r)
       
    print('Instrumento: '+dic['Instrumento'][0])
    print()
    trat_estadistico(lst_diam, dic['Ap. Nom'][0], 'Diametro', dic)
    trat_estadistico(lst_altu, dic['Ap. Nom'][0], 'Altura', dic)
    
def main():
    dic_1={'Diametro':[7,7,8,8,7,8,7,7,7,8],
           'Altura':[19,19,20,20,20,19,20,21,19,20],
           'Ap. Nom': [1], 'Instrumento': ['Regla'], 'Objeto':['Cilindro']}
    
    dic_2={'Diametro':[7.88,7.89,7.88,7.88,8.39,8.38,7.88,7.88,7.86,7.87],
           'Altura':[20.01,20.02,20.01,20.01,20.00,19.95,20.01,20.02,20.01,20.00],
           'Ap. Nom': [0.01], 'Instrumento': ['Micrometro'], 'Objeto':['Cilindro']}
    
    dic_3={'Diametro':[7.86,7.90,7.92,7.86,8.00,8.00,7.98,7.92,7.88,7.86],
           'Altura':[20.02,20.00,20.00,20.00,20.00,20.02,20.00,20.02,20.00,20.02],
           'Ap. Nom': [0.02], 'Instrumento': ['Calibre'], 'Objeto':['Cilindro']}
    
    print('Objeto: '+dic_1['Objeto'][0])
    procesar(dic_1)
    procesar(dic_2)
    procesar(dic_3)
    
main()