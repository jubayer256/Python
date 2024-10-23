import tkinter as tk
from tkinter import messagebox

def calculate_bmi():
    try:
        weight = float(entry_weight.get())
        feet = float(entry_feet.get())
        inches = float(entry_inches.get())
        height_meters = ((feet * 12) + inches) * 0.0254
        bmi = weight / (height_meters * height_meters)
        label_result['text'] = f'BMI: {bmi:.2f}'
        if bmi < 18.5:
            messagebox.showinfo("Result", "You are underweight.")
        elif 18.5 <= bmi < 24.9:
            messagebox.showinfo("Result", "You have a normal weight.")
        elif 25 <= bmi < 29.9:
            messagebox.showinfo("Result", "You are overweight.")
        else:
            messagebox.showinfo("Result", "You are obese.")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers.")

window = tk.Tk()
window.title("BMI Calculator")

label_weight = tk.Label(window, text="Weight (kg):")
label_weight.pack()
entry_weight = tk.Entry(window)
entry_weight.pack()

label_feet = tk.Label(window, text="Height (feet):")
label_feet.pack()
entry_feet = tk.Entry(window)
entry_feet.pack()

label_inches = tk.Label(window, text="Height (inches):")
label_inches.pack()
entry_inches = tk.Entry(window)
entry_inches.pack()

button_calculate = tk.Button(window, text="Calculate BMI", command=calculate_bmi)
button_calculate.pack()

label_result = tk.Label(window, text="BMI: ")
label_result.pack()

window.mainloop()
