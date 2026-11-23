from datetime import datetime, timedelta, timezone

import jwt

ALGORITMO = "HS256"


class TokenExpiradoException(Exception):
    """El token es válido pero ya expiró."""


class TokenInvalidoException(Exception):
    """El token está malformado o su firma no es válida."""


def generar_token(afiliado_id, secreto, minutos_expiracion=30, ahora=None):
    """Genera un JWT para un afiliado. 'ahora' permite simular fechas en las pruebas."""
    if not afiliado_id:
        raise ValueError("El id del afiliado es obligatorio")
    if not secreto:
        raise ValueError("El secreto es obligatorio")

    ahora = ahora or datetime.now(timezone.utc)
    payload = {
        "sub": str(afiliado_id),
        "iat": ahora,
        "exp": ahora + timedelta(minutes=minutos_expiracion),
    }
    return jwt.encode(payload, secreto, algorithm=ALGORITMO)


def decodificar_token(token, secreto):
    """Decodifica y valida un JWT. Devuelve el payload (diccionario)."""
    try:
        return jwt.decode(token, secreto, algorithms=[ALGORITMO])
    except jwt.ExpiredSignatureError as e:
        raise TokenExpiradoException("El token ha expirado") from e
    except jwt.InvalidTokenError as e:
        raise TokenInvalidoException("Token inválido") from e