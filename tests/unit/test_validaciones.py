import pytest
from src.validaciones import (
    validar_formato_formula,
    InvalidFileExtensionException,
    FileTooLargeException,
    TAMANO_MAXIMO_BYTES,
)


def test_validar_formato_formula_valido():
    assert validar_formato_formula("formula.pdf", 1024) is True
    assert validar_formato_formula("foto.JPG", 2048) is True


def test_validar_formato_formula_invalido():
    with pytest.raises(InvalidFileExtensionException):
        validar_formato_formula("virus.exe", 1024)
    with pytest.raises(InvalidFileExtensionException):
        validar_formato_formula("archivo.zip", 1024)


def test_archivo_sin_extension():
    with pytest.raises(InvalidFileExtensionException):
        validar_formato_formula("formula", 1024)


def test_archivo_supera_10mb():
    with pytest.raises(FileTooLargeException):
        validar_formato_formula("formula.pdf", TAMANO_MAXIMO_BYTES + 1)


def test_archivo_exactamente_10mb_es_valido():
    assert validar_formato_formula("formula.png", TAMANO_MAXIMO_BYTES) is True