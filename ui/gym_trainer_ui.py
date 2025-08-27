import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import mediapipe as mp

from utils import score_table
from types_of_exercise import TypeOfExercise
from database_manager import fetch_one, execute_query

def create_gym_trainer_frame(parent, get_username_callback, offline=False):
    GTframe = ctk.CTkFrame(parent, fg_color='gray14', width=700, height=620)
    
    session_rep_counters = { "pull-up": 0, "push-up": 0, "squat": 0, "walk": 0, "sit-up": 0 }
    
    def start_exercise(selected_exercise):
        mp_pose = mp.solutions.pose
        video_path = f"exercise_media/videos/{selected_exercise}.mp4"
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            messagebox.showerror("Video Error", f"Could not open video file for {selected_exercise}.")
            return

        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            counter = 0
            status = True
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame = cv2.resize(frame, (800, 480), interpolation=cv2.INTER_AREA)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(frame)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                try:
                    landmarks = results.pose_landmarks.landmark
                    counter, status = TypeOfExercise(landmarks).calculate_exercise(selected_exercise, counter, status)
                except:
                    pass

                score_table(selected_exercise, frame, counter, status)
                cv2.imshow('Exercise Feed', frame)
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
            
            session_rep_counters[selected_exercise] += counter
            
            if not offline:
                update_exercise_in_db(selected_exercise, counter)
            
            update_ui_labels()
            
        cap.release()
        cv2.destroyAllWindows()

    def update_exercise_in_db(exercise_name, reps_done):
        username = get_username_callback()
        db_column_map = {"pull-up": "pullups", "push-up": "pushups", "squat": "squats", "walk": "walking", "sit-up": "situps"}
        column = db_column_map.get(exercise_name)
        
        if not column: return
        
        # Use GREATEST(0, ...) to prevent reps from going below zero
        query = f"UPDATE exercises SET {column} = GREATEST(0, {column} - %s) WHERE username = %s"
        values = (reps_done, username)
        execute_query(query, values)

    def update_ui_labels():
        if offline:
            pullup_counter.configure(text=f"Session Reps: {session_rep_counters['pull-up']}")
            pushup_counter.configure(text=f"Session Reps: {session_rep_counters['push-up']}")
            squat_counter.configure(text=f"Session Reps: {session_rep_counters['squat']}")
            walk_counter.configure(text=f"Session Reps: {session_rep_counters['walk']}")
            situp_counter.configure(text=f"Session Reps: {session_rep_counters['sit-up']}")
        else:
            username = get_username_callback()
            user_exercises = fetch_one("SELECT pullups, pushups, squats, walking, situps FROM exercises WHERE username = %s", (username,))
            sets = user_exercises if user_exercises else [0, 0, 0, 0, 0]
            
            pullup_counter.configure(text=f"Remaining: {sets[0]}")
            pushup_counter.configure(text=f"Remaining: {sets[1]}")
            squat_counter.configure(text=f"Remaining: {sets[2]}")
            walk_counter.configure(text=f"Remaining: {sets[3]}")
            situp_counter.configure(text=f"Remaining: {sets[4]}")

    GymTitle = ctk.CTkLabel(GTframe, text="Gym Trainer", font=('Helvetica', 30, 'bold'), text_color='#425fe4')
    GymTitle.grid(row=0, column=0, columnspan=2, padx=100, pady=(10, 60))

    exercise_images = {
        "pull-up": "exercise_media/images/pull-up.jpg", "push-up": "exercise_media/images/push-up.jpg",
        "squat": "exercise_media/images/squat.jpg", "walk": "exercise_media/images/walk.jpg",
        "sit-up": "exercise_media/images/sit-up.jpg",
    }
    
    pullup_counter = ctk.CTkLabel(GTframe, text="")
    pullup_counter.grid(row=1, column=0)
    pushup_counter = ctk.CTkLabel(GTframe, text="")
    pushup_counter.grid(row=1, column=1)
    squat_counter = ctk.CTkLabel(GTframe, text="")
    squat_counter.grid(row=3, column=0)
    walk_counter = ctk.CTkLabel(GTframe, text="")
    walk_counter.grid(row=3, column=1)
    situp_counter = ctk.CTkLabel(GTframe, text="")
    situp_counter.grid(row=5, column=0)

    positions = [(2, 0), (2, 1), (4, 0), (4, 1), (6, 0)]
    for (exercise_name, image_path), pos in zip(exercise_images.items(), positions):
        try:
            img = Image.open(image_path).resize((120, 120))
            photo = ImageTk.PhotoImage(img)
            btn = ctk.CTkButton(GTframe, image=photo, text=exercise_name.title(), compound="top",
                                command=lambda e=exercise_name: start_exercise(e), text_color='white',
                                fg_color='gray14', corner_radius=10, hover_color='#425fe4')
            btn.image = photo
            btn.grid(row=pos[0], column=pos[1], padx=100, pady=(0, 20))
        except FileNotFoundError:
            # If an image is missing, place a text button instead
            btn = ctk.CTkButton(GTframe, text=f"{exercise_name.title()}\n(Image not found)",
                                command=lambda e=exercise_name: start_exercise(e),
                                fg_color='gray14', corner_radius=10, hover_color='#425fe4')
            btn.grid(row=pos[0], column=pos[1], padx=100, pady=(0, 20))

    update_ui_labels()
    
    GTframe.update_counters = update_ui_labels
    
    return GTframe