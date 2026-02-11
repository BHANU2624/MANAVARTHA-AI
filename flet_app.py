import flet as ft
import requests
import json

API_URL = "http://127.0.0.1:8000/search"

def main(page: ft.Page):
    page.title = "Telugu News AI"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.window_width = 400
    page.window_height = 800
    
    # Colors
    primary_color = "#1f6feb"
    user_bg = "#1f6feb"
    bot_bg = "#033a16"
    bot_text = "#d1ffd6"

    # Message List
    chat_view = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    def send_message(e):
        user_message = message_input.value
        if not user_message:
            return

        # Add User Message
        chat_view.controls.append(
            ft.Row([
                ft.Container(
                    content=ft.Text(user_message, color="white", size=16),
                    bgcolor=user_bg,
                    padding=10,
                    border_radius=ft.border_radius.only(top_left=15, top_right=15, bottom_left=15),
                    width=300
                )
            ], alignment=ft.MainAxisAlignment.END)
        )
        
        message_input.value = ""
        page.update()

        # Call API
        try:
            # Show typing...
            typing_dots = ft.Row([ft.Text("Typing...", italic=True, size=12)], alignment=ft.MainAxisAlignment.START)
            chat_view.controls.append(typing_dots)
            page.update()
            
            r = requests.get(API_URL, params={"query": user_message})
            
            # Remove typing
            chat_view.controls.pop()
            
            if r.status_code == 200:
                answer = r.json().get("answer", "No answer found.")
            else:
                answer = f"Error: {r.status_code}"
            
            # Add Bot Message
            chat_view.controls.append(
                ft.Row([
                    ft.Container(
                        content=ft.Text(answer, color=bot_text, size=16),
                        bgcolor=bot_bg,
                        padding=10,
                        border_radius=ft.border_radius.only(top_left=15, top_right=15, bottom_right=15),
                        width=300
                    )
                ], alignment=ft.MainAxisAlignment.START)
            )

        except Exception as ex:
            chat_view.controls.append(ft.Text(f"Error: {ex}", color="red"))
        
        page.update()

    # Input Area
    message_input = ft.TextField(
        hint_text="Ask a question...",
        expand=True,
        border_radius=20,
        on_submit=send_message
    )
    
    send_btn = ft.IconButton(
        icon="send",
        icon_color="white",
        bgcolor=primary_color,
        on_click=send_message
    )

    input_row = ft.Row([
        message_input,
        send_btn
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    # Header
    header = ft.Container(
        content=ft.Row([
            ft.Icon("newspaper", color="white"),
            ft.Text("Telugu News AI", size=20, weight="bold", color="white")
        ]),
        bgcolor="#161b22",
        padding=15,
        border_radius=10
    )

    page.add(
        header,
        ft.Divider(height=10, color="transparent"),
        chat_view,
        ft.Divider(height=10, color="transparent"),
        input_row
    )

ft.app(target=main)
