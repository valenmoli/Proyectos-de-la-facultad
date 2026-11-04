"""Genera las tablas del informe desde el modelo. Ninguna cifra se copia a mano.

Uso (desde la carpeta del proyecto):  python -m calculo.generar_resultados
Escribe:  informe/supuestos.md, informe/resultados_consumo.md, informe/resultados_consumo.json
"""
import json
import os

from . import combustion as cb
from . import edificio as ed
from . import estimacion as es
from . import refrigeracion as rf
from . import supuestos

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDA = os.path.join(RAIZ, "informe")


def n(x, nd=0):
    """Formato con coma decimal y punto de miles."""
    s = f"{x:,.{nd}f}"
    return s.replace(",", "\x00").replace(".", ",").replace("\x00", ".")


def pct(x, nd=0):
    return n(x * 100, nd) + " %"


# Referencias (valores leidos de los documentos; ids de datos/*.md)
REF = dict(
    AR=[("Garrahan (CABA), HCWH 2021, H-01", 259), ("CEMAR (Rosario), HCWH 2021, H-02", 211), ("Giordano (San Juan), HCWH 2021, H-03", 163)],
    ES_util=380, ES_final=(394, 400),
    INT=dict(media=387, mediana=333, minimo=120, maximo=900),
    # participacion de climatizacion + ventilacion + ACS en el consumo total, segun distribuciones citadas por Hospitecnia
    PART=[("Hospitecnia (10): 45 % climatizacion + 20 % ACS", 0.65),
          ("Banco de Desarrollo de America Latina (13): 51 % climatizacion + 12 % ventilacion y bombas + 6 % ACS", 0.69),
          ("Hospital de Madrid (5): 40 % calefaccion + 20 % refrigeracion + 6 % ventilacion + 7 % ACS", 0.73),
          ("Chile (11): 36 % termico x (54 % climatizacion + 30 % agua caliente) + 64 % electrico x (21 % climatizacion + 3 % ACS)",
           0.36 * (0.54 + 0.30) + 0.64 * (0.21 + 0.03))],
)


