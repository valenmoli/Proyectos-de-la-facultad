"""Dentro de pytest, el armado de documentos no vuelve a lanzar pytest (seria recursivo)."""
import os

os.environ["TP_EN_TESTS"] = "1"
