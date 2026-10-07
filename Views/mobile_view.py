import threading
import time
import flet as ft
import flet.canvas as cv
from Core.api_client import verificar_status_servidor, enviar_mensagem

def interface_mobile(page: ft.Page):
    page.title = "J.A.R.V.I.S. HUD"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.Colors.BLACK
    page.padding = 10
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    page.fonts = {
        "Orbitron": "https://github.com/google/fonts/raw/main/ofl/orbitron/Orbitron%5Bwght%5D.ttf"
    }
    page.theme = ft.Theme(font_family="Orbitron")

    texto_status = ft.Text(
        "ESTABELECENDO CONEXÃO...",
        size=11,
        color=ft.Colors.YELLOW_ACCENT_400,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER
    )

    texto_chat = ft.Text(
        "Aguardando ordem...",
        size=13,
        color=ft.Colors.WHITE_70,
        text_align=ft.TextAlign.CENTER
    )

    campo_comando = ft.TextField(
        hint_text="Digite um comando para o JARVIS",
        width=290,
        height=45,
        color=ft.Colors.WHITE,
        border_color=ft.Colors.CYAN_ACCENT_400,
        cursor_color=ft.Colors.CYAN_ACCENT_400,
        text_size=12
    )

    def enviar_comando(_=None):
        texto = campo_comando.value.strip() if campo_comando.value else ""
        if not texto:
            return

        texto_chat.value = "Processando..."
        texto_chat.color = ft.Colors.CYAN_ACCENT_400
        page.update()

        resultado = enviar_mensagem(texto)

        if resultado.get("tipo") == "function_call":
            texto_chat.value = f"Ação solicitada: '{resultado['nome']}'."
        else:
            texto_chat.value = resultado.get("resposta", "Sem resposta do servidor.")

        texto_chat.color = ft.Colors.WHITE_70
        campo_comando.value = ""
        page.update()

    texto_jarvis = ft.Text(
        "J.A.R.V.I.S.",
        size=11,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.CYAN_ACCENT_400,
    )

    reator = ft.Container(
        width=120,
        height=120,
        shape=ft.BoxShape.CIRCLE,
        bgcolor=ft.Colors.CYAN_900,
        border=ft.Border.all(2, ft.Colors.CYAN_ACCENT_400),
        shadow=ft.BoxShadow(
            spread_radius=3,
            blur_radius=18,
            color=ft.Colors.CYAN_ACCENT_400,
            offset=ft.Offset(0, 0),
        ),
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=3,
            controls=[
                ft.Icon(ft.Icons.MIC, size=36, color=ft.Colors.WHITE),
                texto_jarvis,
            ],
        ),
        alignment=ft.Alignment.CENTER,
        ink=True,
    )

    anel_externo = ft.ProgressRing(
        width=180,
        height=180,
        stroke_width=2,
        color=ft.Colors.CYAN_200,
        value=0.4,
        rotate=ft.Rotate(angle=0),
    )

    anel_interno = ft.ProgressRing(
        width=150,
        height=150,
        stroke_width=3,
        color=ft.Colors.CYAN_ACCENT_400,
        value=0.65,
        rotate=ft.Rotate(angle=0),
    )

    esfera = ft.Stack(
        width=180,
        height=180,
        alignment=ft.Alignment.CENTER,
        controls=[anel_externo, anel_interno, reator],
    )

    def girar(anel, velocidade):
        angulo = 0.0
        while True:
            angulo += velocidade
            anel.rotate = ft.Rotate(angle=angulo)
            try:
                page.update()
            except Exception:
                break
            time.sleep(0.05)

    threading.Thread(target=girar, args=(anel_externo, 0.025), daemon=True).start()
    threading.Thread(target=girar, args=(anel_interno, -0.045), daemon=True).start()

    def criar_painel_tatico(titulo, controles, largura=155, altura=105):
        desenho_bordas = cv.Canvas(
            width=largura,
            height=altura,
            shapes=[
                cv.Path(
                    elements=[
                        cv.Path.MoveTo(0, 12),
                        cv.Path.LineTo(0, 0),
                        cv.Path.LineTo(12, 0),
                    ],
                    paint=ft.Paint(color=ft.Colors.CYAN_ACCENT_400, stroke_width=2, style=ft.PaintingStyle.STROKE)
                ),
                cv.Path(
                    elements=[
                        cv.Path.MoveTo(largura - 12, 0),
                        cv.Path.LineTo(largura, 0),
                        cv.Path.LineTo(largura, 12),
                    ],
                    paint=ft.Paint(color=ft.Colors.CYAN_ACCENT_400, stroke_width=2, style=ft.PaintingStyle.STROKE)
                ),
                cv.Path(
                    elements=[
                        cv.Path.MoveTo(0, altura - 12),
                        cv.Path.LineTo(0, altura),
                        cv.Path.LineTo(12, altura),
                    ],
                    paint=ft.Paint(color=ft.Colors.CYAN_ACCENT_400, stroke_width=2, style=ft.PaintingStyle.STROKE)
                ),
                cv.Path(
                    elements=[
                        cv.Path.MoveTo(largura - 12, altura),
                        cv.Path.LineTo(largura, altura),
                        cv.Path.LineTo(largura, altura - 12),
                    ],
                    paint=ft.Paint(color=ft.Colors.CYAN_ACCENT_400, stroke_width=2, style=ft.PaintingStyle.STROKE)
                ),
            ]
        )

        conteudo = ft.Container(
            width=largura,
            height=altura,
            padding=8,
            bgcolor="#0A00BCD4",
            content=ft.Column(
                spacing=4,
                controls=[
                    ft.Text(titulo, color=ft.Colors.CYAN_ACCENT_400, size=10, weight=ft.FontWeight.BOLD),
                    ft.Divider(height=1, color=ft.Colors.CYAN_700),
                ] + controles
            )
        )

        return ft.Stack(
            controls=[
                conteudo,
                desenho_bordas
            ]
        )

    popup_bateria = ft.Container(
        padding=6,
        border_radius=4,
        bgcolor="#0A00BCD4",
        border=ft.Border.all(1, ft.Colors.CYAN_700),
        content=ft.Row(
            spacing=6,
            controls=[
                ft.Icon(ft.Icons.BATTERY_CHARGING_FULL, size=14, color=ft.Colors.CYAN_ACCENT_400),
                ft.Text("Bateria: 92%", size=10, color=ft.Colors.WHITE_70)
            ]
        )
    )

    popup_emails = ft.Container(
        padding=6,
        border_radius=4,
        bgcolor="#0A00BCD4",
        border=ft.Border.all(1, ft.Colors.CYAN_700),
        content=ft.Row(
            spacing=6,
            controls=[
                ft.Icon(ft.Icons.EMAIL, size=14, color=ft.Colors.CYAN_ACCENT_400),
                ft.Text("E-mails: 3 novos", size=10, color=ft.Colors.WHITE_70)
            ]
        )
    )

    popups_topo = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=8,
        controls=[
            texto_status,
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8,
                controls=[popup_bateria, popup_emails]
            )
        ]
    )

    painel_esquerdo = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            criar_painel_tatico("SYSTEM STATUS", [
                ft.Text("Bateria: 92%", color=ft.Colors.WHITE_70, size=9),
                ft.Text("Memória: Estável", color=ft.Colors.WHITE_70, size=9),
            ]),
            ft.Container(height=6),
            criar_painel_tatico("NOTIFICAÇÕES", [
                ft.Text("Ambiente: 100%", color=ft.Colors.WHITE_70, size=9),
                ft.Text("E-mails: 3 novos", color=ft.Colors.WHITE_70, size=9),
            ])
        ]
    )

    painel_direito = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            criar_painel_tatico("CONECTIVIDADE", [
                ft.Text("Rede: Render", color=ft.Colors.WHITE_70, size=9),
                ft.Text("Ping: 45ms", color=ft.Colors.WHITE_70, size=9),
            ]),
            ft.Container(height=6),
            criar_painel_tatico("SISTEMA", [
                ft.Text("Escuta Ativa", color=ft.Colors.WHITE_70, size=9),
                ft.Text("Status: Ótimo", color=ft.Colors.WHITE_70, size=9),
            ])
        ]
    )

    conteudo_dinamico = ft.Container()

    def reordenar_layout(_=None):
        largura = page.width or 0
        altura = page.height or 0

        if largura > altura:
            conteudo_dinamico.content = ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
                controls=[
                    texto_status,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            painel_esquerdo,
                            ft.Container(width=10),
                            esfera,
                            ft.Container(width=10),
                            painel_direito
                        ]
                    ),
                    campo_comando,
                    ft.Button(content="Enviar", on_click=enviar_comando),
                    texto_chat
                ]
            )
        else:
            conteudo_dinamico.content = ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                controls=[
                    popups_topo,
                    esfera,
                    campo_comando,
                    ft.Button(content="Enviar", on_click=enviar_comando),
                    texto_chat
                ]
            )
        page.update()

    page.on_resize = reordenar_layout

    page.add(conteudo_dinamico)
    reordenar_layout()

    if verificar_status_servidor():
        texto_status.value = "S I S T E M A   O N L I N E"
        texto_status.color = ft.Colors.CYAN_ACCENT_400
    else:
        texto_status.value = "S I S T E M A   O F F L I N E"
        texto_status.color = ft.Colors.RED_ACCENT_400

    page.update()
