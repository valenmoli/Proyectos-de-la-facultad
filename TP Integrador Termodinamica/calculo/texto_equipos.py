"""Redaccion de la seccion de equipos y ubicacion (informe y memoria) desde calculo/equipos.py."""
from . import equipos as eq
from . import mejoras as mj
from .construir_borrador import n, tabla


def redactar(c, V, T):
    r = eq.resumen_equipos(c)
    en, ca, ut, hi, sh, az, ni, cop, mz = (r["enfriadoras"], r["calderas"], r["utas"], r["hidraulica"], r["shafts"], r["azotea"],
                                          r["niveles"], r["cop"], r["matriz"])
    pz = ut["por_zona"]
    pt = r["planta"]
    v = {
        "enf_unidad": n(en["cap_unidad"]), "enf_serv": n(en["cap_servicio"]), "enf_req": n(en["req_unidad"], 1), "enf_falta": n(en["faltante_kW"], 1),
        "enf_falta_pct": n(abs(en["margen_rel"]) * 100, 1), "enf_carga_rel": n(en["carga_relativa_unidad"] * 100, 1),
        "enf_pot": n(en["pot_unidad"], 1), "enf_fam_min": n(r["p"]["cap_fam_min"]), "enf_fam_max": n(r["p"]["cap_fam_max"]),
        "enf_bombas": n(en["calor_bombas_max_kW"], 1), "enf_Q_bombas": n(en["Q_L"] + en["calor_bombas_max_kW"]),
        "enf_n_total": n(en["n_total"]), "enf_n_serv": n(en["n_serv"]), "enf_n_res": n(en["n_res"]), "enf_QL": n(en["Q_L"], 1),
        "enf_cap_parada": n(en["cap_una_parada"]), "enf_margen_kW": n(en["margen_una_parada_kW"], 1), "enf_margen_pct": n(en["margen_una_parada_rel"] * 100),
        "enf_margen_bombas": n(en["margen_con_bombas_kW"], 1),
        "enf_2m1_cap": n(en["alt_2mas1"]["cap_servicio"]), "enf_2m1_falta": n(en["alt_2mas1"]["faltante_kW"], 1),
        "enf_2m1_pct": n(en["alt_2mas1"]["faltante_rel"] * 100, 1), "enf_2m1_req": n(en["alt_2mas1"]["req_unidad_redondeada"]),
        "enf_ramal_m3h": n(hi["ramal_enfriadora"]["V_m3h"]),
        "cop_cat": n(cop["cop_catalogo"], 2), "cop_mod34": n(cop["cop_modelo_34"], 2), "cop_mod35": n(cop["cop_modelo_35"], 2),
        "cal_diseno": n(ca["Q_diseno"]), "cal_inv": n(ca["Q_invierno"]), "cal_vapor": n(ca["Q_vapor"]), "cal_acs_punta": n(ca["Q_acs_punta"]),
        "cal_sin_vapor": n(ca["Q_agua_caliente_sin_vapor"]), "cal_cond_cap": n(ca["opcion_b"]["cap_unidad"]), "cal_cond_n": n(ca["opcion_b"]["n"]),
        "cal_cond_serv": n(ca["opcion_b"]["n_servicio"]), "cal_cond_una_parada": n(ca["opcion_b"]["cap_una_parada"]),
        "cal_cond_carga": n(ca["opcion_b"]["carga_relativa_servicio"] * 100), "cal_dn": n(ca["DN_chimenea"]),
        "cal_gas_m3h": n(ca["V_gas_m3h"], 1), "cal_ahorro_cond": n(ca["ahorro_gas_max"] * 100, 1),
        "uta_n": n(ut["n_total"]), "uta_cub": n(ut["n_cubierta"]), "uta_crit": n(ut["n_criticas"]),
        "uta_G1": n(pz["G1"]["caudal_unidad"]), "uta_G2": n(pz["G2"]["caudal_unidad"]), "uta_G3": n(pz["G3"]["caudal_unidad"]),
        "uta_G4": n(pz["G4"]["caudal_unidad"]), "uta_G5": n(pz["G5"]["caudal_unidad"]), "uta_V": n(ut["V_total"]),
        "hid_m3h": n(hi["principal"]["V_m3h"]), "hid_DN": n(hi["principal"]["DN"]), "hid_v": n(hi["principal"]["v_real"], 2),
        "hid_DN_ram": n(hi["ramal_enfriadora"]["DN"]), "hid_v_ram": n(hi["ramal_enfriadora"]["v_real"], 2),
        "hid_Dcalc": n(hi["principal"]["D_calc_mm"]),
        "sh_vert": n(sh["A_vertical_total"], 1), "sh_n": n(sh["n_shafts_agrupados"]), "sh_n_area": n(sh["n_shafts_por_area"]),
        "az_n": n(az["n_unidades"]), "az_A": n(az["A_total"]), "az_pct": n(az["fraccion_cubierta"] * 100, 1), "az_q": n(az["q_kN_m2"], 2), "az_ref": n(az["q_ref"], 1),
        "az_rel": n(az["q_sobre_ref"], 2), "az_peso": n(r["p"]["peso_op_t"]), "az_cub": n(az["A_cubierta"]),
        "mz_azotea": n(mz["base"]["azotea"], 2), "mz_patio": n(mz["base"]["patio"], 2),
        "mz_iguales": n(mz["pesos_iguales"]["azotea"], 2), "mz_x2_azotea": n(mz["estructura_e_izaje_x2"]["azotea"], 2),
        "mz_x2_patio": n(mz["estructura_e_izaje_x2"]["patio"], 2),
        "pt_W": n(pt["W"], 1), "pt_H": n(pt["H"], 1), "pt_nuc_w": n(pt["nucleo"]["ancho"], 1), "pt_nuc_d": n(pt["nucleo"]["prof"], 1),
        "pt_nuc_A": n(pt["nucleo"]["area"]), "sh_brutos": n(pt["nucleo"]["area_shafts"]), "sh_netos": n(pt["nucleo"]["area_vertical_neta"], 1),
        "niv_bruta": n(ni["bruta_nivel"]), "niv_clim": n(ni["clim_nivel"]), "niv_no_clim": n(ni["bruta_nivel"] - ni["clim_nivel"]),
        "fv_area": n(mj.parametro("kWp_fv") * 5.0), "solar_area": n(mj.parametro("A_solar")),
    }
    v["_cumple_enf"] = (f"{v['enf_n_serv']} + {v['enf_n_res']} enfriadoras Carrier 30XA 1002: {v['enf_cap_parada']} kW con una parada, "
                        f"{v['enf_margen_pct']} % sobre la carga")
    V.update(v)

    # ------------------------------------------------------------------ informe
    tabla_eq = tabla(["Equipo", "Qué elegimos", "Por qué", "Respaldo"], [
        ("Enfriadoras", f"{v['enf_n_total']} unidades iguales de tornillo condensadas por aire ({v['enf_n_serv']} en servicio y {v['enf_n_res']} de reserva). Ejemplo: Carrier AquaForce 30XA 1002, R-134a, {v['enf_unidad']} kW nominales",
         f"Cada unidad en servicio debe dar al menos {v['enf_req']} kW (un tercio de {n(en['Q_L'])} kW); la reserva mantiene el servicio si una falla", "Cita (catálogo, búsqueda web) y propio"),
        ("Calderas", f"2 calderas de agua caliente a gas de {v['cal_diseno']} kW cada una (100 % cada una). Ejemplo de condensación: {v['cal_cond_n']} Viessmann Vitocrossal 300 CM3C de {v['cal_cond_cap']} kW",
         f"Carga de diseño {v['cal_diseno']} kW = {v['cal_inv']} kW de invierno + {v['cal_acs_punta']} kW de punta de ACS (el doble de la media, supuesto)", "Cita (catálogo) y propio"),
        ("Unidades de tratamiento de aire", f"{v['uta_n']} unidades: una por quirófano (6 × {v['uta_G1']} m³/h, con filtro HEPA), una para terapia intensiva ({v['uta_G2']} m³/h) y {v['uta_cub']} en cubierta para las demás zonas (hasta 25.000 m³/h cada una)",
         "Las críticas junto a su zona (continuidad, presiones y recorridos cortos); las demás en cubierta, cerca de las enfriadoras", "Propio"),
        ("Cañería de agua helada", f"Principal DN {v['hid_DN']} ({v['hid_m3h']} m³/h a {v['hid_v']} m/s) y ramal por enfriadora DN {v['hid_DN_ram']}",
         "Caudal de la carga con salto de 5 K y velocidad de diseño de 2 m/s", "Propio"),
        ("Shafts de aire", f"{v['sh_n']} shafts de unos 2 m² ({v['sh_vert']} m² verticales en total), apilados en un núcleo técnico",
         "Áreas con 6 m/s en impulsión y 5 m/s en retorno", "Propio"),
    ], (13, 38, 33, 16))
    inf = f"""## 4.1 Qué elegimos

{tabla_eq}

Table: Tabla 6. Equipos elegidos. Los datos de catálogo son **citas de búsquedas web** (no pudimos abrir los catálogos): hay que cotejarlos con el fabricante.

**La enfriadora de ejemplo cumple, pero con un margen grande.** La Carrier 30XA 1002 da {v['enf_unidad']} kW nominales con {v['enf_pot']} kW de compresores a 35 °C de aire y agua 12/7 °C (la familia va de {v['enf_fam_min']} a {v['enf_fam_max']} kW). Con {v['enf_n_serv']} unidades en servicio y 1 de reserva quedan **{v['enf_cap_parada']} kW con una unidad parada contra {v['enf_QL']} kW de carga (+{v['enf_margen_pct']} %)**, y cada unidad en servicio trabaja al {v['enf_carga_rel']} % de su capacidad. **Por qué 3+1 y no 2+1:** con 2+1 y la misma unidad quedan {v['enf_2m1_cap']} kW y **faltan {v['enf_2m1_falta']} kW ({v['enf_2m1_pct']} %)**, así que no cumple; la alternativa más ajustada sería 2+1 con una unidad de al menos {v['enf_2m1_req']} kW (la 30XA 1102, cuya designación y capacidad **no verificamos**). Elegimos 3+1 porque es la única configuración con datos de catálogo que podemos citar, y lo decimos: queda sobredimensionada. El margen cubre el calor de las bombas ({v['enf_bombas']} kW, que la carga no incluye) y la diferencia entre los 34 °C del diseño y los 35 °C del catálogo. **Calderas:** la carga de diseño incluye {v['cal_vapor']} kW de vapor de humidificación, que una caldera de agua caliente **no produce** (hacen falta humidificadores o un generador de vapor); la dejamos completa, del lado seguro. Con la caldera de condensación de ejemplo hacen falta {v['cal_cond_serv']} unidades en servicio más 1 de reserva: con una parada quedan {v['cal_cond_una_parada']} kW, suficiente; con 3 unidades en total (una parada) quedan {n(ca['opcion_b']['cap_3_unidades_una_parada'])} kW y no alcanza.

## 4.2 Dónde ponerlos

Como ingenieros civiles, la ubicación depende del aire, el ruido, la estructura, el izaje, las cañerías y el mantenimiento. Armamos un esquema con tres niveles iguales de {v['niv_bruta']} m² brutos ({v['niv_clim']} climatizados y {v['niv_no_clim']} de locales técnicos, morgue y depósitos) y ubicamos las zonas según la presentación del hospital (figura 3) y, para ver cómo quedan en planta, las dibujamos a escala (figura 4).

**Cómo leer la planta.** El núcleo técnico ({v['pt_nuc_A']} m², de {v['pt_nuc_w']} × {v['pt_nuc_d']} m) ocupa la esquina sudeste, del lado de la calle y **en el mismo lugar en cada nivel**: los shafts se apilan, el agua helada baja por ellos desde la azotea y las enfriadoras se izan desde la calle. En el 2.º piso quirófanos y terapia intensiva quedan **contiguos al núcleo**, donde están sus {v['uta_crit']} UTAs (conductos cortos); la internación (G3) va en dos alas, y la guardia y los consultorios, en el 1.er piso con acceso desde la calle. Los pasillos están dentro de la superficie de cada zona. Es un esquema para razonar la ubicación, no un plano del hospital.

- **Enfriadoras en la azotea**, junto al núcleo técnico: necesitan aire libre (en un patio rodeado por el edificio recirculan el aire caliente) y el ruido queda por encima del 3.er piso, separado de la internación por una losa. Son {v['az_n']} unidades (3 en servicio y 1 de reserva) que ocupan {v['az_A']} m², el {v['az_pct']} % de la cubierta de {v['az_cub']} m². Las tomas de aire exterior de las UTAs de cubierta deben quedar lejos de las descargas de extracción y de la chimenea: la distancia mínima la fija la norma y **no la fijamos acá**.
- **Carga estructural.** Con un peso supuesto de {v['az_peso']} t por unidad, la carga media sobre su huella es de {v['az_q']} kN/m², {v['az_rel']} veces una sobrecarga de referencia de azotea de {v['az_ref']} kN/m² (**supuesta**; recordamos un rango de 1 a 5 kN/m² según el uso en el CIRSOC 101, sin haberlo consultado). La carga bajo los apoyos es mayor: hace falta plataforma o vigas y la verificación del calculista; el peso de {v['az_peso']} t es supuesto: hay que cambiarlo por el del catálogo.
- **UTAs y shafts.** Las {v['uta_crit']} críticas (quirófanos y terapia) van en el cuarto técnico del 2.º piso, junto a su zona; las {v['uta_cub']} restantes, en cubierta. Los {v['uta_V']} m³/h de impulsión necesitan {v['sh_vert']} m² netos de shafts verticales; con shafts de unos 2 m² agrupados por zona resultan {v['sh_n']} ({v['sh_brutos']} m²), dentro del núcleo técnico que se apila en los tres niveles (por área pura saldrían {v['sh_n_area']}).
- **Calderas en un anexo a nivel de calle**: acceso, medidor y regulador de gas, ventilación y chimenea (DN {v['cal_dn']}) por fuera del edificio. **Izaje:** unidades de 14 m y 12 t a unos 15 m de altura exigen grúa móvil grande y corte de calle; es el costo de la azotea.

**La decisión no es robusta.** Puntuamos azotea y patio a nivel con seis criterios: gana la azotea ({v['mz_azotea']} contra {v['mz_patio']}), pero con pesos iguales empatan y si estructura e izaje valen el doble gana el patio ({v['mz_x2_patio']} contra {v['mz_x2_azotea']}). Elegimos la azotea por el aire libre y los recorridos cortos hacia las {v['uta_cub']} UTAs de cubierta; si el calculista descarta la losa, el patio es la alternativa. Las reservas para solar térmico ({v['solar_area']} m²) y fotovoltaica (unos {v['fv_area']} m²) caben, pero **no dimensionamos las UTAs ni la sala de calderas**.

![Figura 3. Corte esquemático con zonas, superficies y equipos, y planta de cubierta con las enfriadoras. Las zonas siguen la presentación del hospital; la distribución en niveles y la planta de cubierta son supuestos nuestros, sin planos.](../figuras/fig08_plano_zonas.png){{width=12.5cm}}

![Figura 4. Planta tipo a escala del 1.er y 2.º piso (rectángulo equivalente de {v['pt_W']} × {v['pt_H']} m): la superficie dibujada de cada zona es proporcional a sus m² del modelo; la distribución en franjas, la calle al sur y el núcleo técnico en la esquina sudeste son supuestos nuestros.](../figuras/fig11_planta_tipo.png){{width=13cm}}
"""

    # ------------------------------------------------------------------ memoria
    filas_uta = [(u["id"], u["zona"], n(u["caudal_m3h"]), u["ubicacion"], "sí" if u["hepa"] else "no") for u in ut["lista"]]
    t_uta = tabla(["Unidad", "Zona", "Caudal [m³/h]", "Ubicación", "HEPA"], filas_uta, (14, 8, 14, 50, 8))
    filas_sh = []
    for g in ("G1", "G2", "G3", "G4", "G5"):
        s = sh["por_zona"][g]
        filas_sh.append((g, n(s["V_sup"]), n(s["A_imp"], 2), n(s["A_ret"], 2), n(s["A_vertical"], 2), n(s["n_shafts"]), s["modo"]))
    filas_sh.append(("Total", n(sh["por_zona"]["G1"]["V_sup"] + sum(sh["por_zona"][g]["V_sup"] for g in ("G2", "G3", "G4", "G5"))), n(sh["A_imp_total"], 2),
                     n(sh["A_ret_total"], 2), n(sh["A_vertical_total"], 2), n(sh["n_shafts_agrupados"]), ""))
    t_sh = tabla(["Zona", "Impulsión [m³/h]", "A impulsión [m²]", "A retorno [m²]", "Shaft vertical [m²]", "Shafts", "Modo"], filas_sh, (7, 12, 12, 11, 12, 7, 39))
    filas_mz = [(m[1], n(m[2] * 100) + " %", str(m[3]), str(m[4]), m[5]) for m in eq.MATRIZ_UBICACION]
    t_mz = tabla(["Criterio", "Peso", "Azotea (1 a 5)", "Patio (1 a 5)", "Razón"], filas_mz, (20, 7, 9, 9, 55))
    t_sup = eq.tabla_supuestos_md()
    mem = f"""## 9.1 Enfriadoras

Carga de diseño $\\dot Q_L$ = {n(en['Q_L'], 1)} kW. Con {v['enf_n_serv']} unidades en servicio cada una debe dar $\\dot Q_L/{v['enf_n_serv']}$ = {v['enf_req']} kW. La Carrier AquaForce 30XA 1002 da {v['enf_unidad']} kW nominales a 35 °C de aire exterior y agua 12/7 °C, con {v['enf_pot']} kW de compresores (cita; no se abrió el catálogo). Con una unidad parada quedan $3 \\cdot {v['enf_unidad']}$ = {v['enf_cap_parada']} kW: margen +{v['enf_margen_kW']} kW (+{v['enf_margen_pct']} %), con cada unidad en servicio al {v['enf_carga_rel']} % de su capacidad nominal. Con el calor de las bombas ({v['enf_bombas']} kW, que la carga no incluye) la carga sería {v['enf_Q_bombas']} kW y todavía sobran {v['enf_margen_bombas']} kW. La configuración 2+1 con la misma unidad da {v['enf_2m1_cap']} kW y no cumple (faltan {v['enf_2m1_falta']} kW, {v['enf_2m1_pct']} %); necesitaría una unidad de al menos {v['enf_2m1_req']} kW, que no verificamos.

{cop['texto']}

## 9.2 Calderas

Carga de diseño $= {v['cal_inv']} + {v['cal_acs_punta']}$ = {v['cal_diseno']} kW (calefacción y humidificación de invierno más la punta de ACS, el doble de la media por supuesto). El vapor de humidificación son {v['cal_vapor']} kW; sin él, el agua caliente necesita {v['cal_sin_vapor']} kW. Chimenea: gases de {n(ca['V_gases_m3h'])} m³/h a 190 °C con 8 m/s dan un diámetro de {n(ca['D_chimenea'] * 1000)} mm, es decir DN {v['cal_dn']}. Condensación como cota superior: 98 % sobre PCS (catálogo, cita) contra {n(ca['eta_PCS_modelo'] * 100, 1)} % del modelo, hasta {v['cal_ahorro_cond']} % menos de gas, solo si el retorno baja del punto de rocío de {n(ca['T_rocio_gases'], 1)} °C.

## 9.3 Unidades de tratamiento de aire

{t_uta}

Table: Tabla M11. Unidades de tratamiento de aire (criterio: una por quirófano y hasta 25.000 m³/h por unidad en las demás zonas).

## 9.4 Hidráulica y conductos

Caudal de agua helada $\\dot m_w = \\dot Q_L/(c_p \\Delta T)$ = {n(hi['m_w'], 1)} kg/s ({v['hid_m3h']} m³/h). Diámetro para 2,0 m/s: $D = \\sqrt{{4\\dot V/(\\pi v)}}$ = {v['hid_Dcalc']} mm, por lo que DN {v['hid_DN']} con una velocidad real de {v['hid_v']} m/s; el ramal por enfriadora (un tercio del caudal, {v['enf_ramal_m3h']} m³/h), DN {v['hid_DN_ram']} ({v['hid_v_ram']} m/s); si una unidad trabajara a su capacidad nominal el caudal sería mayor y convendría DN 200.

{t_sh}

Table: Tabla M12. Shafts de aire (impulsión a 6 m/s y retorno a 5 m/s; para las zonas con la UTA en su nivel el shaft vertical lleva solo aire exterior y extracción).

## 9.5 Azotea y ubicación

Huella de 14 × 3,5 = 49 m² por unidad, {v['az_n']} unidades ({v['az_A']} m² en total, {v['az_pct']} % de la cubierta). Carga media $q = 12 \\cdot 9{{,}}81 / 49$ = {v['az_q']} kN/m² contra {v['az_ref']} kN/m² de referencia (supuesta; rango recordado de 1 a 5 kN/m², sin consultar la norma).

{t_mz}

Table: Tabla M13. Matriz de decisión entre azotea y patio a nivel. Puntaje ponderado: azotea {v['mz_azotea']}, patio {v['mz_patio']}; con pesos iguales {v['mz_iguales']} en ambos; con estructura e izaje al doble, azotea {v['mz_x2_azotea']} y patio {v['mz_x2_patio']}.

## 9.6 Supuestos de la selección de equipos

::: {{custom-style="Largo"}}
{t_sup}

Table: Tabla M14. Supuestos nuevos de la selección y ubicación de equipos, con su estado.
:::
"""
    return inf, mem, v
