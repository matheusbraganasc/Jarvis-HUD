import threading
import time
import flet as ft
import flet.canvas as cv
from Core.api_client import verificar_status_servidor, enviar_mensagem

CYAN = ft.Colors.CYAN_ACCENT_400
CYAN_CLARO = ft.Colors.CYAN_200
CYAN_ESCURO = ft.Colors.CYAN_900
CYAN_BORDA = ft.Colors.CYAN_700
BRANCO_70 = ft.Colors.WHITE_70

FONTE_TITULO = "Orbitron"
FONTE_DADOS = "ShareTechMono"


def _canto(x, y, sx, sy, tam, paint):
    return cv.Path(
        elements=[
            cv.Path.MoveTo(x=x, y=y + sy * tam),
            cv.Path.LineTo(x=x, y=y),
            cv.Path.LineTo(x=x + sx * tam, y=y),
        ],
        paint=paint,
    )


def _cantos_angulares(largura, altura, tam=12, espessura=2):
    paint = ft.Paint(
        color=CYAN, stroke_width=espessura, style=ft.PaintingStyle.STROKE
    )
    m = espessura / 2
    x0, y0, x1, y1 = m, m, largura - m, altura - m
    return cv.Canvas(
        width=largura,
        height=altura,
        shapes=[
            _canto(x0, y0, 1, 1, tam, paint),
            _canto(x1, y0, -1, 1, tam, paint),
            _canto(x0, y1, 1, -1, tam, paint),
            _canto(x1, y1, -1, -1, tam, paint),
        ],
    )


def interface_mobile(page: ft.Page):
    page.title = "J.A.R.V.I.S. HUD"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.Colors.BLACK
    page.padding = 10
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    page.fonts = {
        "Orbitron": "https://github.com/google/fonts/raw/main/ofl/orbitron/Orbitron%5Bwght%5D.ttf",
        "ShareTechMono": "https://github.com/google/fonts/raw/main/ofl/sharetechmono/ShareTechMono-Regular.ttf",
    }
    page.theme = ft.Theme(font_family=FONTE_TITULO)

    texto_status = ft.Text(
        "ESTABELECENDO CONEXÃO...",
        size=11,
        color=ft.Colors.YELLOW_ACCENT_400,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )

    texto_chat = ft.Text(
        "Aguardando ordem...",
        size=13,
        color=BRANCO_70,
        text_align=ft.TextAlign.CENTER,
        font_family=FONTE_DADOS,
    )

    campo_comando = ft.TextField(
        hint_text="Digite um comando para o JARVIS",
        width=290,
        height=45,
        color=ft.Colors.WHITE,
        border_color=CYAN,
        cursor_color=CYAN,
        text_size=12,
    )

    def enviar_comando(_=None):
        texto = campo_comando.value.strip() if campo_comando.value else ""
        if not texto:
            return

        texto_chat.value = "Processando..."
        texto_chat.color = CYAN
        page.update()

        resultado = enviar_mensagem(texto)

        if resultado.get("tipo") == "function_call":
            texto_chat.value = f"Ação solicitada: '{resultado['nome']}'."
        else:
            texto_chat.value = resultado.get("resposta", "Sem resposta do servidor.")

        texto_chat.color = BRANCO_70
        campo_comando.value = ""
        page.update()

    botao_enviar = ft.Button(content="Enviar", on_click=enviar_comando)

    texto_jarvis = ft.Text(
        "J.A.R.V.I.S.",
        size=11,
        weight=ft.FontWeight.BOLD,
        color=CYAN,
    )

    reator = ft.Container(
        width=120,
        height=120,
        shape=ft.BoxShape.CIRCLE,
        bgcolor=CYAN_ESCURO,
        border=ft.Border.all(2, CYAN),
        shadow=ft.BoxShadow(
            spread_radius=3,
            blur_radius=18,
            color=CYAN,
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
        color=CYAN_CLARO,
        value=0.4,
        rotate=ft.Rotate(angle=0),
    )

    anel_interno = ft.ProgressRing(
        width=150,
        height=150,
        stroke_width=3,
        color=CYAN,
        value=0.65,
        rotate=ft.Rotate(angle=0),
    )

    esfera = ft.Stack(
        width=180,
        height=180,
        alignment=ft.Alignment.CENTER,
        controls=[anel_externo, anel_interno, reator],
    )

    def animar_aneis():
        ang_externo = 0.0
        ang_interno = 0.0
        while True:
            ang_externo += 0.025
            ang_interno -= 0.045
            anel_externo.rotate = ft.Rotate(angle=ang_externo)
            anel_interno.rotate = ft.Rotate(angle=ang_interno)
            try:
                page.update()
            except Exception:
                break
            time.sleep(0.05)

    threading.Thread(target=animar_aneis, daemon=True).start()

    def linha_dado(texto, tam=9):
        return ft.Text(texto, color=BRANCO_70, size=tam, font_family=FONTE_DADOS)

    def criar_painel_tatico(titulo, controles, largura=155, altura=92):
        conteudo = ft.Container(
            width=largura,
            height=altura,
            padding=8,
            bgcolor="#0A00BCD4",
            content=ft.Column(
                spacing=4,
                controls=[
                    ft.Text(
                        titulo,
                        color=CYAN,
                        size=10,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Divider(height=1, color=CYAN_BORDA),
                    *controles,
                ],
            ),
        )
        return ft.Stack(
            width=largura,
            height=altura,
            controls=[conteudo, _cantos_angulares(largura, altura)],
        )

    def chip(icone, texto):
        return ft.Container(
            padding=6,
            border_radius=4,