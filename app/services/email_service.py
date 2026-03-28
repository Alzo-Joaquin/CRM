import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


def enviar_mail(destinatario, asunto, cuerpo_html):
    servidor = os.getenv("MAIL_SERVER")
    puerto = int(os.getenv("MAIL_PORT", 587))
    usuario = os.getenv("MAIL_USERNAME")
    password = os.getenv("MAIL_PASSWORD")
    remitente = os.getenv("MAIL_DEFAULT_SENDER")

    mensaje = MIMEMultipart()
    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje["Subject"] = asunto

    mensaje.attach(MIMEText(cuerpo_html, "html"))

    try:
        with smtplib.SMTP(servidor, puerto) as server:
            server.starttls()
            server.login(usuario, password)
            server.send_message(mensaje)
    except Exception as e:
        print(f"Error enviando mail: {e}")

def enviar_mail_venta(destinatario, venta, cliente, items):
    asunto = f"CRM Comercial | Comprobante de compra #{venta.id}"

    filas_items = ""
    for item in items:
        filas_items += f"""
        <tr>
            <td style="padding: 12px; border-bottom: 1px solid #e5e7eb;">{item['producto']}</td>
            <td style="padding: 12px; border-bottom: 1px solid #e5e7eb; text-align: center;">{item['cantidad']}</td>
            <td style="padding: 12px; border-bottom: 1px solid #e5e7eb; text-align: right;">${item['precio_unitario']:.2f}</td>
            <td style="padding: 12px; border-bottom: 1px solid #e5e7eb; text-align: right;">${item['subtotal']:.2f}</td>
        </tr>
        """

    nombre_cliente = cliente.nombre
    if hasattr(cliente, "apellido") and cliente.apellido:
        nombre_cliente = f"{cliente.nombre} {cliente.apellido}"

    fecha_texto = venta.fecha.strftime("%d/%m/%Y %H:%M") if venta.fecha else "-"

    cuerpo = f"""
    <html>
      <body style="margin: 0; padding: 0; background-color: #f3f4f6; font-family: Arial, sans-serif; color: #111827;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f3f4f6; padding: 32px 0;">
          <tr>
            <td align="center">
              <table width="680" cellpadding="0" cellspacing="0" style="max-width: 680px; width: 100%; background-color: #ffffff; border-radius: 14px; overflow: hidden; box-shadow: 0 4px 14px rgba(0,0,0,0.08);">

                <tr>
                  <td style="background: linear-gradient(135deg, #1d4ed8, #2563eb); padding: 28px 32px; color: white;">
                    <h1 style="margin: 0; font-size: 24px;">CRM Comercial</h1>
                    <p style="margin: 8px 0 0; font-size: 14px; color: #dbeafe;">
                      Comprobante de compra
                    </p>
                  </td>
                </tr>

                <tr>
                  <td style="padding: 32px;">
                    <h2 style="margin: 0 0 12px; font-size: 22px; color: #111827;">
                      Gracias por tu compra
                    </h2>

                    <p style="margin: 0 0 22px; font-size: 15px; line-height: 1.6; color: #4b5563;">
                      Hola <strong>{nombre_cliente}</strong>, te compartimos el detalle de tu operación registrada en nuestro sistema.
                    </p>

                    <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 24px; background-color: #f9fafb; border: 1px solid #e5e7eb; border-radius: 10px;">
                      <tr>
                        <td style="padding: 18px 20px;">
                          <p style="margin: 0 0 8px; font-size: 14px; color: #6b7280;">
                            <strong>Número de comprobante:</strong> #{venta.id}
                          </p>
                          <p style="margin: 0 0 8px; font-size: 14px; color: #6b7280;">
                            <strong>Fecha:</strong> {fecha_texto}
                          </p>
                          <p style="margin: 0; font-size: 14px; color: #6b7280;">
                            <strong>Estado:</strong> {venta.estado}
                          </p>
                        </td>
                      </tr>
                    </table>

                    <table width="100%" cellpadding="0" cellspacing="0" style="border-collapse: collapse; margin-bottom: 24px;">
                      <thead>
                        <tr style="background-color: #eff6ff;">
                          <th style="padding: 12px; text-align: left; font-size: 14px; color: #1e3a8a; border-bottom: 1px solid #dbeafe;">Producto</th>
                          <th style="padding: 12px; text-align: center; font-size: 14px; color: #1e3a8a; border-bottom: 1px solid #dbeafe;">Cantidad</th>
                          <th style="padding: 12px; text-align: right; font-size: 14px; color: #1e3a8a; border-bottom: 1px solid #dbeafe;">Precio unitario</th>
                          <th style="padding: 12px; text-align: right; font-size: 14px; color: #1e3a8a; border-bottom: 1px solid #dbeafe;">Subtotal</th>
                        </tr>
                      </thead>
                      <tbody>
                        {filas_items}
                      </tbody>
                    </table>

                    <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 28px;">
                      <tr>
                        <td align="right">
                          <div style="display: inline-block; background-color: #ecfdf5; color: #065f46; border: 1px solid #a7f3d0; padding: 14px 18px; border-radius: 10px; font-size: 18px; font-weight: bold;">
                            Total: ${float(venta.total):.2f}
                          </div>
                        </td>
                      </tr>
                    </table>

                    <p style="margin: 0; font-size: 14px; line-height: 1.6; color: #6b7280;">
                      Este correo fue generado automáticamente por el sistema CRM Comercial.
                      Conservá este comprobante como referencia de tu compra.
                    </p>
                  </td>
                </tr>

                <tr>
                  <td style="padding: 20px 32px; background-color: #f9fafb; border-top: 1px solid #e5e7eb;">
                    <p style="margin: 0; font-size: 12px; color: #9ca3af; text-align: center;">
                      CRM Comercial · Sistema de gestión y ventas
                    </p>
                  </td>
                </tr>

              </table>
            </td>
          </tr>
        </table>
      </body>
    </html>
    """

    enviar_mail(destinatario, asunto, cuerpo)

# def enviar_mail_venta(destinatario, venta, cliente, items):
#     asunto = f"Comprobante de compra #{venta.id}"

#     detalle_items = ""
#     for item in items:
#         detalle_items += f"""
#         <tr>
#             <td>{item['producto']}</td>
#             <td>{item['cantidad']}</td>
#             <td>${item['precio_unitario']}</td>
#             <td>${item['subtotal']}</td>
#         </tr>
#         """

#     cuerpo = f"""
#     <h2>Gracias por tu compra</h2>
#     <p><strong>Cliente:</strong> {cliente.nombre}</p>
#     <p><strong>Fecha:</strong> {venta.fecha}</p>

#     <table border="1" cellpadding="6" cellspacing="0">
#         <tr>
#             <th>Producto</th>
#             <th>Cantidad</th>
#             <th>Precio</th>
#             <th>Subtotal</th>
#         </tr>
#         {detalle_items}
#     </table>

#     <h3>Total: ${venta.total}</h3>
#     """

#     enviar_mail(destinatario, asunto, cuerpo)