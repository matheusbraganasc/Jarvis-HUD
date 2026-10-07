import threading
import time
import flet as ft

from Core.api_client import (
    verificar_status_servidor,
    enviar_mensagem,
)

# Paleta Stark Tech - Azul / Ciano Holográfico
CYAN = "#00F0FF"
CYAN_BRIGHT = "#64FFFF"
CYAN_DARK = "#003246"
CYAN_GLOW = "#0078A0"
CYAN_BORDER = "#00A0C8"
BG_DARK = "#02070D"
BG_PANEL = "#051321"
TEXT_WHITE = "#E0F8FF"
TEXT_MUTED = "#5096B4"
RED_ALERT = "#FF2A50"


def interface_mobile(page: ft.Page):
    page.title = "J.A.R.V.I.S. HUD - STARK INTERFACE"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = BG_DARK
    page.padding = 0
    page.spacing = 0
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    estado = {
        "orientacao": "portrait",
        "painel_comando": False,
        "popup_aberto": None,
        "online": True,
    }

    # --- NÚCLEO CENTRAL (REATOR STARK TRIANGULAR) ---
    icone_triangulo = ft.Icon(ft.Icons.CHANGE_HISTORY, size=40, color=CYAN_BRIGHT)

    triangulo_nucleo = ft.Container(
        width=45,
        height=45,
        alignment=ft.Alignment.CENTER,
        content=icone_triangulo,
    )

    reator_circulo = ft.Container(
        width=140,
        height=140,
        shape=ft.BoxShape.CIRCLE,
        bgcolor=ft.Colors.with_opacity(0.25, CYAN_DARK),
        border=ft.Border.all(2, CYAN),
        shadow=ft.BoxShadow(spread_radius=6, blur_radius=30, color=CYAN_GLOW),
        alignment=ft.Alignment.CENTER,
        content=triangulo_nucleo,
    )

    anel_1 = ft.ProgressRing(width=220, height=220, stroke_width=2, color=CYAN_BORDER, value=0.6, rotate=ft.Rotate(0))
    anel_2 = ft.ProgressRing(width=185, height=185, stroke_width=3, color=CYAN, value=0.75, rotate=ft.Rotate(0))
    anel_3 = ft.ProgressRing(width=160, height=160, stroke_width=1.5, color=CYAN_BRIGHT, value=0.4, rotate=ft.Rotate(0))

    esfera_stark = ft.Stack(
        width=220,
        height=220,
        alignment=ft.Alignment.CENTER,
        controls=[anel_1, anel_2, anel_3, reator_circulo],
    )

    def animar_aneis():
        ang1, ang2, ang3 = 0.0, 0.0, 0.0
        while True:
            ang1 += 0.02
            ang2 -= 0.035
            ang3 += 0.05
            anel_1.rotate = ft.Rotate(angle=ang1)
            anel_2.rotate = ft.Rotate(angle=ang2)
            anel_3.rotate = ft.Rotate(angle=ang3)
            try:
                page.update()
            except Exception:
                break
            time.sleep(0.04)

    threading.Thread(target=animar_aneis, daemon=True).start()

    # --- COMPONENTES DE DESIGN CIBERNÉTICO ---
    def criar_painel_stark(titulo, conteudo, width=175):
        return ft.Container(
            width=width,
            padding=8,
            border_radius=4,
            bgcolor=ft.Colors.with_opacity(0.4, BG_PANEL),
            border=ft.Border.all(1, ft.Colors.with_opacity(0.6, CYAN_BORDER)),
            content=ft.Column(
                spacing=4,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(titulo.upper(), size=9, weight=ft.FontWeight.BOLD, color=CYAN),
                            ft.Container(width=6, height=6, bgcolor=CYAN, shape=ft.BoxShape.CIRCLE),
                        ],
                    ),
                    ft.Divider(height=1, color=ft.Colors.with_opacity(0.3, CYAN_BORDER)),
                    *conteudo,
                ],
            ),
        )

    # --- MODAL OVERLAY HOLOGRÁFICO ---
    modal_titulo = ft.Text("", size=12, weight=ft.FontWeight.BOLD, color=CYAN_BRIGHT)
    modal_conteudo = ft.Column(spacing=6)

    def fechar_modal(_=None):
        overlay_modal.visible = False
        page.update()

    overlay_modal = ft.Container(
        visible=False,
        alignment=ft.Alignment.CENTER,
        bgcolor=ft.Colors.with_opacity(0.75, BG_DARK),
        expand=True,
        content=ft.Container(
            width=310,
            padding=14,
            border_radius=6,
            bgcolor=BG_PANEL,
            border=ft.Border.all(1.5, CYAN),
            shadow=ft.BoxShadow(spread_radius=2, blur_radius=20, color=CYAN_GLOW),
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[modal_titulo, ft.IconButton(ft.Icons.CLOSE, icon_color=CYAN, icon_size=18, on_click=fechar_modal)],
                    ),
                    ft.Divider(height=1, color=CYAN_BORDER),
                    modal_conteudo,
                ],
            ),
        ),
    )

    # --- NÓS DO TOPO (BATERIA, SERVIDORES, ETC.) ---
    def criar_no_status(icone, titulo, valor, identificador, detalhes):
        def abrir(_=None):
            if not estado["online"] and identificador != "servidor":
                return
            modal_titulo.value = f"// {titulo.upper()}"
            modal_conteudo.controls = [
                ft.Row([ft.Icon(ft.Icons.CHEVRON_RIGHT, size=12, color=CYAN), ft.Text(d, size=11, color=TEXT_WHITE)])
                for d in detalhes
            ]
            overlay_modal.visible = True
            page.update()

        return ft.Container(
            width=140,
            padding=8,
            border_radius=4,
            bgcolor=ft.Colors.with_opacity(0.2, BG_PANEL),
            border=ft.Border.all(1, CYAN_BORDER),
            ink=True,
            on_click=abrir,
            content=ft.Row(
                spacing=8,
                controls=[
                    ft.Icon(icone, size=16, color=CYAN),
                    ft.Column(
                        spacing=0,
                        controls=[
                            ft.Text(titulo, size=9, weight=ft.FontWeight.BOLD, color=CYAN),
                            ft.Text(valor, size=9, color=TEXT_MUTED),
                        ],
                    ),
                ],
            ),
        )

    btn_bateria = criar_no_status(ft.Icons.BATTERY_CHARGING_FULL, "BATERIA", "92% • STABLE", "bateria", ["Tensão: 4.2V", "Carga: 92%", "Status: Estável"])
    btn_servidor = criar_no_status(ft.Icons.CLOUD_DONE, "SERVIDOR", "● ONLINE", "servidor", ["Host: Render Cloud", "Latência: 42ms", "Status: Operacional"])
    btn_email = criar_no_status(ft.Icons.EMAIL, "MENSAGENS", "3 NOVAS", "email", ["3 mensagens não lidas", "Prioridade: Alta"])
    btn_noticias = criar_no_status(ft.Icons.NEWSPAPER, "NOTÍCIAS", "FEED ATIVO", "noticias", ["Destaques Starknet", "Alertas globais: 0"])

    linha_top = ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=10, controls=[btn_bateria, btn_servidor])
    linha_bottom = ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=10, controls=[btn_email, btn_noticias])

    # --- CAMPO DE COMANDO & CHAT ---
    campo_comando = ft.TextField(
        hint_text="DIGITE UM COMANDO PARA O JARVIS...",
        width=280, height=42, color=TEXT_WHITE,
        hint_style=ft.TextStyle(color=TEXT_MUTED, size=11),
        border_color=CYAN_BORDER, focused_border_color=CYAN, cursor_color=CYAN,
        text_size=11, content_padding=8,
    )

    texto_chat = ft.Text("SYSTEM READY. LISTENING...", size=11, color=TEXT_MUTED, text_align=ft.TextAlign.CENTER)

    def enviar_cmd(_=None):
        txt = campo_comando.value.strip()
        if not txt:
            return
        texto_chat.value = "PROCESSING QUERY..."
        texto_chat.color = CYAN
        page.update()
        try:
            res = enviar_mensagem(txt)
            texto_chat.value = res.get("resposta", "Comando executado.")
            texto_chat.color = TEXT_WHITE
        except Exception:
            texto_chat.value = "ERRO DE CONEXÃO COM O NÚCLEO."
            texto_chat.color = RED_ALERT
        campo_comando.value = ""
        page.update()

    btn_enviar = ft.IconButton(icon=ft.Icons.SEND, icon_color=CYAN, icon_size=18, on_click=enviar_cmd)

    def alternar_painel_comando(_=None):
        estado["painel_comando"] = not estado["painel_comando"]
        painel_bottom.visible = estado["painel_comando"]
        seta_comando.icon = ft.Icons.KEYBOARD_ARROW_DOWN if estado["painel_comando"] else ft.Icons.KEYBOARD_ARROW_UP
        page.update()

    seta_comando = ft.IconButton(icon=ft.Icons.KEYBOARD_ARROW_UP, icon_color=CYAN, icon_size=30, on_click=alternar_painel_comando)

    painel_bottom = ft.Container(
        visible=False,
        padding=10,
        bgcolor=ft.Colors.with_opacity(0.85, BG_PANEL),
        border=ft.Border.all(1, CYAN_BORDER),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
            controls=[
                ft.Row([campo_comando, btn_enviar], alignment=ft.MainAxisAlignment.CENTER),
                texto_chat,
            ],
        ),
    )

    # --- LAYOUT EM PÉ (PORTRAIT) ---
    texto_status = ft.Text("J A R V I S   S Y S T E M S", size=12, color=CYAN, weight=ft.FontWeight.BOLD)

    layout_portrait = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            ft.Container(height=5),
            texto_status,
            linha_top,
            esfera_stark,
            linha_bottom,
            seta_comando,
            painel_bottom,
            ft.Container(height=5),
        ],
    )

    # --- LAYOUT DEITADO (LANDSCAPE - PAINEL COMPLETO STARK) ---
    col_esquerda_1 = ft.Column([
        criar_painel_stark("DEVICE", [
            ft.Text("MARK VII • OS v7.2", size=8, color=TEXT_MUTED),
            ft.Text("CPU: 2.7 GHz • 8 CORES", size=8, color=TEXT_MUTED),
            ft.Text("RAM: 16 GB STABLE", size=8, color=TEXT_MUTED),
        ]),
        criar_painel_stark("SYSTEM MONITOR", [
            ft.Text("CPU USAGE: 55%", size=8, color=CYAN),
            ft.ProgressBar(value=0.55, color=CYAN, height=4),
            ft.Text("RAM USAGE: 68%", size=8, color=CYAN),
            ft.ProgressBar(value=0.68, color=CYAN, height=4),
        ]),
    ], spacing=6)

    col_esquerda_2 = ft.Column([
        criar_painel_stark("DIAGNOSTICS", [
            ft.Text("SYSTEM STATUS: 100%", size=8, color=CYAN_BRIGHT),
            ft.Text("PERFORMANCE: SECURE", size=8, color=TEXT_MUTED),
        ]),
        criar_painel_stark("CONNECTIONS", [
            ft.Text("SATELLITE 01: CONNECTED", size=8, color=TEXT_MUTED),
            ft.Text("SATELLITE 02: CONNECTED", size=8, color=TEXT_MUTED),
        ]),
    ], spacing=6)

    col_direita_1 = ft.Column([
        criar_painel_stark("WEATHER", [
            ft.Text("28°C FORTALEZA", size=8, color=CYAN),
            ft.Text("HUMIDITY: 65% • WIND 12 KM/H", size=8, color=TEXT_MUTED),
        ]),
        criar_painel_stark("CALENDAR", [
            ft.Text("OCT 2026 • UPCOMING EVENTS", size=8, color=CYAN),
            ft.Text("10:00 AM - SYSTEM CHECK", size=8, color=TEXT_MUTED),
        ]),
    ], spacing=6)

    col_direita_2 = ft.Column([
        criar_painel_stark("DATA STREAM", [
            ft.Text("VOICE MATCH: 100%", size=8, color=CYAN_BRIGHT),
            ft.Text("LATITUDE: 3.7319° S", size=8, color=TEXT_MUTED),
        ]),
        criar_painel_stark("FILES & DOCS", [
            ft.Text("PROJECT_REPORT.PDF", size=8, color=TEXT_MUTED),
            ft.Text("SECURITY_PROTOCOL.PDF", size=8, color=TEXT_MUTED),
        ]),
    ], spacing=6)

    col_centro = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=8,
        controls=[
            esfera_stark,
            ft.Row([campo_comando, btn_enviar], alignment=ft.MainAxisAlignment.CENTER),
            texto_chat,
        ],
    )

    layout_landscape = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
        controls=[col_esquerda_1, col_esquerda_2, col_centro, col_direita_1, col_direita_2],
    )

    layout_landscape.visible = False

    stack_main = ft.Stack(
        expand=True,
        alignment=ft.Alignment.CENTER,
        controls=[layout_portrait, layout_landscape, overlay_modal],
    )

    page.add(stack_main)

    # --- RESPONSIVIDADE LANDSCAPE / PORTRAIT ---
    def redimensionar(_=None):
        if page.width and page.height:
            if page.width > page.height:
                layout_portrait.visible = False
                layout_landscape.visible = True
            else:
                layout_portrait.visible = True
                layout_landscape.visible = False
            page.update()

    page.on_resize = redimensionar

    # --- MONITORAMENTO DO SERVIDORES ---
    def atualizar_online(online):
        estado["online"] = online
        if online:
            texto_status.value = "J A R V I S   S Y S T E M S"
            texto_status.color = CYAN
            icone_triangulo.color = CYAN_BRIGHT
            reator_circulo.shadow = ft.BoxShadow(spread_radius=6, blur_radius=30, color=CYAN_GLOW)
        else:
            texto_status.value = "S Y S T E M S   O F F L I N E"
            texto_status.color = RED_ALERT
            icone_triangulo.color = RED_ALERT
            reator_circulo.shadow = ft.BoxShadow(spread_radius=2, blur_radius=10, color=RED_ALERT)

        try:
            page.update()
        except Exception:
            pass

    def loop_servidor():
        while True:
            try:
                st = verificar_status_servidor()
            except Exception:
                st = False
            atualizar_online(st)
            time.sleep(12)

    threading.Thread(target=loop_servidor, daemon=True).start()
    page.update()
