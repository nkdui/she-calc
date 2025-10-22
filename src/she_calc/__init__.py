from tkinter import E, EW, NSEW, W
from typing import Any, Optional, Tuple

from autosar_she import MemorySlot, ProtectionFlag, memory_update
from customtkinter import (
    CTk,
    CTkButton,
    CTkCheckBox,
    CTkComboBox,
    CTkFrame,
    CTkLabel,
    CTkTextbox,
)

PAD = 5


class InputProtFlg(CTkFrame):
    @property
    def value(self) -> ProtectionFlag:
        prot_flg = ProtectionFlag.NONE
        for checkbox in self._checkbox_flags:
            if checkbox.get():
                prot_flg |= ProtectionFlag[checkbox.cget("text")]
        return prot_flg

    def __init__(self, master: Any, **kwargs):
        super().__init__(master, **kwargs)
        self._title = CTkLabel(self, text="Protection Flag")
        self._title.grid(row=0, column=0, padx=PAD, pady=PAD, sticky=W)

        self._checkbox_flags = [
            CTkCheckBox(self, text=flag.name)
            for flag in ProtectionFlag
            if flag.name is not None
        ]

        for i, checkbox in enumerate(self._checkbox_flags):
            checkbox.grid(row=i + 1, column=0, padx=PAD, pady=PAD, sticky=W)


class InputMemSlot(CTkFrame):
    @property
    def value(self) -> Optional[MemorySlot]:
        selected = self._combobox_slot.get()
        return MemorySlot[selected] if selected != "" else None

    def __init__(self, master: Any, title: str, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure((0, 1), weight=1)

        self._title = CTkLabel(self, text=title)
        self._title.grid(row=0, column=0, padx=PAD, pady=PAD, sticky=W)

        self._combobox_slot = CTkComboBox(
            self, state="readonly", values=[slot.name for slot in MemorySlot], width=150
        )
        self._combobox_slot.grid(row=0, column=1, padx=PAD, pady=PAD, sticky=E)


class InputHex(CTkFrame):
    @property
    def value(self) -> bytes:
        return bytes.fromhex(self._combo_hex.get())

    def __init__(self, master: Any, title: str, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure((0, 1), weight=1)

        self._title = CTkLabel(self, text=title)
        self._title.grid(row=0, column=0, padx=PAD, pady=PAD, sticky=W)

        self._combo_hex = CTkComboBox(self, values=[""], width=300)
        self._combo_hex.bind("<FocusOut>", self.__save_combo_value)
        self._combo_hex.grid(row=0, column=1, padx=PAD, pady=PAD, sticky=E)

    def __save_combo_value(self, event) -> None:
        current_choice = self._combo_hex.get()
        values: list[str] = self._combo_hex.cget("values")
        if current_choice not in values:
            values.append(current_choice)
            self._combo_hex.configure(values=values)


class InputCounter(CTkFrame):
    def __init__(self, master: Any, title: str, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure((0, 1), weight=1)

        self._title = CTkLabel(self, text=title)
        self._title.grid(row=0, column=0, padx=PAD, pady=PAD, sticky=W)


class InputGroup(CTkFrame):
    @property
    def uid(self) -> bytes:
        return self._input_uid.value

    @property
    def authid(self) -> Optional[MemorySlot]:
        return self._input_authid.value

    @property
    def key_authid(self) -> bytes:
        return self._input_key_authid.value

    @property
    def id(self) -> Optional[MemorySlot]:
        return self._input_id.value

    @property
    def key_id(self) -> bytes:
        return self._input_key_id.value

    @property
    def protflg(self) -> ProtectionFlag:
        return self._input_protflg.value

    def __init__(self, master: Any, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure(0, weight=1)

        self._title = CTkLabel(self, text="Configurations")
        self._title.grid(row=0, column=0, padx=PAD, pady=PAD, sticky=EW)

        self._input_uid = InputHex(self, "UID")
        self._input_uid.grid(row=1, column=0, padx=PAD, pady=PAD, sticky=EW)

        self._input_authid = InputMemSlot(self, "Auth ID")
        self._input_authid.grid(row=2, column=0, padx=PAD, pady=PAD, sticky=EW)

        self._input_key_authid = InputHex(self, "Key (Auth ID)")
        self._input_key_authid.grid(row=3, column=0, padx=PAD, pady=PAD, sticky=EW)

        self._input_id = InputMemSlot(self, "ID")
        self._input_id.grid(row=4, column=0, padx=PAD, pady=PAD, sticky=EW)

        self._input_key_id = InputHex(self, "Key (ID)")
        self._input_key_id.grid(row=5, column=0, padx=PAD, pady=PAD, sticky=EW)

        self._input_protflg = InputProtFlg(self)
        self._input_protflg.grid(row=6, column=0, padx=PAD, pady=PAD, sticky=EW)


class OutputGroup(CTkFrame):
    @property
    def text(self) -> str:
        return self._textbox_results.get("0.0", "end")

    @text.setter
    def text(self, value: str) -> None:
        self._textbox_results.configure(state="normal")
        self._textbox_results.delete("0.0", "end")
        self._textbox_results.insert("0.0", value)
        self._textbox_results.configure(state="disabled")

    def __init__(self, master: Any, **kwargs):
        super().__init__(master, **kwargs)
        self._title = CTkLabel(self, text="Results")
        self._title.grid(row=0, column=0, padx=PAD, pady=PAD, sticky=EW)

        self._textbox_results = CTkTextbox(self, width=500)
        self._textbox_results.grid(row=1, column=0, padx=PAD, pady=PAD, sticky=NSEW)
        self.text = "Results will be displayed here."


class App(CTk):
    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.title("SHE Calculator")
        self.resizable(False, False)

        self.group_input = InputGroup(self)
        self.group_input.grid(row=0, column=0, padx=PAD, pady=PAD, sticky=NSEW)

        self.group_output = OutputGroup(self)
        self.group_output.grid(row=0, column=1, padx=PAD, pady=PAD, sticky=NSEW)

        self.button_calc = CTkButton(self, text="Calculate", command=self.__calcuate)

        self.button_calc.grid(
            row=1, column=0, padx=PAD, pady=PAD, sticky=EW, columnspan=2
        )

    def __calcuate(self):
        self.group_output.text = f"""UID: {self.group_input.uid.hex()}
Auth ID: {self.group_input.authid.__repr__()}
Key (Auth ID): {self.group_input.key_authid.hex()}
ID: {self.group_input.id.__repr__()}
Key (ID): {self.group_input.key_id.hex()}
ProtFlg: {self.group_input.protflg.__repr__()}
"""


def main():
    App().mainloop()
