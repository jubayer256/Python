from tkinter import *

def calculator():
    enter_weight = float(weight.get())
    enter_height_in_feet = float(height_feet.get())
    enter_height_in_inch = float(height_inch.get())
    """enter_meter = ((enter_height_in_feet * 12) + enter_height_in_inch) * 0.0254"""
    height_meter = ((0.30 * enter_height_in_feet) + (0.025 * enter_height_in_inch))
    bmi = enter_weight / (height_meter * height_meter)
    bmi = round(bmi,2)
    Label(window, text=bmi).grid(column=1, row=3)

window = Tk()
window.title("BMI Calculator")
window.geometry("250x100")

Label(window, text="Weight : ").grid(row=0, column=0)
weight = Entry(window, borderwidth=1, relief="solid")
weight.grid(row=0, column=1)

Label(window, text="Height(feet) : ").grid(row=1, column=0)
height_feet = Entry(window, borderwidth=1, relief="solid")
height_feet.grid(row=1, column=1)

Label(window, text="Height(inch) : ").grid(row=2, column=0)
height_inch = Entry(window, borderwidth=1, relief="solid")
height_inch.grid(row=2, column=1)

BMI = Button(window, text="BMI", width=10, command=calculator)
BMI.grid(column=0, row=3, pady=5)
window.mainloop()

