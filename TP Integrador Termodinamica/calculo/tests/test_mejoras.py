"""Chequeos de la alternativa B y de las mejoras (calculo/mejoras.py)."""
import copy

import pytest

from calculo import estimacion as es
from calculo import mejoras as mj
from calculo import supuestos

C = supuestos.defaults()
BASE = mj.anual_variante(C, {})


def test_sin_opciones_es_el_caso_base():
    """Con las opciones vacias, el calculo con variantes da lo mismo que el calculo anual original."""
    r = es.resumen(C)
    assert BASE["E_total"] == pytest.approx(r["E_total"], rel=1e-12)
    assert BASE["E_elec"] == pytest.approx(r["E_elec"], rel=1e-12)
    assert BASE["E_PCS"] == pytest.approx(r["E_gas_PCS"], rel=1e-12)


def test_alternativa_b_ahorra_gas_y_gasta_mas_electricidad():
    b = mj.anual_variante(C, {"rec_cond": True})
    assert b["E_PCS"] < BASE["E_PCS"]
    assert b["elec"]["compresor"] > BASE["elec"]["compresor"]       # condensar mas caliente cuesta trabajo
    assert b["E_total"] < BASE["E_total"]
    assert 0 < b["q_rec_cond"] <= BASE["q_recal"] + BASE["q_cal"] + 1e-6  # no se recupera mas calor del que se demanda


def test_alternativa_b_no_supera_el_calor_rechazado():
    b = mj.anual_variante(C, {"rec_cond": True})
    assert b["q_rec_cond"] < es.anual(C)["planta"]["Q_cond"]


def test_menos_coincidencia_menos_ahorro():
    a = mj.anual_variante(C, {"rec_cond": {"f": 0.5}})["E_total"]
    b = mj.anual_variante(C, {"rec_cond": {"f": 1.0}})["E_total"]
    assert BASE["E_total"] > a > b


def test_condensacion_rinde_mas_que_la_caldera_base():
    cd = mj.caldera_condensacion(C["P"], 45.0)
    base = es.cb.caldera(C["P"])
    assert cd["eta_PCI"] > base["eta_PCI"]
    assert cd["eta_PCS"] < 1.0                                     # nunca supera el 100 % sobre PCS (primera ley)
    assert 0 < cd["frac_cond"] < 1
    # sin condensacion (gases por encima del rocio) coincide con el rendimiento base
    sin = mj.caldera_condensacion(C["P"], C["P"]["T_gases"])
    assert sin["eta_PCI"] == pytest.approx(base["eta_PCI"], abs=1e-9)


def test_menos_temperatura_de_gases_mas_rendimiento():
    assert mj.caldera_condensacion(C["P"], 35.0)["eta_PCI"] > mj.caldera_condensacion(C["P"], 50.0)["eta_PCI"]


def test_irradiacion_mensual_suma_la_irradiacion_anual():
    H, Kt = mj.irradiacion_mensual(-34.7, 1700.0)
    dias = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    assert sum(h * d for h, d in zip(H, dias)) == pytest.approx(1700.0, rel=1e-9)
    assert 0.3 < Kt < 0.75
    assert H[0] > H[5] and H[11] > H[6]                            # mas sol en verano que en invierno (hemisferio sur)


def test_solar_no_supera_la_demanda_de_acs():
    r = mj.anual_variante(C, {"solar_acs": True})
    assert 0 < r["solar_kWh"] < r["q_acs"]
    assert r["E_PCS"] < BASE["E_PCS"]


def test_fotovoltaica_descuenta_electricidad():
    r = mj.anual_variante(C, {"fv": True})
    assert r["E_elec"] == pytest.approx(BASE["E_elec"] - r["fv_kWh"])
    assert r["fv_kWh"] == pytest.approx(mj.parametro("kWp_fv") * mj.parametro("GHI_anual") * mj.parametro("PR_fv"))


def test_recuperador_de_extraccion_nunca_empeora_con_bypass():
    r = mj.anual_variante(C, {"rec_extraccion": True})
    assert r["E_total"] <= BASE["E_total"] + 1e-6
    sin_penal = mj.anual_variante(C, {"rec_extraccion": True, "dp_rec": 0.0})
    assert sin_penal["E_total"] <= r["E_total"] + 1e-6


def test_menos_presion_de_ventiladores_ahorra_menos_que_su_electricidad():
    """El calor del ventilador que ya no se disipa hay que reponerlo con gas: el ahorro neto es menor que el de la electricidad."""
    r = mj.anual_variante(C, {"dp_vent": 0.8})
    ahorro_vent = BASE["elec"]["ventiladores"] - r["elec"]["ventiladores"]
    assert 0 < BASE["E_total"] - r["E_total"] < ahorro_vent


def test_factor_de_co2_del_gas_coincide_con_el_valor_de_referencia():
    """56,1 kg de CO2 por GJ de PCI es el valor por defecto del IPCC para el gas natural (recordado)."""
    f_gj = mj.factor_co2_gas(C["P"]) * 1000.0 / 3.6 / 1000.0 * 1000.0   # kg/kWh -> kg/GJ
    assert f_gj == pytest.approx(56.1, rel=0.03)


def test_el_paquete_ahorra_mas_que_cualquier_medida_sola():
    base, filas = mj.comparar(C)
    d = {f["clave"]: f["d_E"] for f in filas}
    assert d["P"] < min(d[k] for k in ("B", "M1", "M2", "M3", "M4", "M5"))
    assert d["P"] > -1.0                                            # no se puede ahorrar mas del 100 %


def test_mismos_refrigerantes_mismo_ciclo_ideal():
    out = mj.refrigerantes(C)
    r134 = [o for o in out if o["refrigerante"] == "R134a"][0]
    assert r134["cop_elec"] == pytest.approx(es.resumen(C)["diseno"]["planta"]["W_comp"] and 3.5567, rel=1e-3)
    ze = [o for o in out if o["refrigerante"] == "R1234ze(E)"]
    assert ze and ze[0]["q_vol"] < r134["q_vol"]                    # menos capacidad volumetrica: compresor mas grande


def test_los_parametros_nuevos_tienen_estado():
    for fila in mj.PARAMETROS:
        assert fila[5] in ("DATO", "SUPUESTO", "FUENTE SECUNDARIA", "PROPIO")
        assert len(fila[6]) > 10
