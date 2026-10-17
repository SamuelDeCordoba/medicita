import pytest
from src.turnos import generar_turno


def test_generar_turno_prioritario():
    turno = generar_turno(edad=70, consecutivo=14)
    assert turno["codigo"] == "P-999"
    assert turno["prioridad"] == "alta"


def test_generar_turno_regular():
    turno = generar_turno(edad=30, consecutivo=85)
    assert turno["codigo"] == "R-085"
    assert turno["prioridad"] == "normal"


def test_limite_edad_60_es_prioritario():
    assert generar_turno(60, 1)["codigo"].startswith("P-")
    assert generar_turno(59, 1)["codigo"].startswith("R-")


def test_entrada_invalida():
    with pytest.raises(ValueError):
        generar_turno(-1, 1)
    with pytest.raises(ValueError):
        generar_turno(30, 0)