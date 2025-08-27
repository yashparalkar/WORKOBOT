import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk

def create_home_frame(parent):
    frame = ctk.CTkFrame(parent, fg_color='gray14', width=700, height=620)

    def animate_text():
        text = "Welcome to WORKOBOT, your ultimate fitness companion! Whether you're aiming to lose weight, gain muscle, or simply maintain a balanced lifestyle, WORKOBOT is here to support you every step of the way. Our Fitness App is designed to help you achieve your fitness goals. Head over to the Diet Recommender to give your physical goals and your activity level so we could recommend you the diet and a few exercises to achieve your desired physique."
        for i in range(len(text) + 1):
            display_text.set(text[:i])
            frame.update()
            frame.after(15)

    display_text = tk.StringVar()
    
    heading_frame = ctk.CTkFrame(frame, fg_color="gray14")
    heading_frame.pack(side=tk.TOP, padx=20, pady=10, fill=tk.BOTH)
    heading_label = ctk.CTkLabel(heading_frame, text="Welcome to Workobot", font=('Helvetica', 30, 'bold'), text_color='#425fe4', justify='center')
    heading_label.pack(pady=(0, 10))

    top_frame = ctk.CTkFrame(frame, fg_color='gray14')
    top_frame.pack(side=tk.TOP, padx=20, pady=10, fill=tk.BOTH, expand=True)

    bottom_frame = ctk.CTkFrame(frame, fg_color='gray14')
    bottom_frame.pack(side=tk.BOTTOM, padx=10, pady=10, fill=tk.BOTH, expand=True)

    image = Image.open('assets/TrainerImage.jpg')
    image = image.resize((600, 350))
    photo = ImageTk.PhotoImage(image)
    image_label = ctk.CTkLabel(top_frame, image=photo, text="", fg_color='gray14', anchor='w')
    image_label.image = photo
    image_label.pack()

    info_label = tk.Label(bottom_frame, textvariable=display_text, wraplength=600, font=("Helvetica", 15), background='gray14', anchor='w', foreground="#ffffff")
    info_label.pack()
    
    # Add a property to the frame to hold the animation function
    frame.start_animation = animate_text
    
    return frame