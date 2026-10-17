from datetime import date


def generar_turno(edad: int, consecutivo: int) -> dict:
    if edad < 0 or consecutivo < 1:
        raise ValueError("Edad o consecutivo inválido")

    if edad >= 60:
        return {"codigo": f"P-{consecutivo:03d}", "prioridad": "alta"}
    return {"codigo": f"R-{consecutivo:03d}", "prioridad": "normal"}