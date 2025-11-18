from tkinter import EW, NSEW, E, W
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
    StringVar,
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
        self._combobox_slot.set(MemorySlot.SECRET_KEY.name)


class InputHex(CTkFrame):
    @property
    def value(self) -> bytes:
        current_choice = self._combo_hex.get()
        values: list[str] = self._combo_hex.cget("values")
        if current_choice not in values:
            values.append(current_choice)
            self._combo_hex.configure(values=values)
        return bytes.fromhex(current_choice)

    def __init__(self, master: Any, title: str, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure((0, 1), weight=1)

        self._title = CTkLabel(self, text=title)
        self._title.grid(row=0, column=0, padx=PAD, pady=PAD, sticky=W)

        self._combo_hex = CTkComboBox(self, values=[""], width=300)
        self._combo_hex.grid(row=0, column=1, padx=PAD, pady=PAD, sticky=E)


class IntCounter(CTkFrame):
    @property
    def value(self) -> int:
        return int(self._value.get())

    def __init__(self, master: Any, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure((0, 2), weight=1)
        self.columnconfigure(1, weight=2)

        self._value = StringVar(value="0")
        self._button_decr = CTkButton(
            self, text="-", width=30, command=self.__decrement
        )
        self._button_decr.grid(row=0, column=0, padx=PAD, pady=PAD, sticky=W)

        self._label_value = CTkLabel(self, textvariable=self._value, width=50)
        self._label_value.grid(row=0, column=1, padx=PAD, pady=PAD)

        self._button_incr = CTkButton(
            self, text="+", width=30, command=self.__increment
        )
        self._button_incr.grid(row=0, column=2, padx=PAD, pady=PAD, sticky=E)

    def __decrement(self):
        current_value = int(self._value.get())
        if current_value > 0:
            self._value.set(str(current_value - 1))

    def __increment(self):
        current_value = int(self._value.get())
        self._value.set(str(current_value + 1))


class InputCounter(CTkFrame):
    @property
    def value(self) -> int:
        return self._counter.value

    def __init__(self, master: Any, title: str, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure((0, 1), weight=1)

        self._title = CTkLabel(self, text=title)
        self._title.grid(row=0, column=0, padx=PAD, pady=PAD, sticky=W)

        self._counter = IntCounter(self)
        self._counter.grid(row=0, column=1, padx=PAD, pady=PAD, sticky=E)


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
    def c_id(self) -> int:
        return self._input_c_id.value

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

        self._input_c_id = InputCounter(self, "Counter (ID)")
        self._input_c_id.grid(row=6, column=0, padx=PAD, pady=PAD, sticky=EW)

        self._input_protflg = InputProtFlg(self)
        self._input_protflg.grid(row=7, column=0, padx=PAD, pady=PAD, sticky=EW)


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
        m12345 = memory_update(
            uid=self.group_input.uid,
            auth_id=self.group_input.authid,
            k_auth_id=self.group_input.key_authid,
            id_=self.group_input.id,
            k_id=self.group_input.key_id,
            c_id=self.group_input.c_id,
            f_id=self.group_input.protflg,
        )
        self.group_output.text = "\n".join(m.hex().capitalize() for m in m12345)


def main():
    App().mainloop()
