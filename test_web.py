"""Pruebas de la interfaz web sin navegador ni servidor externo."""
from pathlib import Path
import unittest
from streamlit.testing.v1 import AppTest


class PruebasWeb(unittest.TestCase):
    def setUp(self):
        self.app = AppTest.from_file(str(Path(__file__).with_name("app.py")), default_timeout=30).run()
        self.assertFalse(self.app.exception)

    def cifrar(self):
        self.app.button[0].click().run()
        self.assertFalse(self.app.exception)
        self.assertEqual(self.app.session_state["resultado_enc"]["C"], "026054 123875")

    def test_transferencia_y_recuperacion(self):
        self.cifrar()
        self.app.button[1].click().run()
        self.assertEqual(self.app.radio[0].value, "Desencriptar")
        self.assertEqual(self.app.text_area[0].value, "026054 123875")
        self.assertNotIn("resultado_dec", self.app.session_state)
        self.app.button[0].click().run()
        self.assertFalse(self.app.exception)
        self.assertEqual(self.app.session_state["resultado_dec"]["mensaje"], "RSA")
        self.assertEqual(self.app.session_state["resultado_dec"]["d"], 8009)

    def test_error_limpia_cifrado_y_transferencia(self):
        self.cifrar()
        self.app.text_area[0].set_value("JOSÉ")
        self.app.button[0].click().run()
        self.assertFalse(self.app.exception)
        self.assertTrue(self.app.error)
        self.assertNotIn("resultado_enc", self.app.session_state)
        self.assertEqual(len(self.app.button), 1)

    def test_mensaje_con_espacios_y_sesiones_independientes(self):
        self.app.text_area[0].set_value(" A  ")
        self.app.button[0].click().run()
        self.app.button[1].click().run()
        self.app.button[0].click().run()
        self.assertEqual(self.app.session_state["resultado_dec"]["mensaje"], " A  ")
        otra = AppTest.from_file(str(Path(__file__).with_name("app.py")), default_timeout=30).run()
        self.assertNotIn("resultado_dec", otra.session_state)

    def test_descifrado_invalido_y_recuperacion(self):
        self.app.radio[0].set_value("Desencriptar").run()
        self.app.button[0].click().run()
        self.app.text_area[0].set_value("12345")
        self.app.button[0].click().run()
        self.assertTrue(self.app.error)
        self.assertNotIn("resultado_dec", self.app.session_state)
        self.app.text_area[0].set_value("026054 123875")
        self.app.button[0].click().run()
        self.assertFalse(self.app.error)
        self.assertEqual(self.app.session_state["resultado_dec"]["mensaje"], "RSA")

    def test_limite_publico(self):
        self.app.text_input[0].set_value("999999999999")
        self.app.button[0].click().run()
        self.assertTrue(self.app.error)
        self.assertFalse(self.app.exception)


if __name__ == "__main__":
    unittest.main()
