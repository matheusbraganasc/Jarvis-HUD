import threading
import time
import flet as ft

from Core.api_client import (
    verificar_status_servidor,
    enviar_mensagem,
)


CYAN = ft.Colors.CYAN_ACCENT_400
CYAN_LIGHT = ft.Colors.CYAN_200
CYAN_DARK = ft.Colors.CYAN_900
CYAN_BORDER = ft.Colors.CYAN_700
WHITE = ft.Colors.WHITE
WHITE_70 = ft.Colors.WHITE_70
BLACK = ft.Colors.BLACK


def interface_mobile(page: ft.Page):
    page.title = "J.A.R.V.I.S. HUD"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = BLACK
    page.padding = 0
    page.spacing = 0
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    estado = {
        "orientacao": "portrait",
        "painel_comando": False,
        "popup_aberto": None,
    }

    texto_status = ft.Text(
        "ESTABELECENDO CONEXÃO...",
        size=13,
        color=ft.Colors.YELLOW_ACCENT_400,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )

    texto_jarvis = ft.Text(
        "J.A.R.V.I.S.",
        size=12,
        weight=ft.FontWeight.BOLD,
        color=CYAN,
        text_align=ft.TextAlign.CENTER,
    )

    reator = ft.Container(
        width=130,
        height=130,
        shape=ft.BoxShape.CIRCLE,
        bgcolor=CYAN_DARK,
        border=ft.Border.all(3, CYAN),
        shadow=ft.BoxShadow(
            spread_radius=4,
            blur_radius=25,
            color=CYAN,
            offset=ft.Offset(0, 0),
        ),
        alignment=ft.Alignment.CENTER,
        ink=True,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5,
            controls=[
                ft.Icon(
                    ft.Icons.MIC,
                    size=42,
                    color=WHITE,
                ),
                texto_jarvis,
            ],
        ),
    )

    anel_externo = ft.ProgressRing(
        width=205,
        height=205,
        stroke_width=2,
        color=CYAN_LIGHT,
        value=0.55,
        rotate=ft.Rotate(angle=0),
    )

    anel_interno = ft.ProgressRing(
        width=170,
        height=170,
        stroke_width=4,
        color=CYAN,
        value=0.70,
        rotate=ft.Rotate(angle=0),
    )

    esfera = ft.Stack(
        width=205,
        height=205,
        alignment=ft.Alignment.CENTER,
        controls=[
            anel_externo,
            anel_interno,
            reator,
        ],
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

    threading.Thread(
        target=girar,
        args=(anel_externo, 0.025),
        daemon=True,
    ).start()

    threading.Thread(
        target=girar,
        args=(anel_interno, -0.045),
        daemon=True,
    ).start()

    popup_detalhes = {}

    def criar_popup(
        icone,
        titulo,
        resumo,
        detalhes,
        identificador,
    ):
        titulo_texto = ft.Text(
            titulo,
            size=11,
            weight=ft.FontWeight.BOLD,
            color=CYAN,
        )

        resumo_texto = ft.Text(
            resumo,
            size=10,
            color=WHITE_70,
        )

        conteudo_detalhes = ft.Column(
            spacing=5,
            visible=False,
            controls=[
                ft.Divider(
                    height=1,
                    color=CYAN_BORDER,
                ),
                *[
                    ft.Text(
                        item,
                        size=10,
                        color=WHITE_70,
                    )
                    for item in detalhes
                ],
            ],
        )

        def clicar(e):
            if estado["popup_aberto"] == identificador:
                estado["popup_aberto"] = None
                conteudo_detalhes.visible = False
            else:
                estado["popup_aberto"] = identificador

                for popup_id, detalhes_ref in popup_detalhes.items():
                    if popup_id != identificador:
                        detalhes_ref.visible = False

                conteudo_detalhes.visible = True

            page.update()

        container = ft.Container(
            width=135,
            padding=8,
            border_radius=6,
            bgcolor="#080E1113",
            border=ft.Border.all(
                1,
                CYAN_BORDER,
            ),
            ink=True,
            on_click=clicar,
            content=ft.Column(
                spacing=5,
                controls=[
                    ft.Row(
                        spacing=6,
                        controls=[
                            ft.Icon(
                                icone,
                                size=15,
                                color=CYAN,
                            ),
                            titulo_texto,
                        ],
                    ),
                    resumo_texto,
                    conteudo_detalhes,
                ],
            ),
        )

        return container, conteudo_detalhes

    popup_bateria, detalhes_bateria = criar_popup(
        ft.Icons.BATTERY_CHARGING_FULL,
        "BATERIA",
        "92% • Carregando",
        [
            "Carga atual: 92%",
            "Estado: Carregando",
            "Última carga: 100%",
            "Temperatura: --°C",
        ],
        "bateria",
    )

    popup_detalhes["bateria"] = detalhes_bateria

    popup_servidor, detalhes_servidor = criar_popup(
        ft.Icons.CLOUD,
        "SERVIDOR",
        "● ONLINE",
        [
            "Backend: Render Cloud",
            "Ping: 45 ms",
            "Latência: -- ms",
            "Status: Operacional",
        ],
        "servidor",
    )

    popup_detalhes["servidor"] = detalhes_servidor

    popup_email, detalhes_email = criar_popup(
        ft.Icons.EMAIL,
        "E-MAIL",
        "3 não lidos",
        [
            "3 mensagens não lidas",
            "Último: --",
            "Remetente: --",
            "Assunto: --",
        ],
        "email",
    )

    popup_detalhes["email"] = detalhes_email

    popup_noticias, detalhes_noticias = criar_popup(
        ft.Icons.NEWSPAPER,
        "NOTÍCIAS",
        "5 importantes",
        [
            "1 notícia importante",
            "5 notícias recentes",
            "Tecnologia: --",
            "Mundo: --",
        ],
        "noticias",
    )

    popup_detalhes["noticias"] = detalhes_noticias

    linha_popups_superior = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=8,
        controls=[
            popup_bateria,
            popup_servidor,
        ],
    )

    linha_popups_inferior = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=8,
        controls=[
            popup_email,
            popup_noticias,
        ],
    )

    seta_comando = ft.IconButton(
        icon=ft.Icons.KEYBOARD_ARROW_DOWN,
        icon_color=CYAN,
        icon_size=38,
        tooltip="Abrir comandos",
    )

    campo_comando = ft.TextField(
        hint_text="Diga ou digite um comando para o JARVIS",
        width=340,
        height=55,
        color=WHITE,
        hint_style=ft.TextStyle(
            color=WHITE_70,
        ),
        border_color=CYAN,
        focused_border_color=CYAN,
        cursor_color=CYAN,
        text_size=14,
    )

    texto_chat = ft.Text(
        "Aguardando ordem...",
        size=14,
        color=WHITE_70,
        text_align=ft.TextAlign.CENTER,
    )

    def enviar_comando(e):
        texto = campo_comando.value.strip()

        if not texto:
            return

        texto_chat.value = "PROCESSANDO..."
        texto_chat.color = CYAN
        page.update()

        try:
            resultado = enviar_mensagem(texto)

            if resultado.get("tipo") == "function_call":
                texto_chat.value = (
                    f"Ação solicitada: "
                    f"{resultado.get('nome', 'desconhecida')}"
                )
            else:
                texto_chat.value = resultado.get(
                    "resposta",
                    "Sem resposta do servidor.",
                )

            texto_chat.color = WHITE_70

        except Exception as erro:
            texto_chat.value = (
                "Falha na comunicação com o JARVIS."
            )
            texto_chat.color = ft.Colors.RED_ACCENT_400
            print(f"Erro JARVIS: {erro}")

        campo_comando.value = ""
        page.update()

    botao_enviar = ft.Button(
        content="ENVIAR",
        on_click=enviar_comando,
    )

    def fechar_comandos():
        estado["painel_comando"] = False
        painel_comando.visible = False
        seta_comando.visible = True
        page.update()

    painel_comando = ft.Column(
        visible=False,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=14,
        controls=[
            ft.IconButton(
                icon=ft.Icons.KEYBOARD_ARROW_UP,
                icon_color=CYAN,
                icon_size=34,
                on_click=lambda e: fechar_comandos(),
            ),
            campo_comando,
            botao_enviar,
            texto_chat,
        ],
    )

    def abrir_comandos(e):
        estado["painel_comando"] = True
        painel_comando.visible = True
        seta_comando.visible = False
        page.update()

    seta_comando.on_click = abrir_comandos

    def criar_painel(titulo, icone, controles):
        return ft.Container(
            width=175,
            padding=10,
            border_radius=5,
            bgcolor="#080E1113",
            border=ft.Border.all(
                1,
                CYAN_BORDER,
            ),
            content=ft.Column(
                spacing=5,
                controls=[
                    ft.Row(
                        spacing=6,
                        controls=[
                            ft.Icon(
                                icone,
                                size=15,
                                color=CYAN,
                            ),
                            ft.Text(
                                titulo,
                                color=CYAN,
                                size=11,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                    ),
                    ft.Divider(
                        height=1,
                        color=CYAN_BORDER,
                    ),
                    *controles,
                ],
            ),
        )

    painel_esquerdo = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=8,
        controls=[
            criar_painel(
                "DEVICE",
                ft.Icons.SMARTPHONE,
                [
                    ft.Text(
                        "Bateria: 92%",
                        color=WHITE_70,
                        size=10,
                    ),
                    ft.Text(
                        "Memória: Estável",
                        color=WHITE_70,
                        size=10,
                    ),
                    ft.Text(
                        "Sistema: Android",
                        color=WHITE_70,
                        size=10,
                    ),
                ],
            ),
            criar_painel(
                "NOTIFICAÇÕES",
                ft.Icons.NOTIFICATIONS,
                [
                    ft.Text(
                        "E-mails: 3 novos",
                        color=WHITE_70,
                        size=10,
                    ),
                    ft.Text(
                        "Notícias: 5 novas",
                        color=WHITE_70,
                        size=10,
                    ),
                ],
            ),
        ],
    )

    painel_direito = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=8,
        controls=[
            criar_painel(
                "NETWORK",
                ft.Icons.WIFI,
                [
                    ft.Text(
                        "Rede: 5G",
                        color=WHITE_70,
                        size=10,
                    ),
                    ft.Text(
                        "Ping: 45 ms",
                        color=WHITE_70,
                        size=10,
                    ),
                    ft.Text(
                        "Backend: ONLINE",
                        color=WHITE_70,
                        size=10,
                    ),
                ],
            ),
            criar_painel(
                "SYSTEM",
                ft.Icons.MIC,
                [
                    ft.Text(
                        "Escuta: Ativa",
                        color=WHITE_70,
                        size=10,
                    ),
                    ft.Text(
                        "Mídia: Desconectada",
                        color=WHITE_70,
                        size=10,
                    ),
                ],
            ),
        ],
    )

    layout_paisagem = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15,
        controls=[
            painel_esquerdo,
            esfera,
            painel_direito,
        ],
    )

    layout_retrato = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
        controls=[
            texto_status,
            linha_popups_superior,
            esfera,
            linha_popups_inferior,
            seta_comando,
            painel_comando,
        ],
    )

    layout_paisagem_completo = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=8,
        controls=[
            layout_paisagem,
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        content=campo_comando,
                        width=300,
                    ),
                    botao_enviar,
                ],
            ),
            texto_chat,
        ],
    )

    layout_paisagem_completo.visible = False

    container_principal = ft.Container(
        expand=True,
        alignment=ft.Alignment.CENTER,
        content=ft.Stack(
            expand=True,
            alignment=ft.Alignment.CENTER,
            controls=[
                layout_retrato,
                layout_paisagem_completo,
            ],
        ),
    )

    page.add(container_principal)

    def atualizar_orientacao(e=None):
        largura = page.width
        altura = page.height

        if largura is None or altura is None:
            return

        if largura > altura:
            estado["orientacao"] = "landscape"
            layout_retrato.visible = False
            layout_paisagem_completo.visible = True
        else:
            estado["orientacao"] = "portrait"
            layout_retrato.visible = True
            layout_paisagem_completo.visible = False

        page.update()

    page.on_resized = atualizar_orientacao

    def verificar_backend():
        try:
            online = verificar_status_servidor()

            if online:
                texto_status.value = "S I S T E M A   O N L I N E"
                texto_status.color = CYAN
            else:
                texto_status.value = "S I S T E M A   O F F L I N E"
                texto_status.color = ft.Colors.RED_ACCENT_400

            page.update()

        except Exception:
            texto_status.value = "S I S T E M A   O F F L I N E"
            texto_status.color = ft.Colors.RED_ACCENT_400
            page.update()

    threading.Thread(
        target=verificar_backend,
        daemon=True,
    ).start()

    page.update()