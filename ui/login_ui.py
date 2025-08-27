import customtkinter as ctk
from database_manager import fetch_one, execute_query

def create_login_screen(parent, show_main_app_callback):
    """Creates and displays the login and signup frames."""
    login_frame = ctk.CTkFrame(parent, corner_radius=15)
    signup_frame = ctk.CTkFrame(parent, corner_radius=15)

    title_font = ('Helvetica', 40, 'bold')
    font = ('Helvetica', 20, 'bold')

    # --- Login Frame Widgets ---
    login_frame.place(relx=0.6, rely=0.5, anchor='center')
    login_title = ctk.CTkLabel(login_frame, text="Login", font=title_font)
    login_title.grid(row=0, column=0, columnspan=2, pady=(50, 70), padx=100)
    username_label = ctk.CTkLabel(login_frame, text="Username:", font=font)
    username_label.grid(row=1, column=0, padx=(50, 10), pady=20, sticky="e")
    username_entry = ctk.CTkEntry(login_frame, font=font, width=200)
    username_entry.grid(row=1, column=1, padx=(10, 50), pady=10)
    password_label = ctk.CTkLabel(login_frame, text="Password:", font=font)
    password_label.grid(row=2, column=0, padx=(50, 10), pady=20, sticky="e")
    password_entry = ctk.CTkEntry(login_frame, show="*", font=font, width=200)
    password_entry.grid(row=2, column=1, padx=(10, 50), pady=10)

    # --- Signup Frame Widgets ---
    signup_title = ctk.CTkLabel(signup_frame, text="Sign Up", font=title_font)
    signup_title.grid(row=0, column=0, columnspan=2, pady=(50, 70), padx=100)
    signup_username_label = ctk.CTkLabel(signup_frame, text="Username:", font=font)
    signup_username_label.grid(row=1, column=0, padx=(50, 10), pady=20, sticky="e")
    signup_username_entry = ctk.CTkEntry(signup_frame, font=font, width=200)
    signup_username_entry.grid(row=1, column=1, padx=(10, 50), pady=10)
    signup_password_label = ctk.CTkLabel(signup_frame, text="Password:", font=font)
    signup_password_label.grid(row=2, column=0, padx=(50, 10), pady=20, sticky="e")
    signup_password_entry = ctk.CTkEntry(signup_frame, show="*", font=font, width=200)
    signup_password_entry.grid(row=2, column=1, padx=(10, 50), pady=10)
    signup_name_label = ctk.CTkLabel(signup_frame, text="Name:", font=font)
    signup_name_label.grid(row=3, column=0, padx=(50, 10), pady=20, sticky="e")
    signup_name_entry = ctk.CTkEntry(signup_frame, font=font, width=200)
    signup_name_entry.grid(row=3, column=1, padx=(10, 50), pady=10)
    signup_email_label = ctk.CTkLabel(signup_frame, text="Email:", font=font)
    signup_email_label.grid(row=4, column=0, padx=(50, 10), pady=20, sticky="e")
    signup_email_entry = ctk.CTkEntry(signup_frame, font=font, width=200)
    signup_email_entry.grid(row=4, column=1, padx=(10, 50), pady=10)

    # --- Helper Functions ---
    def switch_to_signup():
        login_frame.place_forget()
        signup_frame.place(relx=0.6, rely=0.5, anchor='center')

    def switch_to_login():
        signup_frame.place_forget()
        login_frame.place(relx=0.6, rely=0.5, anchor='center')

    def handle_login():
        username = username_entry.get()
        password = password_entry.get()
        user = fetch_one("SELECT * FROM users WHERE username = %s", (username,))
        if user and user[2] == password:
            print("Login successful!")
            login_frame.place_forget()
            show_main_app_callback(user[0]) # Call the callback function
        else:
            # Add some user feedback, e.g., a message box
            print("Incorrect username or password.")

    def handle_signup():
        username = signup_username_entry.get()
        password = signup_password_entry.get()
        name = signup_name_entry.get()
        email = signup_email_entry.get()
        if not all([username, password, name, email]):
             print("All fields are required.")
             return
        user = fetch_one("SELECT * FROM users WHERE username = %s", (username,))
        if user:
            print("Username already exists.")
        else:
            query = "INSERT INTO users (username, password, name, email) VALUES (%s, %s, %s, %s)"
            execute_query(query, (username, password, name, email))
            print("Signup successful! Please log in.")
            switch_to_login()

    # --- Buttons ---
    login_button = ctk.CTkButton(login_frame, text="Login", command=handle_login, font=font, corner_radius=20)
    login_button.grid(row=3, column=0, columnspan=2, pady=20)
    signup_button = ctk.CTkButton(login_frame, text="Signup", command=switch_to_signup, font=font, corner_radius=20)
    signup_button.grid(row=4, column=0, columnspan=2, pady=(20, 50))

    back_button = ctk.CTkButton(signup_frame, text="Back", command=switch_to_login, font=font, corner_radius=20)
    back_button.grid(row=5, column=0, pady=(20, 50))
    signup_submit_button = ctk.CTkButton(signup_frame, text="Submit", command=handle_signup, font=font, corner_radius=20)
    signup_submit_button.grid(row=5, column=1, pady=(20, 50))