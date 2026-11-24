# RSA LAB — Grupo 5 · Versión web

Matemática Discreta I · Raúl Godínez y María Marroquín

## Cambio solicitado

Se añadió una interfaz web en `app.py` para reemplazar la necesidad de ejecutar
Tkinter al revisar el trabajo. Conserva los módulos originales `rsa.py` y
`algoritmos.py`, sus validaciones, los bloques ASCII de seis dígitos, las llaves,
el procedimiento matemático, los espacios originales y el relleno.
`main.py` sigue siendo la versión de escritorio original.

**Estado:** código preparado para publicar. Este ZIP por sí solo no genera
un enlace público ni sustituye el despliegue. Sigue `PUBLICAR.md`.

## Ejecución local (solo para desarrollar)

Desde esta carpeta, con Python 3.11:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m streamlit run app.py
```

Abre la URL local que indique Streamlit. El profesor no necesitará estos pasos
cuando la aplicación esté publicada.

## Uso

1. Selecciona Encriptar; introduce p, q, e y el mensaje; pulsa Encriptar mensaje.
2. Consulta el cifrado C, la longitud L y la tabla.
3. Pulsa Enviar cifrado a desencriptar. Se copian los datos y cambia la operación;
   no se descifra automáticamente.
4. Pulsa Desencriptar mensaje para ver d, la comprobación y el mensaje recuperado.

Los formularios calculan al pulsar el botón. Si editas una entrada, vuelve a
calcular. Un intento inválido elimina el resultado anterior de esa operación.
Cada visitante usa su propia sesión; los mensajes no se guardan en archivos.

## Restricciones conservadas

- Primos p y q distintos; 126126 < p × q < 1000000.
- e > 1, coprimo con φ(n).
- ASCII imprimible 32–126; no se aceptan tildes, ñ ni saltos de línea.
- Parejas de caracteres; un espacio temporal si L es impar.
- Bloques cifrados de seis dígitos separados por un solo espacio.
- Algoritmos matemáticos implementados manualmente, sin bibliotecas criptográficas.

La interfaz pública limita el mensaje a 2000 caracteres y el cifrado a 1000
bloques; p, q y e admiten hasta 1 000 000 000 para acotar el trabajo de cálculo.
Es una demostración educativa, no un sistema para proteger información real.

## Ejemplo de comprobación

Mensaje `RSA`; p = 367; q = 373; e = 17.

- n = 136891; φ(n) = 136152.
- C = `026054 123875`; L = 3.
- d = 8009; mensaje recuperado `RSA`.

## Archivos y pruebas

- `app.py`: interfaz web, estado por sesión y límites de uso.
- `rsa.py`, `algoritmos.py`: lógica original sin modificaciones.
- `main.py`: interfaz original de escritorio, opcional.
- `test_rsa.py`: 12 pruebas originales (las de escritorio requieren Tkinter).
- `test_web.py`: pruebas de transferencia, errores, recuperación y sesiones.
- `.streamlit/config.toml`: tema y configuración web.
- `requirements.txt`: versión de Streamlit verificada.
- `PUBLICAR.md`: pasos para obtener y revisar el enlace público.

```powershell
.venv\Scripts\python -m unittest test_rsa test_web -v
```

En un servidor sin Tkinter se puede ejecutar solamente `test_web`; la
aplicación web no importa `main.py` ni utiliza Tkinter.
