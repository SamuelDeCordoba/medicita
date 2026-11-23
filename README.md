# Medicita: Pipeline CI/CD de pruebas unitarias

Proyecto de Ingeniería de Software III (Universidad EAM). Backend de **Medicita**, una aplicación de turnos digitales para la entrega de medicamentos en EPS. Este repositorio implementa las pruebas unitarias definidas en el **Plan de Pruebas** y un pipeline en **GitHub Actions** que las ejecuta en cada cambio.

**Equipo:** Camilo Andrés Mora Garzón, Luis Eduardo Fino Jaramillo, Samuel Córdoba Hernández, Mariana Martínez.

## 1. Qué se prueba (Plan de Pruebas, Parte 1)

| Módulo | Función | Regla de negocio |
|---|---|---|
| `src/turnos.py` | Generación del código de turno | 60 años o más: prefijo `P-` (prioritario). Menos de 60: prefijo `R-` (regular). Edad negativa o consecutivo menor a 1 lanza `ValueError`. |
| `src/validaciones.py` | Validación de fórmulas médicas | Solo JPG, PNG o PDF; máximo 10 MB. Lanza `InvalidFileExtensionException` o `FileTooLargeException`. |
| `src/tokens.py` | Tokens JWT de afiliados | Genera y decodifica JWT (HS256). Lanza `TokenExpiradoException` o `TokenInvalidoException`. |

**Criterios de aceptación:** 100 % de las pruebas en PASSED y cobertura mayor al 80 %. El pipeline hace cumplir la cobertura con `--cov-fail-under=80`.

## 2. Estructura del proyecto

```
Medicita/
├── .github/workflows/ci-cd.yml   # Definición del pipeline
├── src/
│   ├── turnos.py
│   ├── validaciones.py
│   └── tokens.py
├── tests/unit/
│   ├── test_turnos.py
│   ├── test_validaciones.py
│   └── test_tokens.py
├── requirements.txt
├── Dockerfile
└── README.md
```

## 3. Requisitos

- Git
- Python 3.11 o superior (el pipeline usa 3.11; también funciona con versiones más nuevas)
- Cuenta de GitHub (solo para ejecutar el pipeline en la nube)
- Docker (opcional, solo para construir la imagen en local)

## 4. Instalación y ejecución local

### Windows (PowerShell)

```powershell
git clone https://github.com/SamuelDeCordoba/medicita.git
cd medicita
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pytest tests/unit/ --cov=src --cov-fail-under=80 -v
```

Si PowerShell bloquea la activación del entorno virtual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
venv\Scripts\activate
```

### Linux / macOS

```bash
git clone https://github.com/SamuelDeCordoba/medicita.git
cd medicita
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest tests/unit/ --cov=src --cov-fail-under=80 -v
```

### Resultado esperado

16 pruebas en `PASSED` y una tabla de cobertura con `TOTAL 100%`, terminando con `Required test coverage of 80% reached`.

## 5. El pipeline (`.github/workflows/ci-cd.yml`)

Se activa con cada **push** a `main` o `develop` y con cada **pull request** hacia `main`. Tiene tres jobs encadenados con `needs`:

| Job | Qué hace | Cuándo corre |
|---|---|---|
| **Build & Test** | Checkout, Python 3.11, instala dependencias, ejecuta `pytest` con cobertura mínima del 80 % y guarda `coverage.xml` como artefacto. | Siempre |
| **Docker Build & Push** | Construye la imagen del `Dockerfile` y la publica en GitHub Container Registry. | Solo si Build & Test pasó y el evento es un push |
| **Deploy a Runtime** | Despliegue simulado (imprime imagen, ambiente y commit). | Solo si Docker pasó y la rama es `main` |

Las pruebas siempre se ejecutan antes de construir o desplegar. Si una prueba falla, o la cobertura baja del 80 %, los jobs siguientes se omiten.

### Parámetros configurables

| Parámetro | Dónde | Valor actual |
|---|---|---|
| Versión de Python | `env: PYTHON_VERSION` en `ci-cd.yml` | 3.11 |
| Umbral de cobertura | `--cov-fail-under=80` en el paso de pruebas | 80 |
| Ramas que disparan el pipeline | bloque `on:` | `main`, `develop` (PR hacia `main`) |
| Registro de imágenes | `env: REGISTRY` | `ghcr.io` |
| Dependencias | `requirements.txt` | pytest, pytest-cov, PyJWT |

No se necesitan *secrets*: la publicación de la imagen usa el `GITHUB_TOKEN` automático y el despliegue es simulado.

## 6. Ejecutar el pipeline en tu propia copia (fork)

1. Haz **Fork** del repositorio a tu cuenta de GitHub.
2. Entra a la pestaña **Actions** de tu fork y pulsa **"I understand my workflows, go ahead and enable them"** (GitHub desactiva los workflows en los forks por defecto).
3. Clona tu fork, trabaja en la rama `develop` y haz push:

```bash
git clone https://github.com/<TU_USUARIO>/medicita.git
cd medicita
git checkout develop
# ... realiza cambios ...
git add .
git commit -m "prueba del pipeline"
git push origin develop
```

4. En **Actions** verás la ejecución "Pipeline CI/CD Medicita".
5. Para ver el despliegue, abre un Pull Request de `develop` a `main` en tu fork y fusiónalo. La ejecución sobre `main` correrá los tres jobs.

## 7. Cómo provocar un fallo en las pruebas

1. Abre `tests/unit/test_turnos.py` y en `test_generar_turno_prioritario` cambia el valor esperado, por ejemplo `P-014` por `P-999`.
2. Comprueba el fallo en local:

```bash
pytest tests/unit/ --cov=src --cov-fail-under=80 -v
```

   Debe aparecer `FAILED` y terminar con código de salida 1.

3. Haz commit y push a `develop`.
4. En **Actions** el resultado esperado es:
   - **Build & Test:** en rojo (falló la prueba).
   - **Docker Build & Push:** omitido.
   - **Deploy a Runtime:** omitido.
5. Revierte el cambio (`git revert HEAD` o corrige la aserción) y vuelve a hacer push: el pipeline queda otra vez en verde.

Otra forma de fallar el pipeline: eliminar pruebas hasta que la cobertura baje del 80 %.

## 8. Construir la imagen Docker en local (opcional)

```bash
docker build -t medicita .
```

## 9. Resultados de referencia

- 16 pruebas unitarias en PASSED (4 de turnos, 5 de validaciones, 7 de tokens JWT).
- Cobertura total del 100 %.
- Tiempo de ejecución de la suite menor a 1 segundo (criterio del plan: menos de 2 s).
- Pipeline en verde sobre `main` (tres jobs).