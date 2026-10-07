import flet as ft
import flet.canvas as cv

CYAN = ft.Colors.CYAN_ACCENT_400

FONTES = {
    "Rajdhani": "https://raw.githubusercontent.com/google/fonts/main/ofl/rajdhani/Rajdhani-SemiBold.ttf",
    "ShareTechMono": "https://raw.githubusercontent.com/google/fonts/main/ofl/sharetechmono/ShareTechMono-Regular.ttf",
}


def aplicar_fontes(page: ft.Page):
    page.fonts = FONTES
    page.theme = ft.Theme(font_family="Rajdhani")


def _canto(x, y, sx, sy, tam, paint):
    # Desenha um "L": segue pela borda e vira pro lado
    return cv.Path(
        [
            cv.Path.MoveTo(x=x, y=y + sy * tam),
            cv.Path.LineTo(x=x, y=y),
            cv.Path.LineTo(x=x + sx * tam, y=y),
        ],
        paint=paint,
    )


def painel_com_cantos(painel, largura, altura, tam=14, cor=CYAN, espessura=2):
    """Marcas angulares nos 4 cantos de um painel de tamanho fixo.
    O painel precisa ter o mesmo width/height passados aqui."""
    paint = ft.Paint(
        color=cor, stroke_width=espessura, style=ft.PaintingStyle.STROKE
    )
    m = espessura / 2
    x0, y0, x1, y1 = m, m, largura - m, altura - m
    cantos = cv.Canvas(
        [
            _canto(x0, y0, 1, 1, tam, paint),
            _canto(x1, y0, -1, 1, tam, paint),
            _canto(x0, y1, 1, -1, tam, paint),
            _canto(x1, y1, -1, -1, tam, paint),
        ],
        width=largura,
        height=altura,
    )
    # Canvas por baixo, pra não engolir os toques no painel
    return ft.Stack(width=largura, height=altura, controls=[cantos, painel])