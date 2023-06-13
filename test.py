"""
test.py
13. June 2023

<description>

Author:
Nilusink
"""
import customtkinter as ctk
import random


class BlackjackGame(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.attributes('-fullscreen', True)
        self.create_widgets()

    def create_widgets(self):
        self.Hit = ctk.CTkButton(self)
        self.Hit.pack()


game = BlackjackGame()
game.mainloop()
