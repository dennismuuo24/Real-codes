import tkinter as tk
from tkinter import messagebox
import mysql.connector
import requests
import datetime
import matplotlib.pyplot as plt

# Add your MySQL database connection details here
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="*.*dennis1M",
    database="uhuru"
)

class FarmerConnectApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Farmer Connect")
        self.geometry("600x500")  # Adjusted window size
        self.configure(bg="green")  # Change background color to green

        self.current_frame = None

        self.set_background_image()
        self.set_logo()  # Add the farming logo

        self.switch_to_login()

    def set_background_image(self):
        self.background_image = tk.PhotoImage(file="crops.png")  # Make sure to replace "crops.png" with your image file
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

    def set_logo(self):
        self.logo_image = tk.PhotoImage(file="imagess.png")  # Replace "farming_logo.png" with your logo file
        self.logo_label = tk.Label(self, image=self.logo_image, bg="green")
        self.logo_label.place(x=10, y=10)  # Adjust the position of the logo as needed

    def switch_to_login(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = LoginFrame(self)
        self.current_frame.pack(expand=True, fill=tk.BOTH)


    def switch_to_signup(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = SignupFrame(self)
        self.current_frame.pack(expand=True, fill=tk.BOTH)

    def switch_to_dashboard(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = DashboardFrame(self)
        self.current_frame.pack(expand=True, fill=tk.BOTH)

class DashboardFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#e3f2fd")
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        # Add the logo label to the frame with a smaller size
        self.logo_image = tk.PhotoImage(file="imagess.png")  # Replace "logos.png" with your logo file
        self.logo_image = self.logo_image.subsample(2, 2)  # Resize the logo to half its original size
        self.logo_label = tk.Label(self, image=self.logo_image, bg="#e3f2fd")
        self.logo_label.grid(row=0, column=0, sticky="nw", padx=5, pady=5)  # Place the logo in the top-left corner

        # Add other widgets below the logo
        self.label = tk.Label(self, text="Welcome to Trading Dashboard", bg="#e3f2fd", font=("Arial", 20, "bold"))
        self.label.grid(row=0, column=1, columnspan=2, pady=(20, 10), sticky="w")

        self.add_product_button = tk.Button(self, text="Add Product", command=self.add_product, bg="#4caf50", fg="white", font=("Arial", 12))
        self.add_product_button.grid(row=1, column=1, pady=10, padx=10, sticky="ew")

        self.predict_weather_button = tk.Button(self, text="Predict Weather", command=self.predict_weather, bg="#4caf50", fg="white", font=("Arial", 12))
        self.predict_weather_button.grid(row=1, column=2, pady=10, padx=10, sticky="ew")

        self.view_profile_button = tk.Button(self, text="View Profile", command=self.view_profile, bg="#4caf50", fg="white", font=("Arial", 12))
        self.view_profile_button.grid(row=2, column=1, pady=10, padx=10, sticky="ew")

        self.communicate_buyer_button = tk.Button(self, text="Communicate with Buyer", command=self.communicate_buyer, bg="#4caf50", fg="white", font=("Arial", 12))
        self.communicate_buyer_button.grid(row=2, column=2, pady=10, padx=10, sticky="ew")

        self.chatbot_button = tk.Button(self, text="Chatbot", command=self.open_chatbot, bg="#4caf50", fg="white", font=("Arial", 12))
        self.chatbot_button.grid(row=3, column=1, pady=10, padx=10, sticky="ew")

        # Search Entry
        self.search_entry = tk.Entry(self, font=("Arial", 12))
        self.search_entry.grid(row=3, column=2, pady=10, padx=10, sticky="ew")

        # Search Button
        self.search_button = tk.Button(self, text="Search", command=self.search_weather, bg="#4caf50", fg="white", font=("Arial", 12))
        self.search_button.grid(row=4, column=2, pady=10, padx=10, sticky="ew")

        # Logout Button
        self.logout_button = tk.Button(self, text="Logout", command=self.logout, bg="#f44336", fg="white", font=("Arial", 12))
        self.logout_button.grid(row=5, column=2, pady=10, padx=10, sticky="e")

        # Back Button
        self.back_button = tk.Button(self, text="Back", command=self.back_to_login, bg="#2196f3", fg="white", font=("Arial", 12))
        self.back_button.grid(row=5, column=1, pady=10, padx=10, sticky="w")

    def add_product(self):
        messagebox.showinfo("Add Product", "Functionality to add a product goes here.")

    def predict_weather(self):
        api_key = '77f9b1275208fecedaa91294bed37723'
        city_name = 'Nairobi'  # Default city
        url = f'http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key}&units=metric'

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()

            # Extract relevant information for the next 5 days
            forecast_data = data['list'][:5]
            dates = [datetime.datetime.strptime(entry['dt_txt'], "%Y-%m-%d %H:%M:%S") for entry in forecast_data]
            temperatures = [entry['main']['temp'] for entry in forecast_data]
            humidity = [entry['main']['humidity'] for entry in forecast_data]
            wind_speed = [entry['wind']['speed'] for entry in forecast_data]

            # Plotting the graph
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.plot(dates, temperatures, marker='o', label='Temperature (°C)')
            ax.plot(dates, humidity, marker='o', label='Humidity (%)')
            ax.plot(dates, wind_speed, marker='o', label='Wind Speed (m/s)')
            ax.set_title('Weather Forecast for the Next 5 Days')
            ax.set_xlabel('Date')
            ax.set_ylabel('Value')
            ax.legend()
            ax.grid(True)
            plt.xticks(rotation=45, ha='right')

            # Annotate each data point with temperature, humidity, and wind speed
            for date, temp, hum, wind in zip(dates, temperatures, humidity, wind_speed):
                day = date.strftime("%A")  # Get the day name
                ax.annotate(f'{day}\nTemp: {temp}°C\nHumidity: {hum}%\nWind Speed: {wind} m/s',
                            xy=(date, temp), xytext=(-20, 10), textcoords='offset points', ha='center')

            # Display the plot in a new window
            plt.tight_layout()
            plt.show()

        except requests.exceptions.RequestException as e:
            # Handle exceptions
            print(f"Request Exception: {e}")
            messagebox.showerror("Error", f"Failed to fetch weather data: {str(e)}")
        except Exception as e:
            # Handle other unexpected exceptions
            print(f"Unexpected Exception: {e}")
            messagebox.showerror("Error", f"Failed to fetch weather data: {str(e)}")

    def view_profile(self):
        # Fetch the logged-in user's details from the database using the stored email
        cursor = db_connection.cursor()
        sql = "SELECT * FROM users WHERE email = %s"
        cursor.execute(sql, (self.email,))
        user = cursor.fetchone()

        if user:
            # Display user profile details
            profile_info = f"Name: {user[1]}\nEmail: {user[2]}\nPhone: {user[3]}\nGender: {user[5]}\nUser Type: {user[6]}"
            messagebox.showinfo("Profile Details", profile_info)
        else:
            # If user not found (which shouldn't happen if the user is logged in), show an error message
            messagebox.showerror("Error", "Failed to retrieve user profile")

        cursor.close()

    def communicate_buyer(self):
        messagebox.showinfo("Communicate with Buyer", "Functionality to communicate with buyer goes here.")

    def open_chatbot(self):
        messagebox.showinfo("Chatbot", "Chatbot functionality goes here.")

    def logout(self):
        messagebox.showinfo("Logout", "Successfully logged out")
        self.master.switch_to_login()

    def back_to_login(self):
        self.master.switch_to_login()

    def search_weather(self):
        city_name = "Nairobi"  # Default city
        # Get the city name from the entry widget
        if self.search_entry.get():
            city_name = self.search_entry.get()

        # Update the graph with the weather data for the searched city
        api_key = '77f9b1275208fecedaa91294bed37723'
        url = f'http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key}&units=metric'

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()

            # Extract relevant information for the next 5 days
            forecast_data = data['list'][:5]
            dates = [datetime.datetime.strptime(entry['dt_txt'], "%Y-%m-%d %H:%M:%S") for entry in forecast_data]
            temperatures = [entry['main']['temp'] for entry in forecast_data]
            humidity = [entry['main']['humidity'] for entry in forecast_data]
            wind_speed = [entry['wind']['speed'] for entry in forecast_data]

            # Clear the existing plot before updating with new data
            plt.clf()

            # Plotting the graph
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.plot(dates, temperatures, marker='o', label='Temperature (°C)')
            ax.plot(dates, humidity, marker='o', label='Humidity (%)')
            ax.plot(dates, wind_speed, marker='o', label='Wind Speed (m/s)')
            ax.set_title(f'Weather Forecast for {city_name} - Next 5 Days')
            ax.set_xlabel('Date')
            ax.set_ylabel('Value')
            ax.legend()
            ax.grid(True)
            plt.xticks(rotation=45, ha='right')

            # Annotate each data point with temperature, humidity, and wind speed
            for date, temp, hum, wind in zip(dates, temperatures, humidity, wind_speed):
                day = date.strftime("%A")  # Get the day name
                ax.annotate(f'{day}\nTemp: {temp}°C\nHumidity: {hum}%\nWind Speed: {wind} m/s',
                            xy=(date, temp), xytext=(-20, 10), textcoords='offset points', ha='center')

            # Display the plot in a new window
            plt.tight_layout()
            plt.show()

        except requests.exceptions.RequestException as e:
            # Handle exceptions
            print(f"Request Exception: {e}")
            messagebox.showerror("Error", f"Failed to fetch weather data: {str(e)}")
        except Exception as e:
            # Handle other unexpected exceptions
            print(f"Unexpected Exception: {e}")
            messagebox.showerror("Error", f"Failed to fetch weather data: {str(e)}")

class LoginFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#e3f2fd")
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Login", bg="#e3f2fd", font=("Arial", 20, "bold"))
        self.label.pack(pady=(20, 10))

        self.email_label = tk.Label(self, text="Email:", bg="#e3f2fd", font=("Arial", 12))
        self.email_label.pack()
        self.email_entry = tk.Entry(self, font=("Arial", 12))
        self.email_entry.pack()

        self.password_label = tk.Label(self, text="Password:", bg="#e3f2fd", font=("Arial", 12))
        self.password_label.pack()
        self.password_entry = tk.Entry(self, show="*", font=("Arial", 12))
        self.password_entry.pack()

        self.login_button = tk.Button(self, text="Login", command=self.login, bg="#4caf50", fg="white", font=("Arial", 12))
        self.login_button.pack(pady=10)

        self.signup_link = tk.Label(self, text="Don't have an account? Sign up", bg="#e3f2fd", fg="blue", cursor="hand2", font=("Arial", 10, "underline"))
        self.signup_link.pack()
        self.signup_link.bind("<Button-1>", lambda event: self.master.switch_to_signup())

        # Bind the <Return> key to trigger the login action
        self.password_entry.bind("<Return>", lambda event: self.login())

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Check if the email and password match any existing user in the database
        cursor = db_connection.cursor()
        sql = "SELECT * FROM users WHERE email = %s AND password = %s"
        cursor.execute(sql, (email, password))
        user = cursor.fetchone()

        if user:
            # Show a pop-up message for successful login
            messagebox.showinfo("Login", "Successfully logged in")

            # If login is successful, switch to the dashboard
            self.master.switch_to_dashboard()
        else:
            # Show an error message for invalid user or password
            messagebox.showerror("Login Failed", "Invalid user or password")

class SignupFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#e3f2fd")
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Sign Up", bg="#e3f2fd", font=("Arial", 20, "bold"))
        self.label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

        self.name_label = tk.Label(self, text="Full Name:", bg="#e3f2fd", font=("Arial", 12))
        self.name_label.grid(row=1, column=0, sticky="w", padx=20, pady=10)
        self.name_entry = tk.Entry(self, font=("Arial", 12))
        self.name_entry.grid(row=1, column=1, padx=20, pady=10)

        self.email_label = tk.Label(self, text="Email:", bg="#e3f2fd", font=("Arial", 12))
        self.email_label.grid(row=2, column=0, sticky="w", padx=20, pady=10)
        self.email_entry = tk.Entry(self, font=("Arial", 12))
        self.email_entry.grid(row=2, column=1, padx=20, pady=10)

        self.phone_label = tk.Label(self, text="Phone Number:", bg="#e3f2fd", font=("Arial", 12))
        self.phone_label.grid(row=3, column=0, sticky="w", padx=20, pady=10)
        self.phone_entry = tk.Entry(self, font=("Arial", 12))
        self.phone_entry.grid(row=3, column=1, padx=20, pady=10)

        self.password_label = tk.Label(self, text="Password:", bg="#e3f2fd", font=("Arial", 12))
        self.password_label.grid(row=4, column=0, sticky="w", padx=20, pady=10)
        self.password_entry = tk.Entry(self, show="*", font=("Arial", 12))
        self.password_entry.grid(row=4, column=1, padx=20, pady=10)

        self.gender_label = tk.Label(self, text="Gender:", bg="#e3f2fd", font=("Arial", 12))
        self.gender_label.grid(row=5, column=0, sticky="w", padx=20, pady=10)
        self.gender_var = tk.StringVar(value="Male")
        self.male_radio = tk.Radiobutton(self, text="Male", variable=self.gender_var, value="Male", bg="#e3f2fd", font=("Arial", 12))
        self.male_radio.grid(row=5, column=1, sticky="w", padx=20, pady=5)
        self.female_radio = tk.Radiobutton(self, text="Female", variable=self.gender_var, value="Female", bg="#e3f2fd", font=("Arial", 12))
        self.female_radio.grid(row=6, column=1, sticky="w", padx=20, pady=5)

        self.user_type_label = tk.Label(self, text="User Type:", bg="#e3f2fd", font=("Arial", 12))
        self.user_type_label.grid(row=7, column=0, sticky="w", padx=20, pady=10)
        self.user_type_var = tk.StringVar(value="buyer")
        self.user_type_menu = tk.OptionMenu(self, self.user_type_var, "buyer", "seller")
        self.user_type_menu.config(font=("Arial", 12))
        self.user_type_menu.grid(row=7, column=1, padx=20, pady=10)

        self.signup_button = tk.Button(self, text="Sign Up", command=self.signup, bg="#4caf50", fg="white", font=("Arial", 12))
        self.signup_button.grid(row=8, column=0, columnspan=2, pady=10)

        self.login_link = tk.Label(self, text="Already have an account? Login", bg="#e3f2fd", fg="blue", cursor="hand2", font=("Arial", 10, "underline"))
        self.login_link.grid(row=9, column=0, columnspan=2)
        self.login_link.bind("<Button-1>", lambda event: self.master.switch_to_login())

    def signup(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        password = self.password_entry.get()
        gender = self.gender_var.get()
        user_type = self.user_type_var.get()

        if not name or not email or not phone or not password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if len(phone) != 10 or not phone.isdigit():
            messagebox.showerror("Error", "Please enter a valid 10-digit phone number.")
            return

        # Check if the email already exists in the database
        cursor = db_connection.cursor()
        sql = "SELECT * FROM users WHERE email = %s"
        cursor.execute(sql, (email,))
        user = cursor.fetchone()

        if user:
            messagebox.showerror("Error", "Email already exists. Please use a different email.")
            return

        # If all checks pass, insert the new user into the database
        sql = "INSERT INTO users (name, email, phone, password, gender, user_type) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (name, email, phone, password, gender, user_type))
        db_connection.commit()

        # Show a success message
        messagebox.showinfo("Success", "Account created successfully. You can now login.")
        self.master.switch_to_login()

if __name__ == "__main__":
    app = FarmerConnectApp()
    app.mainloop()
