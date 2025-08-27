import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import pandas as pd

def create_calorie_tracker_frame(parent):
    # --- Data Loading ---
    try:
        md = pd.read_csv('data/nutrients.csv')
        md['Calories'] = pd.to_numeric(md['Calories'], errors='coerce')
        md['Grams'] = pd.to_numeric(md['Grams'], errors='coerce')
        md = md.dropna(subset=['Calories', 'Grams'])
        food_names = md['Food'].tolist()
    except FileNotFoundError:
        messagebox.showerror("Error", "nutrients.csv not found in the 'data' folder.")
        return ctk.CTkFrame(parent) # Return an empty frame on error

    CTframe = ctk.CTkFrame(parent, fg_color='gray14')

    # --- Helper Functions (nested inside to avoid global scope issues) ---
    def calculate_calories(food_name, portion_grams):
        food_row = md[md['Food'] == food_name]
        if not food_row.empty:
            calories_per_gram = food_row['Calories'].values[0] / food_row['Grams'].values[0]
            total_calories = calories_per_gram * portion_grams
            return round(total_calories, 2)
        return None

    def update_food_suggestion(event):
        user_input = combo_food.get().lower()
        suggestions = [food for food in food_names if food.lower().startswith(user_input)]
        combo_food['values'] = suggestions

    def fetch_nutrition(food_name, portion_grams):
        food_row = md[md['Food'] == food_name]
        if not food_row.empty:
            nutritional_facts = f"Nutritional Facts for {food_name}:\n"
            attributes = ['Calories', 'Protein', 'Fat', 'Sat.Fat', 'Fiber', 'Carbs']
            for attr in attributes:
                nutritional_facts += f"{attr}: {food_row[attr].values[0]}\n"
            total_cals = calculate_calories(food_name, portion_grams)
            nutritional_facts += f"Total Calories for {portion_grams}g: {total_cals}"
            return nutritional_facts
        return 'Food not found'

    def get_nutrition():
        selected_food = combo_food.get()
        try:
            portion_grams = float(entry_portion.get())
            nutritional_facts = fetch_nutrition(selected_food, portion_grams)
            label_result.configure(text=nutritional_facts)
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid number for grams.")
    
    total_calories = 0.0
    def add_to_table():
        nonlocal total_calories
        selected_food = combo_food.get()
        try:
            portion_grams = float(entry_portion.get())
            calories = calculate_calories(selected_food, portion_grams)

            if calories is not None:
                table.insert('', 'end', values=(selected_food, portion_grams, calories))
                total_calories += calories
                calorie_counter_label.configure(text=f"Total Calories: {round(total_calories, 2)}")
            else:
                messagebox.showwarning("Food not found", "The selected food item was not found.")
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid number for grams.")
    
    # --- UI Widgets ---
    heading_label = ctk.CTkLabel(CTframe, text="Calorie Tracker", font=('Helvetica', 30, 'bold'), text_color='#425fe4')
    heading_label.pack(pady=(10, 50))
    
    top_frame = ctk.CTkFrame(CTframe, fg_color='gray14')
    top_frame.pack(side=tk.TOP, padx=(90, 0), pady=10, fill=tk.BOTH, expand=True)

    bottom_frame = ctk.CTkFrame(CTframe, fg_color='gray14')
    bottom_frame.pack(side=tk.BOTTOM, padx=(30,0), pady=10, fill=tk.BOTH, expand=True)

    label_font = ('Helvetica', 13)
    btn_font = ('Helvetica', 17)
    
    ctk.CTkLabel(top_frame, text="Select Food:", font=label_font).grid(row=0, column=0, padx=10, pady=5)
    combo_food = ttk.Combobox(top_frame, values=food_names, width=20, font=("Helvetica", 13))
    combo_food.grid(row=0, column=1, padx=10, pady=5)
    combo_food.bind('<KeyRelease>', update_food_suggestion)

    ctk.CTkLabel(top_frame, text="Enter Portion (grams):", font=label_font).grid(row=1, column=0, padx=10, pady=5)
    entry_portion = ctk.CTkEntry(top_frame)
    entry_portion.grid(row=1, column=1, padx=10, pady=5)

    ctk.CTkButton(top_frame, text="Get Nutrition Facts", command=get_nutrition, corner_radius=20, fg_color='#425fe4', font=btn_font).grid(row=2, column=0, padx=5, pady=20)
    ctk.CTkButton(top_frame, text="Add to Table", command=add_to_table, corner_radius=20, fg_color='#425fe4', font=btn_font).grid(row=2, column=1, padx=5, pady=20)

    label_result = ctk.CTkLabel(top_frame, text="", anchor='w', justify='left')
    label_result.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

    table = ttk.Treeview(bottom_frame, columns=('Food', 'Portion (grams)', 'Calories'), show='headings')
    table.heading('Food', text='Food')
    table.heading('Portion (grams)', text='Portion (grams)')
    table.heading('Calories', text='Calories')
    table.pack(fill=tk.BOTH, expand=True)

    calorie_counter_label = ctk.CTkLabel(bottom_frame, text=f"Total Calories: {total_calories}")
    calorie_counter_label.pack(pady=10)

    return CTframe