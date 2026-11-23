"""Las cifras que el informe imprime en sus ecuaciones deben poder repetirse a mano con los numeros impresos."""
import re

import pytest

from calculo import construir_borrador as cbm
from calculo import construir_documentos as cd
from calculo import informe_extra as ie
from calculo import supuestos


def _f(s):
    """'1.234,5' -> 1234.5"""
    return float(s.replace(".", "").replace(",", "."))


@pytest.fixture(scope="module")
def datos():
    c = supuestos.defaults()
    V, T = cbm.valores()
    V, T = cd.valores_nuevos(V, T)
    V.update(ie.valores_informe(c, V, T))
    T.update(ie.tablas_informe(c, V, T))
    return c, V, T


def test_serpentina_a_mano(datos):
    c, V, T = datos
    m, hC, hD = _f(V["inf_m"]), _f(V["inf_hC"]), _f(V["inf_hD"])
    wC, wD, hf = _f(V["inf_wC"]), _f(V["inf_wD"]), _f(V["inf_hf"])
    q = m * ((hC - hD) - (wC - wD) * hf)
    assert q == pytest.approx(_f(V["Q_serp_G1"]), abs=0.15)


def test_latente_a_mano(datos):
    c, V, T = datos
    q = _f(V["inf_m"]) * _f(V["inf_dw"]) * 2501.0
    assert q == pytest.approx(_f(V["Q_lat_G1"]), abs=0.15)
    assert _f(V["Q_sens_G1"]) + _f(V["Q_lat_G1"]) == pytest.approx(_f(V["Q_serp_G1"]), abs=0.15)


def test_ciclo_a_mano(datos):
    c, V, T = datos
    qL, w, eta = _f(V["inf_qL"]), _f(V["inf_w"]), _f(V["eta_motor"])
    cop = qL / (w / eta)
    assert cop == pytest.approx(_f(V["inf_COP"]), abs=0.002)
    W = _f(V["Q_L_dis"]) / _f(V["inf_COP"])
    assert W == pytest.approx(_f(V["inf_W"]), abs=1.0)
    assert _f(V["Q_L_dis"]) + eta * _f(V["inf_W"]) == pytest.approx(_f(V["inf_Qc"]), abs=1.5)


def test_caldera_a_mano(datos):
    c, V, T = datos
    eta = 1 - _f(V["q_gases"]) / 100 - _f(V["f_rad"]) / 100
    assert eta == pytest.approx(_f(V["eta_PCI"]) / 100, abs=0.0006)
    assert _f(V["q_total_MWh"]) / _f(V["inf_etaPCS"]) == pytest.approx(_f(V["E_gas_MWh"]), abs=1.5)


def test_necesidades_cierran(datos):
    c, V, T = datos
    assert _f(V["inf_sens"]) + _f(V["inf_lat"]) == pytest.approx(_f(V["Q_L_dis"]), abs=1.5)


def test_tablas_sin_marcadores_ni_vacios(datos):
    c, V, T = datos
    for k in ("tabla_temas_inf", "tabla_datos_inf", "tabla_zonas_inf", "tabla_nec_inf", "tabla_ab_inf", "tabla_mejoras_inf"):
        assert T[k].count("|") > 20, k
        assert "{{" not in T[k] and "None" not in T[k], k


def test_a_contra_b_coherente(datos):
    c, V, T = datos
    assert _f(V["inf_E_B"]) < _f(V["E_total_MWh"])
    assert (1 - _f(V["inf_E_B"]) / _f(V["E_total_MWh"])) * 100 == pytest.approx(_f(V["dE_B"]), abs=0.1)
    assert _f(V["inf_Qcond_B"]) < _f(V["Q_cond_MWh"])
