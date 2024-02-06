import tkinter as tk
from tkinter import ttk, messagebox
import requests
import threading


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("600x500")

        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Helvetica", 12), anchor="center")
        self.style.configure("TButton", font=("Helvetica", 12), foreground="blue")  
        self.style.configure("TRadiobutton", font=("Helvetica", 12))
        self.style.configure("TCombobox", font=("Helvetica", 12))

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding="10", style="TFrame")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        frame.columnconfigure(0, weight=1)

        self.label_city = ttk.Label(frame, text="Enter city:")
        self.label_city.grid(row=0, column=0, pady=10, sticky=tk.W)

        self.entry_city = ttk.Entry(frame, font=("Helvetica", 12))
        self.entry_city.grid(row=1, column=0, pady=10, sticky=tk.W + tk.E)

        self.button_get_weather = ttk.Button(frame, text="Get Weather", command=self.get_weather)
        self.button_get_weather.grid(row=2, column=0, pady=20, sticky=tk.W + tk.E)

        self.weather_label = ttk.Label(frame, text="", font=("Helvetica", 14), style="TLabel")
        self.weather_label.grid(row=3, column=0, pady=10, sticky=tk.W + tk.E)

        self.temp_unit_var = tk.StringVar()
        self.temp_unit_var.set("metric")

        self.radio_celsius = ttk.Radiobutton(frame, text="Celsius", variable=self.temp_unit_var, value="metric")
        self.radio_celsius.grid(row=4, column=0, pady=5, sticky=tk.W)

        self.radio_fahrenheit = ttk.Radiobutton(frame, text="Fahrenheit", variable=self.temp_unit_var, value="imperial")
        self.radio_fahrenheit.grid(row=4, column=1, pady=5, sticky=tk.W)

        self.weather_info_frame = ttk.Frame(frame, style="TFrame")
        self.weather_info_frame.grid(row=5, column=0, pady=10, sticky=tk.W)

        self.label_wind = ttk.Label(self.weather_info_frame, text="Wind Speed:", style="TLabel")
        self.label_wind.grid(row=0, column=0, pady=5, sticky=tk.W)

        self.label_humidity = ttk.Label(self.weather_info_frame, text="Humidity:", style="TLabel")
        self.label_humidity.grid(row=1, column=0, pady=5, sticky=tk.W)

    def get_weather(self):
        city = self.entry_city.get()

        if not city:
            messagebox.showwarning("Warning", "Enter the city name.")
            return

        def update():
            try:
                api_key = ''
                base_url = 'https://api.openweathermap.org/data/2.5/weather?q=London,uk&APPID='

                params = {
                    'q': city,
                    'appid': api_key,
                    'units': self.temp_unit_var.get()
                }

                response = requests.get(base_url, params=params)
                data = response.json()

                if response.status_code == 200:
                    weather_description = data['weather'][0]['description']
                    temperature = data['main']['temp']
                    wind_speed = data['wind']['speed']
                    humidity = data['main']['humidity']

                    weather_info = f"Weather Conditions: {weather_description}\nTemperature: {temperature}°"
                    self.weather_label.config(text=weather_info)

                    
                    self.label_wind.config(text=f"Wind Speed: {wind_speed} m/s")
                    self.label_humidity.config(text=f"Humidity: {humidity}%")
                else:
                    messagebox.showerror("Error", f"Error: {data['message']}")
            except Exception as e:
                messagebox.showerror("Error", f"Error: {str(e)}")

     
        thread = threading.Thread(target=update)
        thread.start()


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