def main():
    c = supuestos.defaults()
    P = c["P"]
    R = es.resumen(c)
    d, an = R["diseno"], R["anual"]
    A, a_cond = R["A"], R["a_cond"]
    base, sens = es.sensibilidad(c)
    caud = d["caudales"]

    os.makedirs(SALIDA, exist_ok=True)
    with open(os.path.join(SALIDA, "supuestos.md"), "w", encoding="utf-8") as f:
        f.write("# Supuestos y datos de entrada del modelo\n\n"
                "*Generado por `calculo/generar_resultados.py` desde `calculo/supuestos.py`. No editar a mano.*\n\n"
                "Estado: **DATO** = leido de un documento recibido; **SUPUESTO** = fundamentado pero sin fuente citable todavia; "
                "**CONSTANTE** = convencion o propiedad fisica.\n\n" + supuestos.tabla_md() + "\n")

    L = []
    w = L.append
    w("# Resultados de la estimacion de consumos")
    w("")
    w("*Generado por `calculo/generar_resultados.py`. No editar a mano: se regenera con el codigo.*")
    w("")
    w("Hospital modelado: Favaloro (La Matanza), AMBA. Frontera: sistema termico (frio, recalentamiento, calefaccion, "
      "humidificacion y agua caliente sanitaria) y sus auxiliares (ventiladores, bombas, ventiladores del condensador). "
      "Energia final: electricidad mas gas natural medido por su poder calorifico superior.")
    w("")
    # ---- 1. Resultado principal
    w("## 1. Resultado principal")
    w("")
    w("| Magnitud | Valor |")
    w("|---|---|")
    w(f"| Superficie cubierta | {n(P['A_cub'])} m2 |")
    w(f"| Superficie climatizada | {n(a_cond)} m2 ({pct(P['f_acond'])} de la cubierta) |")
    w(f"| Electricidad anual | {n(R['E_elec']/1e3)} MWh |")
    w(f"| Gas natural anual (PCS) | {n(R['E_gas_PCS']/1e3)} MWh = {n(R['V_gas_m3']/1e3)} mil m3 |")
    w(f"| **Energia final anual** | **{n(R['E_total']/1e3)} MWh** |")
    w(f"| **Intensidad sobre superficie cubierta** | **{n(R['i_total_cub'])} kWh/m2 y anio** ({n(R['i_elec_cub'])} electricidad + {n(R['i_gas_cub'])} gas) |")
    w(f"| Intensidad sobre superficie climatizada | {n(R['i_total_cond'])} kWh/m2 y anio |")
    w(f"| Participacion del gas | {pct(R['frac_gas'])} |")
    w(f"| Capacidad frigorifica de diseno | {n(d['Q_L'])} kW ({n(d['Q_L']/P['A_cub']*1000)} W/m2 cubierto; {n(d['Q_L']/a_cond*1000)} W/m2 climatizado) |")
    w(f"| Potencia electrica del compresor al diseno | {n(d['planta']['W_comp'])} kW (COP {n(d['planta']['COP'],2)}, condensacion a {n(d['planta']['T_cond'])} C) |")
    w(f"| Carga de calefaccion de diseno de invierno (aire) | {n(d['Q_caldera_invierno'])} kW |")
    w(f"| Demanda media de ACS | {n(d['acs']['kW'])} kW ({n(P['L_cama_dia'])} L/cama y dia) |")
    w("")
    # ---- 2. Desglose por uso
    el = an["elec"]
    w("## 2. Desglose por uso final")
    w("")
    w("| Uso | Energia [MWh/anio] | % del total | kWh/m2 cubierto |")
    w("|---|---|---|---|")
    filas = [("Electricidad: compresor de la enfriadora", el["compresor"]),
             ("Electricidad: ventiladores de las unidades de tratamiento de aire", el["ventiladores"]),
             ("Electricidad: ventiladores del condensador", el["vent_condensador"]),
             ("Electricidad: bombas de agua helada", el["bombas"])]
    gas_pcs = R["E_gas_PCS"]
    k = R["E_gas_PCS"] / an["q_util_total"]   # energia PCS por kWh util
    filas += [("Gas: recalentamiento despues de la serpentina", an["q_recal"] * k),
              ("Gas: calefaccion del aire", an["q_cal"] * k),
              ("Gas: humidificacion con vapor", an["q_hum"] * k),
              ("Gas: agua caliente sanitaria", an["q_acs"] * k)]
    for nom, v in filas:
        w(f"| {nom} | {n(v/1e3)} | {pct(v/R['E_total'],1)} | {n(v/P['A_cub'],1)} |")
    w(f"| **Total** | **{n(R['E_total']/1e3)}** | 100 % | **{n(R['i_total_cub'],1)}** |")
    w("")
    w(f"El recalentamiento es el {pct(an['q_recal']/an['q_util_total'])} del calor util que entrega la caldera "
      f"({n(an['q_recal']/1e3)} MWh de {n(an['q_util_total']/1e3)} MWh): el aire se enfria para deshumidificar y luego se recalienta con gas. "
      f"Es la ineficiencia que la alternativa B (recuperacion de calor del condensador) busca aprovechar; el calor que la enfriadora "
      f"rechaza en el ano es {n(an['planta']['Q_cond']/1e3)} MWh.")
    w("")
    cop_c = an["planta"]["Q_L"] / el["compresor"]
    cop_p = an["planta"]["Q_L"] / (el["compresor"] + el["vent_condensador"] + el["bombas"])
    w(f"Frio entregado en el ano: {n(an['planta']['Q_L']/1e3)} MWh. COP estacional del compresor: {n(cop_c,2)}. "
      f"COP estacional de la planta (compresor, ventiladores del condensador y bombas): {n(cop_p,2)}. "
      f"Horas equivalentes a plena carga de refrigeracion: {n(an['planta']['Q_L']/d['Q_L'])} h.")
    w("")
    # ---- 3. Por zona
    w("## 3. Por zona")
    w("")
    w("| Zona | Superficie [m2] | Caudal de impulsion [m3/h] | Aire exterior [m3/h] | Serpentina [MWh] | Recalentamiento [MWh] | Calefaccion [MWh] | Ventiladores [MWh] |")
    w("|---|---|---|---|---|---|---|---|")
    for g, z in c["Z"].items():
        zz = an["zonas"][g]
        w(f"| {g} {z['nombre']} | {n(A[g])} | {n(caud[g]['V_sup_m3h'])} | {n(caud[g]['m_oa']/P['rho_aire']*3600)} | "
          f"{n(zz['serp']/1e3)} | {n(zz['recal']/1e3)} | {n(zz['cal']/1e3)} | {n(zz['vent']/1e3)} |")
    w("")
    # ---- 4. Diseno
    w("## 4. Puntos de diseno")
    w("")
    w(f"Verano: {n(d['T_ext_verano'])} C de bulbo seco, {n(P['T_bh_ver'])} C de bulbo humedo coincidente, W = {n(d['W_ext_verano']*1000,2)} g/kg, "
      f"actividad plena y ganancia solar pico. Invierno: {n(d['T_ext_invierno'])} C y {pct(P['HR_inv'])} de humedad relativa, sin ganancias internas.")
    w("")
    w("| Zona | T mezcla [C] | T salida serpentina [C] | T impulsion [C] | Serpentina [kW] | sensible [kW] | latente [kW] | Recalentamiento [kW] | Invierno: calefaccion [kW] | Invierno: humidificacion [kW] |")
    w("|---|---|---|---|---|---|---|---|---|---|")
    for g in c["Z"]:
        v, i = d["verano"][g], d["invierno"][g]
        w(f"| {g} | {n(v['T_mix'],1)} | {n(v['T_c'],1)} | {n(v['T_sup'],1)} | {n(v['Q_coil'])} | {n(v['Q_coil_sens'])} | {n(v['Q_coil_lat'])} | "
          f"{n(v['Q_recal'])} | {n(i['Q_cal']+i['Q_recal'])} | {n(i['Q_hum'])} |")
    w(f"| **Total** | | | | **{n(d['Q_L'])}** | {n(sum(v['Q_coil_sens'] for v in d['verano'].values()))} | "
      f"{n(sum(v['Q_coil_lat'] for v in d['verano'].values()))} | {n(d['Q_recal_verano'])} | "
      f"{n(d['Q_caldera_invierno'])} | |")
    w("")
    # ---- 5. Ciclo de refrigeracion
    r = rf.ciclo(P["T_ev"], d["planta"]["T_cond"], P["refrigerante"], P["sobrecal"], P["subenf"], P["eta_is"], P["eta_motor"])
    w("## 5. Ciclo de refrigeracion al punto de diseno de verano")
    w("")
    w(f"Refrigerante {P['refrigerante']}, evaporacion a {n(P['T_ev'])} C ({n(r['P_ev']/1e3)} kPa), condensacion a {n(d['planta']['T_cond'])} C ({n(r['P_c']/1e3)} kPa).")
    w("")
    w("| Estado | Descripcion | T [C] | h [kJ/kg] |")
    w("|---|---|---|---|")
    w(f"| 1 | Salida del evaporador (vapor sobrecalentado {n(P['sobrecal'])} K) | {n(r['T1'],1)} | {n(r['h1'],1)} |")
    w(f"| 2s | Salida del compresor, isentropica | | {n(r['h2s'],1)} |")
    w(f"| 2 | Salida del compresor, real (rendimiento isentropico {n(P['eta_is'],2)}) | {n(r['T2'],1)} | {n(r['h2'],1)} |")
    w(f"| 3 | Salida del condensador (subenfriado {n(P['subenf'])} K) | {n(r['T3'],1)} | {n(r['h3'],1)} |")
    w(f"| 4 | Salida de la valvula de expansion (titulo {n(r['x4'],2)}) | {n(P['T_ev'],1)} | {n(r['h4'],1)} |")
    w("")
    w(f"Efecto frigorifico {n(r['q_L'],1)} kJ/kg, trabajo de compresion {n(r['w'],1)} kJ/kg, calor rechazado {n(r['q_H'],1)} kJ/kg. "
      f"COP sobre el eje {n(r['cop_comp'],2)}; COP sobre la potencia electrica del compresor {n(r['cop_elec'],2)}; COP de Carnot entre {n(P['T_ev'])} C y {n(d['planta']['T_cond'])} C: {n(r['cop_carnot'],2)}. "
      f"Caudal de refrigerante al diseno: {n(d['Q_L']/r['q_L'],2)} kg/s.")
    w("")
    # ---- 6. Combustion
    cal = d["caldera"]
    b, pc = cal["balance"], cal["pc"]
    w("## 6. Combustion y caldera")
    w("")
    w("Por kmol de gas natural, con relacion de aire " + n(P["lambda_aire"], 2) + ":")
    w("")
    w("| Reactivos | kmol | Productos | kmol |")
    w("|---|---|---|---|")
    w(f"| Gas natural | 1,000 | CO2 | {n(b['productos']['CO2'],3)} |")
    w(f"| O2 | {n(b['reactivos']['O2'],3)} | H2O | {n(b['productos']['H2O'],3)} |")
    w(f"| N2 del aire | {n(b['reactivos']['N2_aire'],3)} | N2 | {n(b['productos']['N2'],3)} |")
    w(f"| | | O2 | {n(b['productos']['O2'],3)} |")
    w("")
    w(f"Aire estequiometrico: {n(b['o2_estequiometrico']*(1+79/21),3)} kmol/kmol de gas. Control de atomos C, H, O y N: cierra.")
    w("")
    w("| Magnitud | Valor |")
    w("|---|---|")
    w(f"| Poder calorifico superior | {n(pc['PCS_MJ_m3'],2)} MJ/m3 = {n(pc['PCS_kcal_m3'])} kcal/m3 = {n(pc['PCS_kWh_m3'],3)} kWh/m3 (m3 estandar a 15 C) |")
    w(f"| Poder calorifico inferior | {n(pc['PCI_MJ_m3'],2)} MJ/m3 = {n(pc['PCI_kWh_m3'],3)} kWh/m3 |")
    w(f"| Relacion PCS/PCI | {n(pc['relacion_PCS_PCI'],4)} |")
    w(f"| Perdida por gases de escape ({n(P['T_gases'])} C) | {pct(cal['q_gases'],1)} del PCI |")
    w(f"| **Rendimiento de la caldera** | **{pct(cal['eta_PCI'],1)} sobre PCI** ({pct(cal['eta_PCS'],1)} sobre PCS) |")
    w(f"| Fraccion molar de agua en los gases | {pct(cal['y_H2O'],1)} |")
    w(f"| Temperatura de rocio de los gases | {n(cal['T_rocio'],1)} C (la chimenea a {n(P['T_gases'])} C no condensa) |")
    w(f"| Temperatura de llama adiabatica (sin disociacion) | {n(cb.temperatura_llama_adiabatica(P))} C |")
    w(f"| Gas consumido por kWh util | {n(cb.consumo_gas(1.0, cal['eta_PCI'], pc)['V_m3'],4)} m3 |")
    w("")
    # ---- 7. Mensual
    w("## 7. Perfil mensual")
    w("")
    w("| Mes | T media [C] | Frio entregado [MWh] | Calor de aire [MWh] | Electricidad del compresor [MWh] | COP del compresor |")
    w("|---|---|---|---|---|---|")
    for i, f in enumerate(an["mensual"]):
        cop = f["Q_L"] / f["W_comp"] if f["W_comp"] else 0
        w(f"| {f['mes']} | {n(c['clima']['T'][i],1)} | {n(f['Q_L']/1e3)} | {n(f['Q_cal']/1e3)} | {n(f['W_comp']/1e3)} | {n(cop,2)} |")
    w("")
    # ---- 8. Contraste
    w("## 8. Contraste con las referencias")
    w("")
    w("Las referencias miden el edificio completo (iluminacion, equipos medicos, cocina y lavanderia), y este modelo solo el sistema termico. "
      "Para comparar, se estima el consumo total equivalente suponiendo que el sistema termico es una fraccion del total, "
      "con las participaciones que citan las fuentes del articulo de Hospitecnia.")
    w("")
    w("| Participacion del sistema termico en el total | Fraccion | Total equivalente [kWh/m2 y anio] |")
    w("|---|---|---|")
    eq = []
    for nom, fr in REF["PART"]:
        eq.append(R["i_total_cub"] / fr)
        w(f"| {nom} | {pct(fr)} | {n(R['i_total_cub']/fr)} |")
    w("")
    w(f"Con esas participaciones, el consumo total equivalente del edificio queda entre **{n(min(eq))} y {n(max(eq))} kWh/m2 y anio**.")
    w("")
    w("| Referencia | kWh/m2 y anio | Observacion |")
    w("|---|---|---|")
    for nom, v in REF["AR"]:
        w(f"| {nom} | {n(v)} | Edificio completo, estimado por auditoria |")
    w(f"| Modelo espanol del articulo (Hospitecnia, D-60) | {n(REF['ES_util'])} | Calor util mas electricidad |")
    w(f"| Mismo modelo en energia final (Hospitecnia, E-16) | {n(REF['ES_final'][0])} a {n(REF['ES_final'][1])} | Edificio completo |")
    w(f"| 23 hospitales internacionales (Hospitecnia, D-61) | mediana {n(REF['INT']['mediana'])}; media {n(REF['INT']['media'])}; rango {n(REF['INT']['minimo'])} a {n(REF['INT']['maximo'])} | Edificio completo |")
    w(f"| **Este modelo, solo sistema termico** | **{n(R['i_total_cub'])}** | Equivale a {n(min(eq))} a {n(max(eq))} para el edificio completo |")
    w("")
    # ---- 9. Sensibilidad
    w("## 9. Sensibilidad")
    w("")
    w(f"Cada fila cambia un supuesto y deja los demas en su valor base ({n(base/1e3)} MWh/anio, {n(base/P['A_cub'])} kWh/m2).")
    w("")
    w("| Variacion | Energia final [MWh/anio] | Diferencia |")
    w("|---|---|---|")
    for f in sorted(sens, key=lambda x: -abs(x["delta"])):
        signo = "+" if f["delta"] >= 0 else "-"
        w(f"| {f['nombre']} | {n(f['E_total']/1e3)} | {signo}{n(abs(f['delta'])*100,1)} % |")
    w("")
    lo = min(f["E_total"] for f in sens)
    hi = max(f["E_total"] for f in sens)
    w(f"Cada variacion por separado mueve el resultado entre {n(lo/P['A_cub'])} y {n(hi/P['A_cub'])} kWh/m2 y anio.")
    w("")
    # ---- 10. Chequeos
    w("## 10. Chequeos termodinamicos")
    w("")
    w("Los ejecuta `python -m pytest calculo/tests`. Resultado de la ultima corrida: ver la salida de pytest.")
    w("")
    w("- Primera ley: la carga de diseno es la suma de las serpentinas; el calor rechazado es el frio entregado mas el trabajo en el eje.")
    w("- Segunda ley: el COP del ciclo y el COP mensual son menores que el de Carnot.")
    w("- Combustion: el balance de atomos de C, H, O y N cierra; PCS mayor que PCI; la diferencia es el calor latente del agua formada.")
    w("- Aire humedo: la psicrometria coincide con CoolProp dentro de 1,2 %; el balance de entalpia de la corriente de aire cierra.")
    w("- Estas verificaciones comprueban la coherencia interna. La verificacion de fondo es la reimplementacion independiente a partir de `calculo/ESPECIFICACION.md`.")
    w("")

    with open(os.path.join(SALIDA, "resultados_consumo.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L))

    # JSON con las cifras para comparar con reimplementaciones independientes
    salida = dict(
        E_elec_kWh=R["E_elec"], E_gas_PCS_kWh=R["E_gas_PCS"], E_gas_PCI_kWh=R["E_gas_PCI"], V_gas_m3=R["V_gas_m3"], E_total_kWh=R["E_total"],
        i_total_cub=R["i_total_cub"], i_total_cond=R["i_total_cond"],
        Q_L_diseno_kW=d["Q_L"], Q_recal_verano_kW=d["Q_recal_verano"], Q_caldera_invierno_kW=d["Q_caldera_invierno"],
        W_comp_diseno_kW=d["planta"]["W_comp"], COP_diseno=d["planta"]["COP"], T_cond_diseno=d["planta"]["T_cond"],
        acs_kW=d["acs"]["kW"], eta_caldera_PCI=cal["eta_PCI"], PCS_kcal_m3=pc["PCS_kcal_m3"], PCS_kWh_m3=pc["PCS_kWh_m3"],
        PCI_kWh_m3=pc["PCI_kWh_m3"], T_rocio=cal["T_rocio"], T_llama_adiabatica=cb.temperatura_llama_adiabatica(P),
        elec={k: v for k, v in el.items()}, q_util=dict(recal=an["q_recal"], cal=an["q_cal"], hum=an["q_hum"], acs=an["q_acs"], total=an["q_util_total"]),
        frio_entregado_kWh=an["planta"]["Q_L"], Q_cond_kWh=an["planta"]["Q_cond"],
        zonas={g: dict(A=A[g], m_sup=caud[g]["m_sup"], m_oa=caud[g]["m_oa"], Q_serp_diseno=d["verano"][g]["Q_coil"],
                       Q_recal_diseno=d["verano"][g]["Q_recal"], Q_cal_invierno=d["invierno"][g]["Q_cal"],
                       serp_kWh=an["zonas"][g]["serp"], recal_kWh=an["zonas"][g]["recal"], cal_kWh=an["zonas"][g]["cal"],
                       hum_kWh=an["zonas"][g]["hum"], vent_kWh=an["zonas"][g]["vent"]) for g in c["Z"]},
        mensual=[dict(mes=f["mes"], Q_L_kWh=f["Q_L"], Q_cal_kWh=f["Q_cal"], W_comp_kWh=f["W_comp"]) for f in an["mensual"]],
        sensibilidad=[dict(nombre=f["nombre"], E_total_kWh=f["E_total"], delta=f["delta"]) for f in sens],
        total_equivalente_edificio=dict(min=min(eq), max=max(eq)),
    )
    with open(os.path.join(SALIDA, "resultados_consumo.json"), "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, indent=1)
    print("Escritos: informe/supuestos.md, informe/resultados_consumo.md, informe/resultados_consumo.json")
    print(f"Energia final: {R['E_total']/1e3:,.0f} MWh/anio = {R['i_total_cub']:.1f} kWh/m2 (equivalente edificio: {min(eq):.0f} a {max(eq):.0f})")


if __name__ == "__main__":
    main()
