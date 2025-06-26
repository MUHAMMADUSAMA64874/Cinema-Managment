import tkinter as tk
import sqlite3
from tkinter import messagebox
from tkinter import simpledialog
import random
from tkinter import ttk
from queue import Queue
from PIL import ImageTk, Image
import time
from math import pi, sin, cos
import threading

# Set global font styles
font_title = ("Segoe UI", 20, "bold")
font_label = ("Segoe UI", 12)
font_entry = ("Segoe UI", 12)
font_button = ("Segoe UI", 12, "bold")

# Define modern color palette
primary_color = "#0D47A1"
secondary_colors = {
    "light_blue": "#2196F3",
    "orange": "#FF5722",
    "green": "#4CAF50",
    "gray": "#757575",
    "dark": "#121212",
    "light": "#F5F5F5",
    "accent": "#FF9800"
}

# Create databases
conn = sqlite3.connect("movies.db")
cursor = conn.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS movies (name TEXT, year INTEGER, rating REAL, genre TEXT)")
conn.commit()

# Create a dictionary to store movie data
movies_dict = {}

# Animation class for UI effects
class Animator:
    @staticmethod
    def fade_in(window, duration=0.3):
        alpha = 0.0
        window.attributes("-alpha", alpha)
        for i in range(1, 11):
            alpha = i/10
            window.attributes("-alpha", alpha)
            time.sleep(duration/10)
    
    @staticmethod
    def fade_out(window, duration=0.3):
        alpha = 1.0
        for i in range(10, 0, -1):
            alpha = i/10
            window.attributes("-alpha", alpha)
            time.sleep(duration/10)
        window.destroy()
    
    @staticmethod
    def pulse(widget, color1, color2, duration=1.0):
        def pulse_effect():
            for i in range(10):
                factor = abs(sin(i * pi / 10))
                r = int((1 - factor) * int(color1[1:3], 16) + factor * int(color2[1:3], 16))
                g = int((1 - factor) * int(color1[3:5], 16) + factor * int(color2[3:5], 16))
                b = int((1 - factor) * int(color1[5:7], 16) + factor * int(color2[5:7], 16))
                color = f"#{r:02x}{g:02x}{b:02x}"
                widget.config(bg=color)
                time.sleep(duration/20)
        threading.Thread(target=pulse_effect, daemon=True).start()

# Center window on screen
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

# Create modern styled button
def create_button(parent, text, command, bg=secondary_colors["accent"], fg="white", width=15):
    button = tk.Button(
        parent, 
        text=text, 
        command=command, 
        bg=bg, 
        fg=fg,
        font=font_button,
        relief="flat",
        bd=0,
        padx=15,
        pady=8,
        width=width,
        cursor="hand2",
        activebackground=secondary_colors["orange"],
        activeforeground="white"
    )
    return button

# Create modern styled entry
def create_entry(parent, width=25):
    entry = tk.Entry(
        parent,
        font=font_entry,
        bd=0,
        highlightthickness=1,
        highlightbackground="#cccccc",
        highlightcolor=primary_color,
        relief="flat",
        width=width
    )
    return entry

# Create modern styled label
def create_label(parent, text, font=font_label, fg="black", bg="white", anchor="w"):
    label = tk.Label(
        parent,
        text=text,
        font=font,
        fg=fg,
        bg=bg,
        anchor=anchor
    )
    return label

