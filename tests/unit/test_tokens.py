from datetime import datetime, timedelta, timezone

import pytest

from src.tokens import (
    TokenExpiradoException,
    TokenInvalidoException,
    decodificar_token,
    generar_token,
)

SECRETO = "secreto-de-pruebas-medicita-1234567890"


def test_decodificar_token_valido():
    token = generar_token("afiliado-42", SECRETO)
    payload = decodificar_token(token, SECRETO)
    assert payload["sub"] == "afiliado-42"


def test_token_expirado():
    hace_una_hora = datetime.now(timezone.utc) - timedelta(hours=1)
    token = generar_token("afiliado-42", SECRETO, minutos_expiracion=30, ahora=hace_una_hora)
    with pytest.raises(TokenExpiradoException):
        decodificar_token(token, SECRETO)


def test_token_con_firma_invalida():
    token = generar_token("afiliado-42", SECRETO)
    with pytest.raises(TokenInvalidoException):
        decodificar_token(token, "otro-secreto-distinto-1234567890-abc")


def test_token_malformado():
    with pytest.raises(TokenInvalidoException):
        decodificar_token("esto.no.es-un-jwt", SECRETO)


def test_token_vacio():
    with pytest.raises(TokenInvalidoException):
        decodificar_token("", SECRETO)


def test_generar_token_sin_afiliado():
    with pytest.raises(ValueError):
        generar_token("", SECRETO)


def test_generar_token_sin_secreto():
    with pytest.raises(ValueError):
        generar_token("afiliado-42", "")