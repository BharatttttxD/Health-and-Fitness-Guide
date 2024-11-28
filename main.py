import json
import datetime
from enum import Enum
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import matplotlib.pyplot as plt

# Enum and classes from the first script
class FitnessStatus(Enum):
    UNDERWEIGHT = "Underweight"
    NORMAL = "Normal"
    OVERWEIGHT = "Overweight"
    OBESE = "Obese"

class User:
    def __init__(self, weight, height):
        self.weight = weight
        self.height = height
        self.bmi = self.calculate_bmi()
        self.fitness_status = self.determine_fitness_status()

    def calculate_bmi(self):
        return round(self.weight / (self.height ** 2), 2)

    def determine_fitness_status(self):
        if self.bmi < 18.5:
            return FitnessStatus.UNDERWEIGHT
        elif 18.5 <= self.bmi < 25:
            return FitnessStatus.NORMAL
        elif 25 <= self.bmi < 30:
            return FitnessStatus.OVERWEIGHT
        else:
            return FitnessStatus.OBESE

class DietPlan:
    def __init__(self, filename):
        with open(filename) as f:
            self.plans = json.load(f)

    def get_plan(self, user, plan_type):
        plan_types = {"1": "weight_loss", "2": "weight_gain", "3": "healthy"}
        return self.plans[user.fitness_status.value][plan_types[plan_type]]

# Utility functions
def log_data(file, data):
    with open(file, 'a') as f:
        f.write(data + '\n')

def display_message(title, message):
    messagebox.showinfo(title, message)

def record_weight(user):
    weight = simpledialog.askfloat("Record Weight", "Enter your weight in kgs:")
    if weight:
        user.weight = weight
        user.bmi = user.calculate_bmi()
        log_data('weight_log.txt', f'{datetime.date.today()}: {weight} kg')
        log_data('bmi_log.txt', f'{datetime.date.today()}: {user.bmi}')
        display_message("Success", "Weight and BMI recorded successfully")

def record_calories():
    calories = simpledialog.askinteger("Calorie Input", "Enter the number of calories consumed today:")
    if calories:
        log_data('calorie_log.txt', f'{datetime.date.today()}: {calories} kcal')
        display_message("Success", "Calories recorded successfully")

def record_exercise():
    ex = simpledialog.askstring("Exercise Log", "Enter the type of exercise:")
    duration = simpledialog.askinteger("Exercise Duration", "Enter the duration of exercise in minutes:")
    if ex and duration:
        log_data('exercise_log.txt', f'{datetime.date.today()}: {ex} for {duration} minutes')
        display_message("Success", "Exercise recorded successfully")

def view_data(file_name):
    try:
        with open(file_name, 'r') as f:
            data = f.read()
        text_window = tk.Toplevel()
        text_window.title("Recorded Data")
        text_area = scrolledtext.ScrolledText(text_window, wrap=tk.WORD, width=40, height=15)
        text_area.insert(tk.INSERT, data)
        text_area.configure(state='disabled')
        text_area.pack(padx=10, pady=10)
    except FileNotFoundError:
        display_message("Error", "No data recorded yet.")

# Plotting functions
def plot_data(file_name, y_label, title):
    dates = []
    values = []
    try:
        with open(file_name, 'r') as f:
            lines = f.readlines()
            for line in lines:
                date_str, value_str = line.split(": ")
                date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                value = float(value_str.split()[0])
                dates.append(date)
                values.append(value)

        # Create the plot
        plt.figure(figsize=(10, 6))
        plt.plot(dates, values, marker='o', color='blue', linestyle='-')
        plt.title(title, fontsize=15, fontweight='bold', fontstyle='italic', color="black")
        plt.xlabel('Date', fontsize=15, fontweight='bold', color='black')
        plt.ylabel(y_label, fontsize=15, fontweight='bold', color='black')
        plt.grid(True, linestyle='--', color='gray', alpha=0.7)
        plt.fill_between(dates, values, color='skyblue', alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    except FileNotFoundError:
        display_message("Error", f"No {title.lower()} log found. Please record some data first.")

# Main GUI function
def main_gui():
    root = tk.Tk()
    root.title("Health and Fitness Guide")

    # User input for weight and height
    weight = simpledialog.askfloat("User Weight", "Enter your weight (in kg):")
    height = simpledialog.askfloat("User Height", "Enter your height (in meters):")
    
    if weight and height:
        user = User(weight, height)
        diet_plan = DietPlan('diet_plans.json')

        display_message("User Info", f"Hello, User!\nYour BMI is: {user.bmi}\nStatus: {user.fitness_status.value}")

        def get_diet_plan():
            plan_choice = simpledialog.askstring("Diet Plan", "Choose a plan type:\n1. Weight Loss\n2. Weight Gain\n3. Healthy Diet")
            if plan_choice in ["1", "2", "3"]:
                plan = diet_plan.get_plan(user, plan_choice)
                display_message("Diet Plan", f"Recommended Plan: {plan}")
            else:
                display_message("Error", "Invalid choice. Please try again.")

        # Buttons for user actions
        tk.Button(root, text="Get a Diet Plan", command=get_diet_plan, bg="lightblue", fg="black").pack(pady=5)
        tk.Button(root, text="Record Weight and BMI", command=lambda: record_weight(user), bg="beige", fg="black").pack(pady=5)
        tk.Button(root, text="Record Calories Intake", command=record_calories, bg="beige", fg="black").pack(pady=5)
        tk.Button(root, text="Record Exercise", command=record_exercise, bg="beige", fg="black").pack(pady=5)
        tk.Button(root, text="View Weight Log", command=lambda: view_data('weight_log.txt'), bg="lightpink", fg="black").pack(pady=5)
        tk.Button(root, text="View BMI Log", command=lambda: view_data('bmi_log.txt'), bg="lightpink", fg="black").pack(pady=5)
        tk.Button(root, text="View Calorie Log", command=lambda: view_data('calorie_log.txt'), bg="lightpink", fg="black").pack(pady=5)
        tk.Button(root, text="View Exercise Log", command=lambda: view_data('exercise_log.txt'), bg="lightpink", fg="black").pack(pady=5)
        tk.Button(root, text="Plot Weight vs Date", command=lambda: plot_data('weight_log.txt', 'Weight (kg)', 'Weight'), bg="lightcyan", fg="black").pack(pady=5)
        tk.Button(root, text="Plot BMI vs Date", command=lambda: plot_data('bmi_log.txt', 'BMI', 'BMI'), bg="lightcyan", fg="black").pack(pady=5)
        tk.Button(root, text="Plot Calories vs Date", command=lambda: plot_data('calorie_log.txt', 'Calories (kcal)', 'Calories Intake'), bg="lightcyan", fg="black").pack(pady=5)
        tk.Button(root, text="Exit", command=root.destroy, bg="red", fg="black").pack(pady=5)

    else:
        display_message("Error", "User data incomplete. Please restart the application.")

    root.mainloop()

if __name__ == "__main__":
    main_gui()
