import flet as ft
from Views.mobile_view import interface_mobile

if __name__ == "__main__":
    ft.run(interface_mobile, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=8550)