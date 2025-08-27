import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import pandas as pd
from database_manager import fetch_one, execute_query

def create_diet_recommender_frame(parent, get_username_callback, offline=False):
    DRframe = ctk.CTkFrame(parent, fg_color='gray14', width=700, height=620)
    
    try:
        food_df = pd.read_csv("data/Scaled_Nutrients.csv")
    except FileNotFoundError:
        messagebox.showerror("Error", "Scaled_Nutrients.csv not found in the 'data' folder.")
        return DRframe # Return empty frame

    def calculate_bmr_harris_benedict(weight, height, age, gender):
        if gender == 'male': return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        else: return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

    def calculate_daily_calories(bmr, activity_level, goal):
        activity_multipliers = {'sedentary': 1.2, 'lightly_active': 1.375, 'moderately_active': 1.55, 'very_active': 1.725, 'extra_active': 1.9}
        calorie_multiplier = activity_multipliers.get(activity_level, 1.2)
        
        goal_sets = {
            'maintenance': ([10, 30, 30, 100, 30], bmr * calorie_multiplier),
            'weight_loss': ([10, 30, 40, 300, 60], bmr * calorie_multiplier * 0.8),
            'weight_gain': ([20, 50, 40, 70, 20], bmr * calorie_multiplier * 1.2),
        }
        sets, daily_calories = goal_sets.get(goal, goal_sets['maintenance'])
        
        if not offline:
            username = get_username_callback()
            user_exists = fetch_one("SELECT * FROM exercises WHERE username = %s", (username,))
            if user_exists:
                query = "UPDATE exercises SET pullups=%s, pushups=%s, squats=%s, walking=%s, situps=%s WHERE username=%s"
                values = sets + [username]
            else:
                query = "INSERT INTO exercises (username, pullups, pushups, squats, walking, situps) VALUES (%s, %s, %s, %s, %s, %s)"
                values = [username] + sets
            execute_query(query, values)
        
        return daily_calories

    def recommend_diet(daily_calories, goal):
        for item in table.get_children():
            table.delete(item)

        total_calories, total_protein = 0, 0
        recommended_food = []
        food_df_sorted = food_df.sort_values(by='Protein', ascending=False)

        for _, row in food_df_sorted.iterrows():
            if len(recommended_food) >= 15: # Limit recommendations for display
                break
            if total_calories + row['Calories'] <= daily_calories:
                recommended_food.append((row['Food'], row['Calories'], row['Protein']))
                total_calories += row['Calories']
                total_protein += row['Protein']
        
        for food, calories, protein in recommended_food:
            table.insert("", "end", values=(food, f"{calories:.2f}", f"{protein:.2f}"))
        table.insert("", "end", values=("Total", f"{total_calories:.2f}", f"{total_protein:.2f}"))

    def calculate_and_display():
        try:
            weight = float(weight_entry.get())
            height = float(height_entry.get())
            age = int(age_entry.get())
            gender = gender_var.get()
            activity = activity_var.get()
            goal = goal_var.get()
        except ValueError:
            messagebox.showerror("Input Error", "Please ensure all fields are filled with valid numbers.")
            return

        if not offline:
            username = get_username_callback()
            user_exists = fetch_one("SELECT * FROM user_data WHERE username = %s", (username,))
            if user_exists:
                query = "UPDATE user_data SET weight=%s, height=%s, age=%s, gender=%s, activity_level=%s, goal=%s WHERE username=%s"
                values = (weight, height, age, gender, activity, goal, username)
            else:
                query = "INSERT INTO user_data (username, weight, height, age, gender, activity_level, goal) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                values = (username, weight, height, age, gender, activity, goal)
            execute_query(query, values)
        
        bmr = calculate_bmr_harris_benedict(weight, height, age, gender)
        daily_calories = calculate_daily_calories(bmr, activity, goal)
        
        result_label.configure(text=f"Estimated Daily Calorie Needs: {daily_calories:.2f} calories")
        recommend_diet(daily_calories, goal)
        
    heading_label = ctk.CTkLabel(DRframe, text="Diet Recommender", font=('Helvetica', 30, 'bold'), text_color='#425fe4')
    heading_label.pack(pady=(10, 20))

    input_frame = ctk.CTkFrame(DRframe, fg_color='gray14')
    input_frame.pack(padx=20, pady=5, fill="x")
    
    result_frame = ctk.CTkFrame(DRframe, fg_color='gray14')
    result_frame.pack(padx=20, pady=10, fill="both", expand=True)

    ctk.CTkLabel(input_frame, text="Weight (kg):").grid(row=0, column=0, padx=5, pady=5, sticky='w')
    weight_entry = ctk.CTkEntry(input_frame)
    weight_entry.grid(row=0, column=1, padx=5, pady=5)

    ctk.CTkLabel(input_frame, text="Height (cm):").grid(row=1, column=0, padx=5, pady=5, sticky='w')
    height_entry = ctk.CTkEntry(input_frame)
    height_entry.grid(row=1, column=1, padx=5, pady=5)
    
    ctk.CTkLabel(input_frame, text="Age:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
    age_entry = ctk.CTkEntry(input_frame)
    age_entry.grid(row=2, column=1, padx=5, pady=5)
    
    ctk.CTkLabel(input_frame, text="Gender:").grid(row=0, column=2, padx=5, pady=5, sticky='w')
    gender_var = tk.StringVar(value="male")
    ctk.CTkRadioButton(input_frame, text="Male", variable=gender_var, value="male").grid(row=0, column=3, sticky='w')
    ctk.CTkRadioButton(input_frame, text="Female", variable=gender_var, value="female").grid(row=0, column=4, sticky='w')

    ctk.CTkLabel(input_frame, text="Activity Level:").grid(row=1, column=2, padx=5, pady=5, sticky='w')
    activity_var = tk.StringVar(value="sedentary")
    activity_options = ["sedentary", "lightly_active", "moderately_active", "very_active", "extra_active"]
    ctk.CTkComboBox(input_frame, variable=activity_var, values=activity_options).grid(row=1, column=3, columnspan=2, padx=5, pady=5)
    
    ctk.CTkLabel(input_frame, text="Goal:").grid(row=2, column=2, padx=5, pady=5, sticky='w')
    goal_var = tk.StringVar(value="maintenance")
    goal_options = ["maintenance", "weight_loss", "weight_gain"]
    ctk.CTkComboBox(input_frame, variable=goal_var, values=goal_options).grid(row=2, column=3, columnspan=2, padx=5, pady=5)
    
    calculate_button = ctk.CTkButton(input_frame, text="Calculate & Recommend", command=calculate_and_display, fg_color='#425fe4', corner_radius=20)
    calculate_button.grid(row=3, column=0, columnspan=5, pady=20)
    
    result_label = ctk.CTkLabel(result_frame, text="", font=('Helvetica', 16, 'bold'))
    result_label.pack(pady=5)
    
    table = ttk.Treeview(result_frame, columns=("Food", "Calories", "Protein"), show="headings")
    table.heading("Food", text="Food")
    table.heading("Calories", text="Calories")
    table.heading("Protein", text="Protein")
    table.pack(fill="both", expand=True)

    return DRframe