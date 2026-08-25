# -*- coding: utf-8 -*-
"""Gera o QR code da Bienal 2026 apontando para a LP /romance-historico."""
import os
import qrcode

URL = ("https://www.livrosdofalco.com.br/romance-historico/"
       "?utm_source=bienal&utm_medium=qrcode&utm_campaign=bienal2026")

qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # 30% de tolerancia:
    box_size=20,                                        # foto amassada, tela
    border=4,                                            # riscada, luz ruim
)
qr.add_data(URL)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")

destino = os.path.join(os.path.dirname(os.path.abspath(__file__)), "qr-bienal-romance-historico.png")
img.save(destino)
print("gerado:", img.size, "px ·", URL)
