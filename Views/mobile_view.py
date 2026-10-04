import threading
import time
import flet as ft
from Core.api_client import verificar_status_servidor, enviar_mensagem

def interface_mobile(page: ft.Page):
    page.title = "J.A.R.V.I.S. HUD"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.Colors.BLACK
    page.padding = 50
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    texto_status = ft.Text(
        "ESTABELECENDO CONEXÃO...",
        size=14,
        color=ft.Colors.YELLOW_ACCENT_400,
        weight=ft.FontWeight.BOLD
    )

    texto_chat = ft.Text(
        "Aguardando ordem...",
        size=16,
        color=ft.Colors.WHITE_70,
        text_align=ft.TextAlign.CENTER
    )

    campo_comando = ft.TextField(
        hint_text="Digite um comando para o JARVIS",
        width=320,
        color=ft.Colors.WHITE,
        border_color=ft.Colors.CYAN_ACCENT_400,
        cursor_color=ft.Colors.CYAN_ACCENT_400,
    )

    def enviar_comando(e):
        texto = campo_comando.value.strip()
        if not texto:
            return

        texto_chat.value = "Processando..."
        texto_chat.color = ft.Colors.CYAN_ACCENT_400
        page.update()

        resultado = enviar_mensagem(texto)

        if resultado.get("tipo") == "function_call":
            texto_chat.value = (
                f"O backend pediu a ação '{resultado['nome']}', "
                "que só pode ser executada pelo app no telemóvel (Termux), não por aqui."
            )
        else:
            texto_chat.value = resultado.get("resposta", "Sem resposta do servidor.")

        texto_chat.color = ft.Colors.WHITE_70
        campo_comando.value = ""
        page.update()

    texto_jarvis = ft.Text(
        "J.A.R.V.I.S.",
        size=13,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.CYAN_ACCENT_400,
    )

    reator = ft.Container(
        width=150,
        height=150,
        shape=ft.BoxShape.CIRCLE,
        bgcolor=ft.Colors.CYAN_900,
        border=ft.Border.all(3, ft.Colors.CYAN_ACCENT_400),
        shadow=ft.BoxShadow(
            spread_radius=5,
            blur_radius=25,
            color=ft.Colors.CYAN_ACCENT_400,
            offset=ft.Offset(0, 0),
        ),
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=6,
            controls=[
                ft.Icon(ft.Icons.MIC, size=48, color=ft.Colors.WHITE),
                texto_jarvis,
            ],
        ),
        alignment=ft.Alignment.CENTER,
        ink=True,
    )

    anel_externo = ft.ProgressRing(
        width=220,
        height=220,
        stroke_width=2,
        color=ft.Colors.CYAN_200,
        value=0.55,
        rotate=ft.Rotate(angle=0),
    )

    anel_interno = ft.ProgressRing(
        width=175,
        height=175,
        stroke_width=4,
        color=ft.Colors.CYAN_ACCENT_400,
        value=0.7,
        rotate=ft.Rotate(angle=0),
    )

    esfera = ft.Stack(
        width=220,
        height=220,
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

    def criar_painel(titulo, controles):
        return ft.Container(
            width=180,
            border=ft.Border.all(1, ft.Colors.CYAN_700),
            border_radius=5,
            padding=10,
            bgcolor="#0A00BCD4",
            content=ft.Column(
                spacing=5,
                controls=[
                    ft.Text(titulo, color=ft.Colors.CYAN_ACCENT_400, size=12, weight=ft.FontWeight.BOLD),
                    ft.Divider(height=1, color=ft.Colors.CYAN_700),
                ] + controles
            )
        )

    painel_esquerdo = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            criar_painel("SYSTEM STATUS v14.2", [
                ft.Text("Bateria: 92%", color=ft.Colors.WHITE_70, size=11),
                ft.Text("Memória: Estável", color=ft.Colors.WHITE_70, size=11),
            ]),
            ft.Container(height=10),
            criar_painel("NOTIFICAÇÕES", [
                ft.Text("Análise Ambiental: 100%", color=ft.Colors.WHITE_70, size=11),
                ft.Text("Protocolo Ativo", color=ft.Colors.WHITE_70, size=11),
            ])
        ]
    )

    painel_direito = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            criar_painel("CONECTIVIDADE", [
                ft.Text("Rede: Render Cloud", color=ft.Colors.WHITE_70, size=11),
                ft.Text("Ping: 45ms", color=ft.Colors.WHITE_70, size=11),
            ]),
            ft.Container(height=10),
            criar_painel("SISTEMA", [
                ft.Text("🎙️ Escuta Ativa", color=ft.Colors.WHITE_70, size=11),
                ft.Text("🎵 Mídia: Desconectado", color=ft.Colors.WHITE_70, size=11),
            ])
        ]
    )

    layout_principal = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            painel_esquerdo,
            ft.Container(width=20),
            esfera,
            ft.Container(width=20),
            painel_direito
        ]
    )

    page.add(
        texto_status,
        ft.Container(height=20),
        layout_principal,
        ft.Container(height=20),
        campo_comando,
        ft.Container(height=10),
        ft.Button(content="Enviar", on_click=enviar_comando),
        ft.Container(height=20),
        texto_chat
    )

    page.update()

    if verificar_status_servidor():
        texto_status.value = "S I S T E M A   O N L I N E"
        texto_status.color = ft.Colors.CYAN_ACCENT_400
    else:
        texto_status.value = "S I S T E M A   O F F L I N E"
        texto_status.color = ft.Colors.RED_ACCENT_400

    page.update()
