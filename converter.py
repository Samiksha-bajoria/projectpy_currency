import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime

class CurrencyConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Live Currency Converter")
        self.root.geometry("450x450")
        
        # API Configuration
        self.api_url = "https://api.exchangerate-api.com/v4/latest/USD"
        self.data = self.get_live_data()
        self.currencies = sorted(list(self.data['rates'].keys()))

        self.setup_ui()

    def get_live_data(self):
        try:
            response = requests.get(self.api_url)
            data = response.json()
            return data
        except:
            messagebox.showerror("Error", "Check your connection!")
            return None

    def setup_ui(self):
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True)

        # Last Updated Timestamp
        last_updated = self.data.get('time_last_updated', 0)
        dt_object = datetime.fromtimestamp(last_updated)
        tk.Label(main_frame, text=f"Rates Updated: {dt_object.strftime('%Y-%m-%d %H:%M')}", 
                 font=("Arial", 8, "italic")).grid(row=0, column=0, columnspan=2, pady=5)

        # Input Amount
        tk.Label(main_frame, text="Amount:").grid(row=1, column=0, sticky="w")
        self.amount_entry = tk.Entry(main_frame, font=("Arial", 12))
        self.amount_entry.grid(row=1, column=1, pady=10)

        # From Selection
        tk.Label(main_frame, text="From:").grid(row=2, column=0, sticky="w")
        self.from_curr = ttk.Combobox(main_frame, values=self.currencies, width=17)
        self.from_curr.set("USD")
        self.from_curr.grid(row=2, column=1, pady=5)

        # Swap Button
        self.swap_btn = tk.Button(main_frame, text="⇅ Swap", command=self.swap)
        self.swap_btn.grid(row=3, column=1, pady=5)

        # To Selection
        tk.Label(main_frame, text="To:").grid(row=4, column=0, sticky="w")
        self.to_curr = ttk.Combobox(main_frame, values=self.currencies, width=17)
        self.to_curr.set("EUR")
        self.to_curr.grid(row=4, column=1, pady=5)

        # Buttons Container
        btn_frame = tk.Frame(main_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)

        self.convert_btn = tk.Button(btn_frame, text="Convert", command=self.convert, 
                                    bg="#0078D7", fg="white", font=("Arial", 11, "bold"), width=10)
        self.convert_btn.pack(side="left", padx=5)

        self.clear_btn = tk.Button(btn_frame, text="Clear", command=self.clear_fields, 
                                  bg="#f44336", fg="white", font=("Arial", 11), width=10)
        self.clear_btn.pack(side="left", padx=5)

        # Result
        self.result_label = tk.Label(main_frame, text="", font=("Arial", 16, "bold"))
        self.result_label.grid(row=6, column=0, columnspan=2)

    def swap(self):
        f, t = self.from_curr.get(), self.to_curr.get()
        self.from_curr.set(t)
        self.to_curr.set(f)
        if self.amount_entry.get(): self.convert()

    def clear_fields(self):
        self.amount_entry.delete(0, tk.END)
        self.result_label.config(text="")

    def convert(self):
        try:
            amount = float(self.amount_entry.get())
            # Convert to USD base then to target
            usd_val = amount / self.data['rates'][self.from_curr.get()]
            result = usd_val * self.data['rates'][self.to_curr.get()]
            self.result_label.config(text=f"{result:,.2f} {self.to_curr.get()}", fg="#2E7D32")
        except ValueError:
            messagebox.showwarning("Error", "Please enter a numeric amount.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverter(root)
    root.mainloop()