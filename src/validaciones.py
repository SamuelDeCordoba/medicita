EXTENSIONES_PERMITIDAS = {"jpg", "jpeg", "png", "pdf"}
TAMANO_MAXIMO_BYTES = 10 * 1024 * 1024 


class InvalidFileExtensionException(Exception):
    pass


class FileTooLargeException(Exception):
    pass


def validar_formato_formula(nombre_archivo: str, tamano_bytes: int) -> bool:
    if "." not in nombre_archivo:
        raise InvalidFileExtensionException("El archivo no tiene extensión")

    extension = nombre_archivo.rsplit(".", 1)[1].lower()
    if extension not in EXTENSIONES_PERMITIDAS:
        raise InvalidFileExtensionException("Formato no admitido")

    if tamano_bytes > TAMANO_MAXIMO_BYTES:
        raise FileTooLargeException(
            "El archivo supera el tamaño máximo permitido de 10 MB"
        )
    return True