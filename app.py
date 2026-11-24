"""Interfaz web de RSA LAB. Ejecutar: streamlit run app.py."""
import streamlit as st
from rsa import encriptar, desencriptar


st.set_page_config(page_title="RSA LAB | Matemática Discreta", page_icon="🔐", layout="wide")


def limpiar(modo):
    st.session_state.pop(f"resultado_{modo}", None)
    st.session_state.pop(f"error_{modo}", None)


def transferir():
    datos = st.session_state.get("resultado_enc")
    if datos is None:
        return
    limpiar("dec")
    for clave in ("p", "q", "e", "C", "L"):
        st.session_state[f"dec_{clave}"] = str(datos[clave])
    st.session_state["modo"] = "Desencriptar"
    st.session_state["transferido"] = True


def formulario(modo):
    with st.form(f"formulario_{modo}"):
        columnas = st.columns(3)
        valores = (("p", "367"), ("q", "373"), ("e", "17"))
        parametros = {}
        for columna, (clave, valor) in zip(columnas, valores):
            with columna:
                etiqueta = f"{clave} · " + ("Primo" if clave != "e" else "Exponente público")
                parametros[clave] = st.text_input(etiqueta, value=valor, key=f"{modo}_{clave}", max_chars=12)
        if modo == "enc":
            mensaje = st.text_area("Mensaje original · ASCII imprimible (32–126)", value="RSA", key="enc_mensaje", max_chars=2000)
            st.caption("Se conservan los espacios. No se admiten tildes, ñ, saltos de línea ni emojis.")
        else:
            cifrado = st.text_area("Cifrado C · Bloques de seis dígitos", value="026054 123875", key="dec_C", max_chars=6999)
            longitud = st.text_input("Longitud original L", value="3", key="dec_L", max_chars=6)
            st.caption("Separa los bloques por un solo espacio; conserva los ceros iniciales.")
        ejecutar = st.form_submit_button("Encriptar mensaje" if modo == "enc" else "Desencriptar mensaje", type="primary")
    if ejecutar:
        limpiar(modo)
        try:
            # Límites de trabajo para una aplicación pública. La lógica RSA original se conserva.
            p, q, e = (parametros[k] for k in ("p", "q", "e"))
            for nombre, valor in parametros.items():
                if len(valor) > 12 or (valor.lstrip("-").isascii() and valor.lstrip("-").isdigit() and abs(int(valor)) > 10**9):
                    raise ValueError(f"{nombre} excede el límite de esta demostración (1 000 000 000).")
            if modo == "enc":
                if len(mensaje) > 2000:
                    raise ValueError("El mensaje admite hasta 2000 caracteres.")
                datos = encriptar(mensaje, p, q, e)
            else:
                if len(cifrado) > 6999:
                    raise ValueError("Se admiten hasta 1000 bloques cifrados.")
                datos = desencriptar(cifrado, longitud, p, q, e)
            st.session_state[f"resultado_{modo}"] = datos
        except ValueError as exc:
            st.session_state[f"error_{modo}"] = str(exc)
    if error := st.session_state.get(f"error_{modo}"):
        st.error(error)


def resultados(modo):
    datos = st.session_state.get(f"resultado_{modo}")
    if datos is None:
        st.info("Completa los datos y pulsa el botón para consultar el procedimiento.")
        return
    st.subheader("Resultados y procedimiento matemático")
    st.caption("Corresponden al último cálculo exitoso; pulsa el botón de nuevo si cambias los datos.")
    columnas = st.columns(3)
    columnas[0].metric("n = p × q", str(datos["n"]))
    columnas[1].metric("φ(n) = (p − 1)(q − 1)", str(datos["phi"]))
    columnas[2].metric("Longitud original L", str(datos["L"]))
    st.write(f"MCD(e, φ) = {datos['mcd']}")
    if modo == "enc":
        st.write(f"Llave pública (e, n): ({datos['e']}, {datos['n']})")
        st.write("Relleno: " + ("sí, un espacio adicional." if datos["relleno"] else "no."))
        st.markdown("**Cifrado C**")
        st.code(datos["C"], language=None)
        st.latex(r"c = m^e \bmod n")
        st.button("Enviar cifrado a desencriptar →", on_click=transferir)
    else:
        st.write(f"Llave privada (d, n): ({datos['d']}, {datos['n']})")
        st.write(f"Comprobación: (e × d) mod φ = {(datos['e'] * datos['d']) % datos['phi']}")
        st.write("Relleno: " + ("se retiró exactamente un espacio adicional." if datos["relleno"] else "no se retiró ninguno."))
        st.markdown("**Mensaje recuperado**")
        st.code(datos["mensaje"], language=None)
        st.caption(f"Representación con espacios visibles: {datos['mensaje']!r}")
        st.latex(r"d = e^{-1} \bmod \varphi(n), \qquad m = c^d \bmod n")
    filas = [{"#": i, "Pareja": repr(f["pareja"]), "ASCII (3+3)": f["ascii"], "Bloque m": f"{f['m']:06d}", "Bloque c": f["cifrado"]} for i, f in enumerate(datos["filas"], 1)]
    st.dataframe(filas, hide_index=True, width="stretch")


st.caption("RSA / LABORATORIO DE CRIPTOGRAFÍA")
st.title("Matemática discreta")
st.write("Hecho por Raúl Godínez y María Marroquín")
st.caption("Versión web · No requiere cuenta ni contraseña para utilizarla.")
modo = "enc" if st.radio("Operación", ("Encriptar", "Desencriptar"), horizontal=True, key="modo") == "Encriptar" else "dec"
if st.session_state.pop("transferido", False):
    st.success("Cifrado recibido. Presiona Desencriptar mensaje para recuperar el texto original.")
formulario(modo)
st.divider()
resultados(modo)
with st.expander("Cómo funciona y ejemplo"):
    st.markdown("Cada pareja de caracteres se convierte en un bloque ASCII de seis dígitos. Si la longitud es impar, se añade un espacio temporal; al recuperar el mensaje se elimina solo ese espacio.\n\n**Ejemplo:** p = 367, q = 373, e = 17; mensaje `RSA`; C = `026054 123875`; L = 3; d = 8009.\n\n**Condiciones:** primos distintos, 126126 < n < 1000000, e > 1 y MCD(e, φ) = 1. Los algoritmos de primalidad, Euclides, inverso y potencia modular son los del proyecto original.")
st.caption("Aplicación educativa. Este RSA por bloques pequeños no debe usarse para proteger información real.")
