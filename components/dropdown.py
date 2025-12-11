# components/dropdown.py
from tkinter import StringVar
from tkinter.ttk import Frame, Label, Combobox

from data.crypto import Crypto
from utils.event import Event


class CryptoDropdown(Frame):
    def __init__(self, master, crypto_list, **kwargs):
        super().__init__(master, **kwargs)

        self.on_selection = Event()
        self.selection = StringVar(value=crypto_list[0])
        self.current_symbol = self.selection.get()
        self.crypto = Crypto(self.current_symbol)

        Label(self, text="Select pair:").pack(side="left", padx=(0, 8))

        self.dropdown = Combobox(
            self,
            state="readonly",
            values=crypto_list,
            textvariable=self.selection,
            width=12,
        )
        self.dropdown.pack(side="left")
        self.dropdown.bind("<<ComboboxSelected>>", self.__handle_selection)

    def __handle_selection(self, _event=None):
        old_symbol = self.current_symbol
        new_symbol = self.selection.get()

        if new_symbol != old_symbol:
            if self.crypto:
                self.crypto.close_all()
            self.crypto = Crypto(new_symbol)
            self.current_symbol = new_symbol

        self.on_selection(old_symbol, new_symbol, self.crypto)