def create_user_table():
    conn = sqlite3.connect("UserDataBase.db")
    cursor = conn.cursor()

    # Create a table to store user data
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        Name TEXT,
                        Password TEXT
                    )''')
    conn.commit()
    conn.close()


def register_user():
    name = reg_username_entry.get()
    password = reg_password_entry.get()

    if name == "" or password == "":
        messagebox.showerror("Error", "Please fill in all fields.")
    else:
        conn = sqlite3.connect("UserDataBase.db")
        cursor = conn.cursor()

        try:
            # Insert user data into the database
            cursor.execute("INSERT INTO users (Name, Password) VALUES (?, ?)",
                           (name, password))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful.")
            clear_signup_entries()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists.")

        conn.close()


def login_user():
    name = login_username_entry.get()
    password = login_password_entry.get()

    if name == "" or password == "":
        messagebox.showerror("Error", "Please enter username and password.")
    else:
        conn = sqlite3.connect("UserDataBase.db")
        cursor = conn.cursor()

        # Retrieve user data from the database
        cursor.execute(
            "SELECT * FROM users WHERE Name = ? AND Password = ?", (name, password))
        user = cursor.fetchone()

        if user:
            messagebox.showinfo("Success", "Login successful.")
            clear_login_entries()
            root.withdraw()
            show_movie_selection()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

        conn.close()


def show_movie_selection():
    # Create the main Tkinter window
    window = tk.Toplevel(root)
    window.title("Movie Selection")
    window.geometry("800x600")
    window.configure(bg=secondary_colors["light"])
    center_window(window)

    # Create a canvas for animations
    canvas = tk.Canvas(window, bg=secondary_colors["light"], highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    
    # Create animated background
    def create_stars():
        stars = []
        for _ in range(50):
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            size = random.uniform(0.5, 2)
            star = canvas.create_oval(x, y, x+size, y+size, fill="white", outline="")
            stars.append(star)
        return stars
    
    def animate_stars():
        nonlocal stars
        for star in stars:
            canvas.move(star, 0, 1)
            coords = canvas.coords(star)
            if coords[1] > 600:
                canvas.delete(star)
                stars.remove(star)
                x = random.randint(0, 800)
                size = random.uniform(0.5, 2)
                star = canvas.create_oval(x, 0, x+size, size, fill="white", outline="")
                stars.append(star)
        window.after(50, animate_stars)
    
    stars = create_stars()
    animate_stars()

    # Create main frame
    main_frame = tk.Frame(canvas, bg=secondary_colors["light"])
    main_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Title label with animation
    title_label = create_label(main_frame, "Movie Selection", font=("Segoe UI", 28, "bold"), fg=primary_color)
    title_label.pack(pady=(0, 30))
    Animator.pulse(title_label, primary_color, secondary_colors["accent"])

    # Fetch movies from the movie database
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()
    c.execute("SELECT * FROM movies")
    movies = c.fetchall()
    conn.close()

    # Create a dictionary to store the movie library
    movie_library = {}

    for movie in movies:
        movie_info = {
            "name": movie[0],
            "year": movie[1],
            "rating": movie[2],
            "genre": movie[3],
            "Price": 800  # Add the movie price here
        }
        movie_library[movie[0]] = movie_info

    # Create movie selection frame
    selection_frame = tk.Frame(main_frame, bg=secondary_colors["light"])
    selection_frame.pack(fill="x", pady=10)

    # Movie selection
    movie_label = create_label(selection_frame, "Select Movie:", fg=primary_color)
    movie_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    
    movie_var = tk.StringVar()
    movie_dropdown = ttk.Combobox(
        selection_frame, 
        textvariable=movie_var,
        values=list(movie_library.keys()),
        font=font_entry,
        state="readonly",
        width=30
    )
    movie_dropdown.grid(row=0, column=1, padx=10, pady=10)
    movie_dropdown.current(0)

    # Timing selection
    timing_label = create_label(selection_frame, "Select Timing:", fg=primary_color)
    timing_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    
    timing_var = tk.StringVar()
    timing_dropdown = ttk.Combobox(
        selection_frame, 
        textvariable=timing_var,
        values=["9am-12pm", "12pm-3pm", "3pm-6pm", "6pm-9pm"],
        font=font_entry,
        state="readonly",
        width=30
    )
    timing_dropdown.grid(row=1, column=1, padx=10, pady=10)
    timing_dropdown.current(0)

    # Create buttons
    button_frame = tk.Frame(main_frame, bg=secondary_colors["light"])
    button_frame.pack(pady=20)
    
    book_button = create_button(
        button_frame, 
        "Book Movie", 
        lambda: book_movie(movie_var.get(), timing_var.get(), movie_library),
        bg=secondary_colors["accent"]
    )
    book_button.grid(row=0, column=0, padx=10)
    
    seat_button = create_button(
        button_frame, 
        "Book Seat", 
        book_seat,
        bg=secondary_colors["light_blue"]
    )
    seat_button.grid(row=0, column=1, padx=10)
    
    snack_button = create_button(
        button_frame, 
        "Snack Bar", 
        snack_bar,
        bg=secondary_colors["green"]
    )
    snack_button.grid(row=0, column=2, padx=10)

    # Back button
    back_button = create_button(
        main_frame, 
        "Back to Main", 
        lambda: [window.destroy(), root.deiconify()],
        bg=secondary_colors["gray"],
        width=12
    )
    back_button.pack(pady=20)


class Seat:
    def __init__(self, position, seat_number):
        self.position = position
        self.seat_number = seat_number
        self.next = None


class SeatingPlan:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_seat(self, position, seat_number):
        new_seat = Seat(position, seat_number)

        if self.head is None:
            self.head = new_seat
            self.tail = new_seat
        else:
            self.tail.next = new_seat
            self.tail = new_seat


class CinemaApp:
    seat_number_counter = 1

    def __init__(self, parent):
        self.parent = parent
        self.seating_plan = SeatingPlan()
        self.selected_seats = []

        self.window = tk.Toplevel(parent)
        self.window.title("Cinema Seat Booking")
        self.window.geometry("600x600")
        self.window.configure(bg=primary_color)
        center_window(self.window)
        Animator.fade_in(self.window)

        # Create canvas for background
        self.canvas = tk.Canvas(self.window, bg=primary_color, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Create animated background
        self.create_animated_background()
        
        # Create main frame
        main_frame = tk.Frame(self.canvas, bg="white", bd=0, highlightthickness=0)
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=500, height=500)
        
        # Title
        title_label = create_label(main_frame, "Select Your Seats", font=font_title, fg=primary_color)
        title_label.pack(pady=20)
        
        # Seat grid frame
        seat_frame = tk.Frame(main_frame, bg="white")
        seat_frame.pack(pady=10)
        
        self.create_seats(seat_frame)
        self.create_buttons(main_frame)

        # Connect to the database
        self.connection = sqlite3.connect("seat.db")
        self.create_table()
        
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_animated_background(self):
        # Create animated particles
        self.particles = []
        for _ in range(30):
            x = random.randint(0, 600)
            y = random.randint(0, 600)
            size = random.randint(2, 5)
            color = random.choice(["#64B5F6", "#42A5F5", "#1E88E5", "#0D47A1"])
            particle = self.canvas.create_oval(
                x, y, x+size, y+size, 
                fill=color, 
                outline=""
            )
            self.particles.append({
                "id": particle,
                "dx": random.uniform(-1, 1),
                "dy": random.uniform(-1, 1)
            })
            
        self.animate_particles()

    def animate_particles(self):
        for particle in self.particles:
            self.canvas.move(particle["id"], particle["dx"], particle["dy"])
            x0, y0, x1, y1 = self.canvas.coords(particle["id"])
            
            # Bounce off walls
            if x0 <= 0 or x1 >= 600:
                particle["dx"] *= -1
            if y0 <= 0 or y1 >= 600:
                particle["dy"] *= -1
                
        self.window.after(30, self.animate_particles)

    def create_seats(self, parent):
        for i in range(1, 26):
            self.seating_plan.add_seat(i, i)
            button = tk.Button(
                parent,
                text=str(i),
                width=4,
                height=2,
                command=lambda i=i: self.select_seat(i),
                font=font_label,
                bg=secondary_colors["light_blue"],
                fg="white",
                relief="flat",
                bd=0,
                activebackground=secondary_colors["accent"]
            )
            button.grid(row=(i - 1) // 5, column=(i - 1) % 5, padx=5, pady=5)

    def create_buttons(self, parent):
        button_frame = tk.Frame(parent, bg="white")
        button_frame.pack(pady=20)
        
        book_button = create_button(
            button_frame, 
            "Book Seats", 
            self.book_seat,
            bg=secondary_colors["accent"]
        )
        book_button.grid(row=0, column=0, padx=5)
        
        view_button = create_button(
            button_frame, 
            "View Selection", 
            self.view_selected_seats,
            bg=secondary_colors["light_blue"]
        )
        view_button.grid(row=0, column=1, padx=5)
        
        snack_button = create_button(
            button_frame, 
            "Snack Bar", 
            snack_bar,
            bg=secondary_colors["green"]
        )
        snack_button.grid(row=0, column=2, padx=5)
        
        back_button = create_button(
            parent, 
            "Back", 
            self.on_close,
            bg=secondary_colors["gray"],
            width=10
        )
        back_button.pack(pady=10)

    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS seat (selectedseat TEXT, seatno INT PRIMARY KEY, ticket INT)"
        )
        self.connection.commit()

    def select_seat(self, position):
        seat = self.seating_plan.head
        while seat is not None:
            if seat.position == position:
                if seat in self.selected_seats:
                    # Deselect the seat
                    self.selected_seats.remove(seat)
                    button = self.get_button_by_position(position)
                    button.configure(bg=secondary_colors["light_blue"])
                    print(f"Seat {position} deselected.")
                else:
                    # Select the seat
                    self.selected_seats.append(seat)
                    button = self.get_button_by_position(position)
                    button.configure(bg="yellow")
                    print(f"Seat {position} selected.")
                break
            seat = seat.next

    def get_button_by_position(self, position):
        for widget in self.window.winfo_children():
            if isinstance(widget, tk.Button) and widget.winfo_parent() == self.window.winfo_children()[0].winfo_children()[1].winfo_id():
                if widget["text"] == str(position):
                    return widget
        return None

    def book_seat(self):
        if self.selected_seats:
            selected_seat_numbers = [
                seat.seat_number for seat in self.selected_seats
            ]
            selected_seats_str = ", ".join(
                str(seat.position) for seat in self.selected_seats
            )

            cursor = self.connection.cursor()

            # Retrieve the maximum seat number
            cursor.execute("SELECT MAX(seatno) FROM seat")
            result = cursor.fetchone()
            max_seat_number = result[0] if result[0] else 0

            # Generate a unique seat number by incrementing the maximum seat number
            seat_number = max_seat_number + 1

            cursor.execute(
                "INSERT INTO seat (selectedseat, seatno, ticket) VALUES (?, ?, ?)",
                (
                    selected_seats_str,
                    seat_number,
                    len(self.selected_seats),
                ),
            )
            self.connection.commit()

            ticket = len(self.selected_seats)
            seat_numbers = ", ".join(str(seat) for seat in selected_seat_numbers)
            messagebox.showinfo(
                "Seats Booked",
                f"{ticket} seats (Numbers: {seat_numbers}) have been booked!",
            )
            self.selected_seats = []
        else:
            messagebox.showerror("Error", "No seats selected.")

    def view_selected_seats(self):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT selectedseat, ticket FROM seat ORDER BY seatno DESC LIMIT 1"
        )
        result = cursor.fetchone()

        if result:
            selected_seats_str = result[0]
            ticket = result[1]
            selected_seats = selected_seats_str.split(", ")

            view_window = tk.Toplevel(self.window)
            view_window.title("Selected Seats")
            view_window.geometry("300x150")
            view_window.configure(bg=secondary_colors["light"])
            center_window(view_window)

            title_label = create_label(
                view_window,
                "Selected Seats",
                font=font_title,
                fg=primary_color
            )
            title_label.pack(pady=10)

            seats_label = create_label(
                view_window,
                f"{ticket} seats: {', '.join(selected_seats)}",
                fg=secondary_colors["dark"]
            )
            seats_label.pack(pady=10)

        else:
            messagebox.showinfo("No Seats", "No seats have been selected.")

    def on_close(self):
        self.connection.close()
        Animator.fade_out(self.window)
        self.parent.deiconify()


def book_seat():
    root.withdraw()
    cinema_app = CinemaApp(root)


def book_movie(movie, timing, movie_library):
    room_no = random.randint(1, 4)  # Generate a random room number

    # Get the movie information from the movie library
    movie_info = movie_library[movie]
    movie_price = movie_info["Price"]  # Retrieve the movie price

    # Store the movie selection, timing, room number, and price in the database
    conn = sqlite3.connect('UserBill.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS UserBill (Movie TEXT, Timing TEXT, RoomNo INT, MoviePrice REAL)")
    c.execute("INSERT INTO UserBill (Movie, Timing, RoomNo, MoviePrice) VALUES (?, ?, ?, ?)",
              (movie, timing, room_no, movie_price))
    conn.commit()
    conn.close()

    # Show a success message
    messagebox.showinfo("Success", "Movie booked successfully!\n\n"
                                    f"Movie: {movie}\n"
                                    f"Timing: {timing}\n"
                                    f"Room No: {room_no}\n"
                                    f"Price: {800}")


def snack_bar():
    # Create the main Tkinter window
    window = tk.Toplevel(root)
    window.title("Snack Bar")
    window.geometry("600x500")
    window.configure(bg=secondary_colors["light"])
    center_window(window)
    Animator.fade_in(window)

    # Create main frame
    main_frame = tk.Frame(window, bg=secondary_colors["light"], bd=0, highlightthickness=0)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Title with animation
    title_label = create_label(main_frame, "Snack Bar", font=font_title, fg=primary_color)
    title_label.pack(pady=10)
    Animator.pulse(title_label, primary_color, secondary_colors["accent"])

    # Create selection frame
    selection_frame = tk.Frame(main_frame, bg=secondary_colors["light"])
    selection_frame.pack(fill="x", pady=20)

    # Popcorn selection
    popcorn_label = create_label(selection_frame, "Select Popcorn:", fg=primary_color)
    popcorn_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    
    popcorn_var = tk.StringVar()
    popcorn_dropdown = ttk.Combobox(
        selection_frame, 
        textvariable=popcorn_var,
        values=["Small Popcorn", "Medium Popcorn", "Large Popcorn"],
        font=font_entry,
        state="readonly",
        width=25
    )
    popcorn_dropdown.grid(row=0, column=1, padx=10, pady=10)
    popcorn_dropdown.current(0)

    # Drink selection
    drink_label = create_label(selection_frame, "Select Drink:", fg=primary_color)
    drink_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    
    drink_var = tk.StringVar()
    drink_dropdown = ttk.Combobox(
        selection_frame, 
        textvariable=drink_var,
        values=["Soda", "Water", "Juice"],
        font=font_entry,
        state="readonly",
        width=25
    )
    drink_dropdown.grid(row=1, column=1, padx=10, pady=10)
    drink_dropdown.current(0)

    # Establish a database connection
    connection = sqlite3.connect("Snack.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS SnackItem (OrderItem TEXT, Price REAL)")
    connection.commit()

    # Create a snack bar queue
    snack_bar_queue = Queue()

    # Function to place an order
    def place_order():
        selected_popcorn = popcorn_var.get()
        selected_drink = drink_var.get()
        order = f"{selected_popcorn} + {selected_drink}"
        price = get_price(selected_popcorn)
        snack_bar_queue.put(order)
        cursor.execute("INSERT INTO SnackItem (OrderItem, Price) VALUES (?, ?)", (order, price))
        connection.commit()
        messagebox.showinfo("Order Placed", f"Your order ({order}) has been placed!")

    # Function to get the price based on the selected popcorn
    def get_price(selected_popcorn):
        if selected_popcorn == "Small Popcorn":
            return 100
        elif selected_popcorn == "Medium Popcorn":
            return 200
        elif selected_popcorn == "Large Popcorn":
            return 250

    # Function to serve an order
    def serve_order():
        if not snack_bar_queue.empty():
            order = snack_bar_queue.get()
            messagebox.showinfo("Order Served", f"The order ({order}) has been served!")
        else:
            messagebox.showinfo("No Orders", "There are no orders to be served.")

    # Function to view orders
    def view_orders():
        orders = list(snack_bar_queue.queue)
        if orders:
            order_details = "\n".join(orders)
            messagebox.showinfo("Current Orders", f"Current Orders:\n{order_details}")
        else:
            messagebox.showinfo("No Orders", "There are no orders.")

    # Function to check waiting time
    def check_waiting_time():
        waiting_orders = snack_bar_queue.qsize()
        messagebox.showinfo("Waiting Time", f"There are {waiting_orders} orders waiting to be served.")

    # Create buttons
    button_frame = tk.Frame(main_frame, bg=secondary_colors["light"])
    button_frame.pack(pady=20)
    
    place_order_button = create_button(
        button_frame, 
        "Place Order", 
        place_order,
        bg=secondary_colors["accent"]
    )
    place_order_button.grid(row=0, column=0, padx=5)
    
    serve_order_button = create_button(
        button_frame, 
        "Serve Order", 
        serve_order,
        bg=secondary_colors["light_blue"]
    )
    serve_order_button.grid(row=0, column=1, padx=5)
    
    view_orders_button = create_button(
        button_frame, 
        "View Orders", 
        view_orders,
        bg=secondary_colors["green"]
    )
    view_orders_button.grid(row=0, column=2, padx=5)
    
    waiting_time_button = create_button(
        button_frame, 
        "Check Waiting", 
        check_waiting_time,
        bg=secondary_colors["orange"]
    )
    waiting_time_button.grid(row=1, column=0, padx=5, pady=10, columnspan=3)

    def totalbill():
        # Create a new window for the total bill
        total_bill_window = tk.Toplevel(window)
        total_bill_window.title("Movie Ticket")
        total_bill_window.geometry("500x700")
        total_bill_window.configure(bg="white")
        center_window(total_bill_window)
        
        # Ticket header
        header_frame = tk.Frame(total_bill_window, bg=primary_color)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        title_label = create_label(
            header_frame, 
            "CINEMA TICKET", 
            font=("Segoe UI", 24, "bold"), 
            fg="white",
            anchor="center"
        )
        title_label.pack(pady=10)
        
        # Ticket body
        body_frame = tk.Frame(total_bill_window, bg="white")
        body_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Display ticket details
        details = [
            ("Name:", "John Doe"),
            ("Movie:", "Avengers: Endgame"),
            ("Timing:", "6pm-9pm"),
            ("Room No:", "3"),
            ("Seats:", "A1, A2, A3"),
            ("Snack:", "Large Popcorn + Soda"),
            ("Total Price:", "₹1,250")
        ]
        
        for label, value in details:
            frame = tk.Frame(body_frame, bg="white")
            frame.pack(fill="x", pady=5)
            
            lbl = create_label(frame, label, font=("Segoe UI", 14, "bold"), fg=primary_color, width=15)
            lbl.pack(side="left", padx=10)
            
            val = create_label(frame, value, font=("Segoe UI", 14), fg=secondary_colors["dark"])
            val.pack(side="left")
        
        # Thank you message
        thank_label = create_label(
            body_frame, 
            "Thank you for your purchase!\nEnjoy the movie!",
            font=("Segoe UI", 14, "italic"),
            fg=secondary_colors["gray"],
            anchor="center"
        )
        thank_label.pack(pady=20)
        
        # Close button
        close_button = create_button(
            body_frame, 
            "Close", 
            total_bill_window.destroy,
            bg=secondary_colors["accent"],
            width=10
        )
        close_button.pack(pady=20)

    total_bill_button = create_button(
        main_frame, 
        "Generate Ticket", 
        totalbill,
        bg=secondary_colors["accent"]
    )
    total_bill_button.pack(pady=10)

    back_button = create_button(
        main_frame, 
        "Back", 
        window.destroy,
        bg=secondary_colors["gray"],
        width=10
    )
    back_button.pack(pady=10)
    
    window.mainloop()


def clear_signup_entries():
    reg_username_entry.delete(0, tk.END)
    reg_password_entry.delete(0, tk.END)


def clear_login_entries():
    login_username_entry.delete(0, tk.END)
    login_password_entry.delete(0, tk.END)


def show_registered_users():
    conn = sqlite3.connect("UserDataBase.db")
    cursor = conn.cursor()

    # Retrieve all user data from the database
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    if users:
        user_list = "\n".join([f"Name: {user[0]}, Password: {user[1]}" for user in users])
        messagebox.showinfo("Registered Users", f"List of Registered Users:\n\n{user_list}")
    else:
        messagebox.showinfo("Registered Users", "No registered users found.")

    conn.close()


def create_movie_library_window():
    # Create movie library window
    movie_library_window = tk.Toplevel(root)
    movie_library_window.title("Movie Library")
    movie_library_window.geometry("600x400")
    movie_library_window.configure(bg=secondary_colors["light"])
    center_window(movie_library_window)

    # Function to add movie to library
    def add_movie():
        name = name_entry.get()
        year = year_entry.get()
        rating = rating_entry.get()
        genre = genre_entry.get()

        # Add movie to dictionary
        movies_dict[name] = {"year": year, "rating": rating, "genre": genre}

        # Insert movie data into SQLite database
        cursor.execute("INSERT INTO movies (name, year, rating, genre) VALUES (?, ?, ?, ?)",
                       (name, year, rating, genre))
        conn.commit()

        # Clear entry fields
        name_entry.delete(0, tk.END)
        year_entry.delete(0, tk.END)
        rating_entry.delete(0, tk.END)
        genre_entry.delete(0, tk.END)

        # Display messagebox
        messagebox.showinfo("Movie Library", "Movie added successfully!")

    # Function to remove movie from library
    def remove_movie():
        name = name_entry.get()

        if name in movies_dict:
            del movies_dict[name]

            # Delete movie data from SQLite database
            cursor.execute("DELETE FROM movies WHERE name = ?", (name,))
            conn.commit()

            # Clear entry fields
            name_entry.delete(0, tk.END)

            # Display messagebox
            messagebox.showinfo("Movie Library", "Movie removed successfully!")
        else:
            messagebox.showerror("Movie Library", "Movie not found")

    # Function to update movie information in library
    def update_movie():
        name = name_entry.get()
        year = year_entry.get()
        rating = rating_entry.get()
        genre = genre_entry.get()

        if name in movies_dict:
            movies_dict[name] = {"year": year, "rating": rating, "genre": genre}

            # Update movie data in SQLite database
            cursor.execute("UPDATE movies SET year = ?, rating = ?, genre = ? WHERE name = ?",
                           (year, rating, genre, name))
            conn.commit()

            # Clear entry fields
            name_entry.delete(0, tk.END)
            year_entry.delete(0, tk.END)
            rating_entry.delete(0, tk.END)
            genre_entry.delete(0, tk.END)

            # Display messagebox
            messagebox.showinfo(
                "Movie Library", "Movie information updated successfully!")
        else:
            messagebox.showerror("Movie Library", "Movie not found")

    # Function to search for a movie in the library
    def search_movie():
        name = name_entry.get()

        if name in movies_dict:
            movie = movies_dict[name]
            messagebox.showinfo(
                "Movie Library", f"Name: {name}\nYear: {movie['year']}\nRating: {movie['rating']}\nGenre: {movie['genre']}")
        else:
            messagebox.showerror("Movie Library", "Movie not found")

    # Create main frame
    main_frame = tk.Frame(movie_library_window, bg=secondary_colors["light"])
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Title
    title_label = create_label(main_frame, "Movie Library", font=font_title, fg=primary_color)
    title_label.pack(pady=10)

    # Input frame
    input_frame = tk.Frame(main_frame, bg=secondary_colors["light"])
    input_frame.pack(pady=10)

    # Add labels and entry fields
    name_label = create_label(input_frame, "Name:", fg=primary_color)
    name_label.grid(row=0, column=0, pady=5, padx=10, sticky="e")
    name_entry = create_entry(input_frame, width=30)
    name_entry.grid(row=0, column=1, pady=5, padx=10)
    
    year_label = create_label(input_frame, "Year:", fg=primary_color)
    year_label.grid(row=1, column=0, pady=5, padx=10, sticky="e")
    year_entry = create_entry(input_frame, width=30)
    year_entry.grid(row=1, column=1, pady=5, padx=10)
    
    rating_label = create_label(input_frame, "Rating:", fg=primary_color)
    rating_label.grid(row=2, column=0, pady=5, padx=10, sticky="e")
    rating_entry = create_entry(input_frame, width=30)
    rating_entry.grid(row=2, column=1, pady=5, padx=10)
    
    genre_label = create_label(input_frame, "Genre:", fg=primary_color)
    genre_label.grid(row=3, column=0, pady=5, padx=10, sticky="e")
    genre_entry = create_entry(input_frame, width=30)
    genre_entry.grid(row=3, column=1, pady=5, padx=10)

    # Button frame
    button_frame = tk.Frame(main_frame, bg=secondary_colors["light"])
    button_frame.pack(pady=20)

    # Add buttons
    add_button = create_button(
        button_frame, 
        "Add Movie", 
        add_movie,
        bg=secondary_colors["green"]
    )
    add_button.grid(row=0, column=0, padx=5)
    
    remove_button = create_button(
        button_frame, 
        "Remove Movie", 
        remove_movie,
        bg=secondary_colors["orange"]
    )
    remove_button.grid(row=0, column=1, padx=5)
    
    update_button = create_button(
        button_frame, 
        "Update Movie", 
        update_movie,
        bg=secondary_colors["light_blue"]
    )
    update_button.grid(row=0, column=2, padx=5)
    
    search_button = create_button(
        button_frame, 
        "Search Movie", 
        search_movie,
        bg=secondary_colors["gray"]
    )
    search_button.grid(row=0, column=3, padx=5)
    
    back_button = create_button(
        main_frame, 
        "Back", 
        movie_library_window.destroy,
        bg=secondary_colors["gray"],
        width=10
    )
    back_button.pack(pady=10)


# Create main window
root = tk.Tk()
root.title("Movie Management System")
root.config(bg=secondary_colors["light"])
root.geometry("700x600")
center_window(root)
root.resizable(False, False)

# Create animated background
canvas = tk.Canvas(root, bg=secondary_colors["light"], highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Create animated particles
particles = []
for _ in range(30):
    x = random.randint(0, 700)
    y = random.randint(0, 600)
    size = random.randint(2, 5)
    color = random.choice(["#64B5F6", "#42A5F5", "#1E88E5", "#0D47A1"])
    particle = canvas.create_oval(
        x, y, x+size, y+size, 
        fill=color, 
        outline=""
    )
    particles.append({
        "id": particle,
        "dx": random.uniform(-1, 1),
        "dy": random.uniform(-1, 1)
    })

def animate_particles():
    for particle in particles:
        canvas.move(particle["id"], particle["dx"], particle["dy"])
        x0, y0, x1, y1 = canvas.coords(particle["id"])
        
        # Bounce off walls
        if x0 <= 0 or x1 >= 700:
            particle["dx"] *= -1
        if y0 <= 0 or y1 >= 600:
            particle["dy"] *= -1
            
    root.after(30, animate_particles)

animate_particles()

# Create main content frame
main_frame = tk.Frame(canvas, bg="white", bd=0, highlightthickness=0, relief="flat")
main_frame.place(relx=0.5, rely=0.5, anchor="center", width=600, height=500)

# Title with animation
title_label = create_label(main_frame, "CINEMA MANAGEMENT SYSTEM", font=("Segoe UI", 24, "bold"), fg=primary_color)
title_label.pack(pady=30)
Animator.pulse(title_label, primary_color, secondary_colors["accent"])

# Create admin password variable
admin_password = "1234"

# Function to handle admin access
def admin_panel():
    # Simple admin panel window
    admin_window = tk.Toplevel(root)
    admin_window.title("Admin Panel")
    admin_window.geometry("400x300")
    admin_window.configure(bg=secondary_colors["light"])
    center_window(admin_window)

    title_label = create_label(admin_window, "Admin Panel", font=font_title, fg=primary_color)
    title_label.pack(pady=20)

    # Example admin actions
    show_users_button = create_button(
        admin_window,
        "Show Registered Users",
        show_registered_users,
        bg=secondary_colors["light_blue"]
    )
    show_users_button.pack(pady=10)

    movie_library_button = create_button(
        admin_window,
        "Movie Library",
        create_movie_library_window,
        bg=secondary_colors["green"]
    )
    movie_library_button.pack(pady=10)

    close_button = create_button(
        admin_window,
        "Close",
        admin_window.destroy,
        bg=secondary_colors["gray"],
        width=10
    )
    close_button.pack(pady=20)

def admin_access():
    password = simpledialog.askstring(
        "Admin Access", "Enter Admin Password:", show="*")
    if password == admin_password:
        admin_panel()
    else:
        messagebox.showerror("Admin Access", "Invalid password.")

# Create admin access frame
admin_frame = tk.Frame(main_frame, bg="white")
admin_frame.pack(fill="x", padx=50, pady=10)

admin_access_button = create_button(
    admin_frame, 
    "Admin Access", 
    admin_access,
    bg=secondary_colors["light_blue"]
)
admin_access_button.pack(fill="x", pady=5)

# Create user registration frame
reg_frame = tk.Frame(main_frame, bg="white")
reg_frame.pack(fill="x", padx=50, pady=10)

reg_title = create_label(reg_frame, "User Registration", font=("Segoe UI", 14, "bold"), fg=primary_color)
reg_title.pack(anchor="w", pady=(0, 5))

# Add registration labels and entry fields
input_frame = tk.Frame(reg_frame, bg="white")
input_frame.pack(fill="x")

reg_username_label = create_label(input_frame, "Username:", fg=primary_color, width=10)
reg_username_label.grid(row=0, column=0, pady=5)
reg_username_entry = create_entry(input_frame, width=25)
reg_username_entry.grid(row=0, column=1, pady=5)

reg_password_label = create_label(input_frame, "Password:", fg=primary_color, width=10)
reg_password_label.grid(row=1, column=0, pady=5)
reg_password_entry = create_entry(input_frame, width=25, show="*")
reg_password_entry.grid(row=1, column=1, pady=5)

# Create register button
register_button = create_button(
    reg_frame, 
    "Register", 
    register_user,
    bg=secondary_colors["green"]
)
register_button.pack(fill="x", pady=10)

# Create user login frame
login_frame = tk.Frame(main_frame, bg="white")
login_frame.pack(fill="x", padx=50, pady=10)

login_title = create_label(login_frame, "User Login", font=("Segoe UI", 14, "bold"), fg=primary_color)
login_title.pack(anchor="w", pady=(0, 5))

# Add login labels and entry fields
login_input_frame = tk.Frame(login_frame, bg="white")
login_input_frame.pack(fill="x")

login_username_label = create_label(login_input_frame, "Username:", fg=primary_color, width=10)
login_username_label.grid(row=0, column=0, pady=5)
login_username_entry = create_entry(login_input_frame, width=25)
login_username_entry.grid(row=0, column=1, pady=5)

login_password_label = create_label(login_input_frame, "Password:", fg=primary_color, width=10)
login_password_label.grid(row=1, column=0, pady=5)
login_password_entry = create_entry(login_input_frame, width=25, show="*")
login_password_entry.grid(row=1, column=1, pady=5)

# Add login button
login_button = create_button(
    login_frame, 
    "Login", 
    login_user,
    bg=secondary_colors["accent"]
)
login_button.pack(fill="x", pady=10)

# Create a table to store user data if it doesn't exist
create_user_table()

# Start the main tkinter loop
root.mainloop()