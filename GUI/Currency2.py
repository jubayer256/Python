from tkinter import *
from tkinter.ttk import Combobox
import requests
from bs4 import BeautifulSoup


def convert_currency():
    amount = float(entry.get())
    from_currency = from_currency_combobox.get()
    to_currency = to_currency_combobox.get()
    response = requests.get("https://www.xe.com/currencyconverter/convert/?Amount={}&From={}&To={}".format(amount, from_currency, to_currency)).content.decode(
        'utf-8')
    beauty = BeautifulSoup(response, "html.parser")
    ans = beauty.find("p", attrs={"class": "sc-423c2a5f-1"}).text.split()[0]
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
from_currency_combobox = Combobox(root, values=["USD", "GBP", "AED", "BDT", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD", "AWG", "AZN", "BAM", "BBD", "BGN", "BHD", "BND", "BOB", "BRL", "BSD", "BTN", "BWP", "BYR", "BZD", "CAD", "CHF", "CLP", "CNY", "COP", "CRC", "CRK", "DKK", "DOP", "DZD", "EGP", "ETB", "EUR", "FJD", "GEL", "GHS", "GMD", "GTQ", "GYD", "HKD", "HNL", "HRK", "HUF", "IDR", "ILS", "INR", "ISK", "JEP", "JMD", "JOD", "JPY", "KES", "MYR"    ])
from_currency_combobox.grid(column=1, row=1)
from_currency_combobox.current(0)

to_currency_label = Label(root, text="To Currency:")
to_currency_label.grid(column=0, row=2)
to_currency_combobox =  Combobox(root, values=["USD", "GBP", "AED", "BDT", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD", "AWG", "AZN", "BAM", "BBD", "BGN", "BHD", "BND", "BOB", "BRL", "BSD", "BTN", "BWP", "BYR", "BZD", "CAD", "CHF", "CLP", "CNY", "COP", "CRC", "CRK", "DKK", "DOP", "DZD", "EGP", "ETB", "EUR", "FJD", "GEL", "GHS", "GMD", "GTQ", "GYD", "HKD", "HNL", "HRK", "HUF", "IDR", "ILS", "INR", "ISK", "JEP", "JMD", "JOD", "JPY", "KES", "MYR"    ])
to_currency_combobox.grid(column=1, row=2)
to_currency_combobox.current(3)

convert_button = Button(root, text="Convert", command=convert_currency)
convert_button.grid(column=0, row=3, columnspan=2)

result_label = Label(root, text="Result:")
result_label.grid(column=0, row=4, columnspan=2)

root.mainloop()