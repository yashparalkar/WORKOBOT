import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk

# Import the status flag from the database manager
from database_manager import DB_CONNECTED

# Import UI modules
from ui.login_ui import create_login_screen
from ui.home_ui import create_home_frame
from ui.calorie_tracker_ui import create_calorie_tracker_frame
from ui.gym_trainer_ui import create_gym_trainer_frame
from ui.diet_recommender_ui import create_diet_recommender_frame
from ui.profile_ui import create_profile_frame

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.current_user = None
        self._set_appearance_mode('Dark')
        self.title("WORKOBOT")
        self.geometry("1024x640")
        self.iconbitmap('assets/logo1.ico')

        self.load_assets()
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        # Check database status to decide which mode to launch
        if DB_CONNECTED:
            self.show_login_screen()
        else:
            self.show_offline_mode()

    def load_assets(self):
        logo_image = Image.open("assets/WORKOBOT-removebg.png").resize((250, 250))
        self.logo_photo = ImageTk.PhotoImage(logo_image)
        self.logo_photo_b = ImageTk.PhotoImage(logo_image.resize((350, 350)))
        self.account_photo = ImageTk.PhotoImage(Image.open("assets/account1.png").resize((30, 30)))
        self.profile_photo = ImageTk.PhotoImage(Image.open("assets/account1.png").resize((100, 100)))

    def show_login_screen(self):
        self.entry_logo = ctk.CTkLabel(self.container, image=self.logo_photo_b, text='')
        self.entry_logo.place(relx=0.2, rely=0.5, anchor='center')
        create_login_screen(self.container, self.show_main_app)
    
    def show_offline_mode(self):
        """Builds a limited UI for when the database is unavailable."""
        self.current_user = "Offline User"
        self.create_nav_frame(offline=True) # Pass offline flag

        # Create all frames, as some are now functional offline
        self.frames = {}
        self.frames["Home"] = create_home_frame(self.container)
        self.frames["Calorie Tracker"] = create_calorie_tracker_frame(self.container)
        self.frames["Gym Trainer"] = create_gym_trainer_frame(self.container, self.get_current_user, offline=True)
        self.frames["Diet Recommender"] = create_diet_recommender_frame(self.container, self.get_current_user, offline=True)
        
        # Add a prominent offline message to the home screen
        offline_label = ctk.CTkLabel(self.frames["Home"], 
                                     text="⚠️ Database connection failed. Running in offline mode.",
                                     font=("Helvetica", 16, "bold"), text_color="orange")
        offline_label.place(relx=0.5, rely=0.05, anchor="center")

        self.navigate_to("Home") # Default to home page

    def show_main_app(self, username):
        """Hides the login screen and builds the main application interface."""
        self.current_user = username
        self.entry_logo.place_forget()
        
        self.create_nav_frame()

        self.frames = {}
        self.frames["Home"] = create_home_frame(self.container)
        self.frames["Calorie Tracker"] = create_calorie_tracker_frame(self.container)
        self.frames["Gym Trainer"] = create_gym_trainer_frame(self.container, self.get_current_user, offline=False)
        self.frames["Diet Recommender"] = create_diet_recommender_frame(self.container, self.get_current_user, offline=False)
        self.frames["Profile"] = create_profile_frame(self.container, self.get_current_user, self.profile_photo)
        
        self.navigate_to("Home")

    def create_nav_frame(self, offline=False):
        """Creates the side navigation bar, disabling buttons based on mode."""
        self.nav_frame = ctk.CTkFrame(self, fg_color='black', width=300, corner_radius=0)
        self.nav_frame.place(x=0, y=0, relheight=1.0)
        
        ctk.CTkLabel(self.nav_frame, image=self.logo_photo, text='').place(x=25, y=10)
        font = ("Arial", 18)
        
        self.nav_buttons = {
            "Home": ctk.CTkButton(self.nav_frame, text="Home", font=font, width=290, height=35, corner_radius=0, command=lambda: self.navigate_to("Home")),
            "Diet Recommender": ctk.CTkButton(self.nav_frame, text="Diet Recommender", font=font, width=290, height=35, corner_radius=0, command=lambda: self.navigate_to("Diet Recommender")),
            "Calorie Tracker": ctk.CTkButton(self.nav_frame, text="Calorie Tracker", font=font, width=290, height=35, corner_radius=0, command=lambda: self.navigate_to("Calorie Tracker")),
            "Gym Trainer": ctk.CTkButton(self.nav_frame, text="Gym Trainer", font=font, width=290, height=35, corner_radius=0, command=lambda: self.navigate_to("Gym Trainer"))
        }
        
        y_pos = 270
        for name, btn in self.nav_buttons.items():
            btn.place(x=5, y=y_pos)
            y_pos += 50
        
        self.account_btn = ctk.CTkButton(self.nav_frame, text=self.current_user, image=self.account_photo, fg_color='gray', font=('Helvetica', 16, 'bold'), command=lambda: self.navigate_to("Profile"))
        self.account_btn.place(relx=0.5, y=590, anchor='center')

        # Only disable the Profile button in offline mode
        if offline:
            self.account_btn.configure(state="disabled")

    def navigate_to(self, page_name):
        for btn in self.nav_buttons.values():
            btn.configure(fg_color="black", hover_color="#425fe4")
        
        for frame in self.frames.values():
            if frame:
                frame.place_forget()

        if page_name in self.frames and self.frames[page_name]:
            frame = self.frames[page_name]
            frame.place(x=310, y=10)
            
            if page_name in self.nav_buttons:
                self.nav_buttons[page_name].configure(fg_color="#425fe4")
            
            if page_name == "Home" and hasattr(frame, 'start_animation'):
                frame.start_animation()
            elif page_name == "Gym Trainer" and hasattr(frame, 'update_counters'):
                frame.update_counters()

    def get_current_user(self):
        return self.current_user

if __name__ == "__main__":
    app = App()
    app.mainloop()