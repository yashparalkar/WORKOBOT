import customtkinter as ctk
from tkinter import ttk
from database_manager import fetch_one

def create_profile_frame(parent, get_username_callback, profile_image):
    Profile_frame = ctk.CTkFrame(parent, fg_color='gray14')
    
    username = get_username_callback()
    
    # Fetch user data
    user_details = fetch_one("SELECT name, email FROM users WHERE username = %s", (username,))
    user_stats = fetch_one("SELECT weight, height, age, gender, goal, activity_level FROM user_data WHERE username = %s", (username,))
    
    # --- UI Widgets ---
    Profile_Title = ctk.CTkLabel(Profile_frame, text="Your Profile", font=('Helvetica', 30, 'bold'), text_color='#425fe4')
    Profile_Title.pack(pady=30)

    profile_image_label = ctk.CTkLabel(Profile_frame, image=profile_image, text="")
    profile_image_label.pack()
    
    ctk.CTkLabel(Profile_frame, text=f"@{username}", font=('Helvetica', 16, 'italic')).pack(pady=(5, 20))

    # --- Details Display ---
    details_frame = ctk.CTkFrame(Profile_frame, fg_color="gray20", corner_radius=10)
    details_frame.pack(padx=20, pady=10, fill="x")

    ctk.CTkLabel(details_frame, text="Name:", font=('Helvetica', 14, 'bold')).grid(row=0, column=0, padx=10, pady=5, sticky="e")
    ctk.CTkLabel(details_frame, text=user_details[0] if user_details else 'N/A', font=('Helvetica', 14)).grid(row=0, column=1, padx=10, pady=5, sticky="w")
    
    ctk.CTkLabel(details_frame, text="Email:", font=('Helvetica', 14, 'bold')).grid(row=1, column=0, padx=10, pady=5, sticky="e")
    ctk.CTkLabel(details_frame, text=user_details[1] if user_details else 'N/A', font=('Helvetica', 14)).grid(row=1, column=1, padx=10, pady=5, sticky="w")

    if user_stats:
        stats_frame = ctk.CTkFrame(Profile_frame, fg_color="gray20", corner_radius=10)
        stats_frame.pack(padx=20, pady=10, fill="x")
        
        ctk.CTkLabel(stats_frame, text="Weight:", font=('Helvetica', 14, 'bold')).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        ctk.CTkLabel(stats_frame, text=f"{user_stats[0]} kg", font=('Helvetica', 14)).grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        ctk.CTkLabel(stats_frame, text="Height:", font=('Helvetica', 14, 'bold')).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        ctk.CTkLabel(stats_frame, text=f"{user_stats[1]} cm", font=('Helvetica', 14)).grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        ctk.CTkLabel(stats_frame, text="Age:", font=('Helvetica', 14, 'bold')).grid(row=0, column=2, padx=10, pady=5, sticky="e")
        ctk.CTkLabel(stats_frame, text=f"{user_stats[2]} years", font=('Helvetica', 14)).grid(row=0, column=3, padx=10, pady=5, sticky="w")
        
        ctk.CTkLabel(stats_frame, text="Gender:", font=('Helvetica', 14, 'bold')).grid(row=1, column=2, padx=10, pady=5, sticky="e")
        ctk.CTkLabel(stats_frame, text=f"{user_stats[3].title()}", font=('Helvetica', 14)).grid(row=1, column=3, padx=10, pady=5, sticky="w")
        
        ctk.CTkLabel(stats_frame, text="Goal:", font=('Helvetica', 14, 'bold')).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        ctk.CTkLabel(stats_frame, text=f"{user_stats[4].replace('_',' ').title()}", font=('Helvetica', 14)).grid(row=2, column=1, padx=10, pady=5, sticky="w")
        
        ctk.CTkLabel(stats_frame, text="Activity:", font=('Helvetica', 14, 'bold')).grid(row=2, column=2, padx=10, pady=5, sticky="e")
        ctk.CTkLabel(stats_frame, text=f"{user_stats[5].replace('_',' ').title()}", font=('Helvetica', 14)).grid(row=2, column=3, padx=10, pady=5, sticky="w")

    return Profile_frame