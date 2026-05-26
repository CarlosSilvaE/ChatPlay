import customtkinter as ctk
from tkinter import END

from chatbot import responder
from utils.text_utils import clear_text
from services.context_services import limpiar_contexto


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class ChatPlayApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("⚡ ChatPlay AI")
        self.geometry("1200x720")
        self.configure(fg_color="#050816")

        self.sidebar = ctk.CTkFrame(
            self,
            width=230,
            fg_color="#070B1A",
            corner_radius=0
        )
        self.sidebar.pack(side="left", fill="y")

        self.logo = ctk.CTkLabel(
            self.sidebar,
            text="⚡ ChatPlay",
            font=("Arial", 30, "bold"),
            text_color="#7F5AF0"
        )
        self.logo.pack(pady=35)

        self.status = ctk.CTkLabel(
            self.sidebar,
            text="AI Assistant\n● En línea",
            font=("Arial", 18),
            text_color="white"
        )
        self.status.pack(pady=10)

        self.menu_title = ctk.CTkLabel(
            self.sidebar,
            text="Chats",
            font=("Arial", 20, "bold"),
            text_color="#A78BFA"
        )
        self.menu_title.pack(pady=(40, 15))

        self.main = ctk.CTkFrame(
            self,
            fg_color="#050816"
        )
        self.main.pack(fill="both", expand=True)

        self.header = ctk.CTkLabel(
            self.main,
            text="ChatPlay AI ⚡",
            font=("Arial", 34, "bold"),
            text_color="#8B5CF6"
        )
        self.header.pack(pady=20)

        self.chatbox = ctk.CTkTextbox(
            self.main,
            fg_color="#0B1120",
            text_color="white",
            border_width=2,
            border_color="#7C3AED",
            corner_radius=20,
            font=("Consolas", 16)
        )
        self.chatbox.pack(
            padx=25,
            pady=10,
            fill="both",
            expand=True
        )

        self.chatbox.insert(
            END,
            "🤖 ChatPlay:\nHola, soy tu asistente de videojuegos ⚡\n\n"
        )

        self.bottom = ctk.CTkFrame(
            self.main,
            fg_color="#050816"
        )
        self.bottom.pack(fill="x", padx=20, pady=20)

        self.entry = ctk.CTkEntry(
            self.bottom,
            placeholder_text="Escribe tu mensaje...",
            height=55,
            corner_radius=18,
            fg_color="#111827",
            border_color="#7C3AED",
            border_width=2,
            text_color="white",
            font=("Arial", 16)
        )
        self.entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 15)
        )

        self.send_btn = ctk.CTkButton(
            self.bottom,
            text="Enviar ⚡",
            width=140,
            height=55,
            corner_radius=18,
            fg_color="#6D28D9",
            hover_color="#7C3AED",
            font=("Arial", 16, "bold"),
            command=self.send_message
        )
        self.send_btn.pack(side="right")

        self.bind("<Return>", lambda event: self.send_message())

    def send_message(self):
        user_msg = self.entry.get()

        if user_msg.strip() == "":
            return

        self.chatbox.insert(
            END,
            f"\n🧑 Tú:\n{user_msg}\n"
        )

        if clear_text(user_msg) == "salir":
            limpiar_contexto()
            response = "¡Hasta luego!"
        else:
            response, tag = responder(user_msg, devolver_tag=True)

        self.chatbox.insert(
            END,
            f"\n🤖 ChatPlay:\n{response}\n"
        )

        self.chatbox.see(END)
        self.entry.delete(0, END)

        if tag == "despedida":
            limpiar_contexto()
            self.after(1500, self.destroy)


if __name__ == "__main__":
    app = ChatPlayApp()
    app.mainloop()