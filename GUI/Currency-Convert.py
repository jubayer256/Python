from tkinter import *
from tkinter.ttk import Combobox


def convert_currency():
    amount = float(entry.get())
    from_currency = from_currency_combobox.get()
    to_currency = to_currency_combobox.get()
    currency_value = {"USD_BDT": 119.72, "USD_POUND": 0.77, "USD_AED": 3.67, "USD_USD": 1}
    temp = "USD_" + from_currency
    temp2 = (1 / currency_value[temp]) * amount

    st = "USD_" + to_currency
    ans = temp2 * currency_value[st]
    result_label.config(text="Result:{}".format(ans))


root = Tk()
root.title("Currency")
root.geometry("300x150")

entry_label = Label(root, text="Amount:")
entry_label.grid(column=0, row=0)
entry = Entry(root)
entry.grid(column=1, row=0)

from_currency_label = Label(root, text="From Currency:")
from_currency_label.grid(column=0, row=1)
from_currency_combobox = Combobox(root, values=["USD", "POUND", "AED", "BDT"])
from_currency_combobox.grid(column=1, row=1)
from_currency_combobox.current(0)

to_currency_label = Label(root, text="To Currency:")
to_currency_label.grid(column=0, row=2)
to_currency_combobox =  Combobox(root, values=["USD", "POUND", "AED", "BDT"])
to_currency_combobox.grid(column=1, row=2)
to_currency_combobox.current(3)

convert_button = Button(root, text="Convert", command=convert_currency)
convert_button.grid(column=0, row=3, columnspan=2)

result_label = Label(root, text="Result:")
result_label.grid(column=0, row=4, columnspan=2)

root.mainloop()
