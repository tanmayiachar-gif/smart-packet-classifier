import tkinter as tk
from tkinter import messagebox
import pickle
import numpy as np
import csv
import os
import random

# Load model
with open('packet_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Global counter for result stats
prediction_counts = {
    'Normal': 0,
    'Video Stream': 0,
    'Suspicious': 0
}

# Motivational lines
quotes = [
    "📡 Staying secure, one packet at a time!",
    "🌐 Smart traffic scan completed!",
    "🚀 Packet analysis done like a pro!",
    "🧠 Network IQ: Activated.",
    "🛡️ Safety first, always!"
]

# Prediction label beautifier
def beautify_prediction(pred):
    if pred == "Normal":
        return "✅ Normal Traffic 🌐"
    elif pred == "Video Stream":
        return "🎬 Video Stream Detected"
    elif pred == "Suspicious":
        return "🚨 Suspicious Activity!"
    else:
        return "❌ Unknown Traffic Type"

# Save result to CSV
def save_to_csv(data, prediction):
    file_exists = os.path.isfile('packet_log.csv')
    with open('packet_log.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Flow Duration', 'Total Fwd Packets', 'Total Bwd Packets',
                             'Fwd Packet Length Mean', 'Bwd Packet Length Mean', 'Prediction'])
        writer.writerow(data + [prediction])

# GUI classify function
def classify_traffic():
    try:
        flow_duration = float(flow_duration_entry.get())
        total_fwd = int(total_fwd_entry.get())
        total_bwd = int(total_bwd_entry.get())
        fwd_len = float(fwd_len_entry.get())
        bwd_len = float(bwd_len_entry.get())

        features = [[flow_duration, total_fwd, total_bwd, fwd_len, bwd_len]]
        prediction = model.predict(features)[0]

        # Count
        if prediction in prediction_counts:
            prediction_counts[prediction] += 1

        # Save
        save_to_csv([flow_duration, total_fwd, total_bwd, fwd_len, bwd_len], prediction)

        # Show result
        result_label.config(text=beautify_prediction(prediction), fg="green", font=("Arial", 14, "bold"))
        quote_label.config(text=random.choice(quotes))

        # Update counter label
        counter_text = f"🧮 Count – Normal: {prediction_counts['Normal']} | Video: {prediction_counts['Video Stream']} | Suspicious: {prediction_counts['Suspicious']}"
        counter_label.config(text=counter_text)

    except ValueError:
        messagebox.showerror("Error", "❌ Please enter valid numbers in all fields.")

# GUI setup
root = tk.Tk()
root.title("✨ Smart Packet Classifier")
root.geometry("450x400")
root.configure(bg="#f0f4ff")

# Inputs
labels = ["Flow Duration", "Total Fwd Packets", "Total Bwd Packets", 
          "Fwd Packet Length Mean", "Bwd Packet Length Mean"]
entries = []

for i, label_text in enumerate(labels):
    tk.Label(root, text=label_text, bg="#f0f4ff", font=("Arial", 10)).grid(row=i, column=0, padx=10, pady=6, sticky="e")
    entry = tk.Entry(root)
    entry.grid(row=i, column=1, padx=10, pady=6)
    entries.append(entry)

flow_duration_entry, total_fwd_entry, total_bwd_entry, fwd_len_entry, bwd_len_entry = entries

# Button
tk.Button(root, text="🚀 Classify Traffic", command=classify_traffic, bg="#aee1f9", font=("Arial", 11, "bold")).grid(row=6, column=0, columnspan=2, pady=15)

# Result
result_label = tk.Label(root, text="", bg="#f0f4ff", font=("Arial", 12))
result_label.grid(row=7, column=0, columnspan=2)

# Motivational quote
quote_label = tk.Label(root, text="", bg="#f0f4ff", fg="#666", font=("Arial", 10, "italic"))
quote_label.grid(row=8, column=0, columnspan=2, pady=5)

# Counter
counter_label = tk.Label(root, text="", bg="#f0f4ff", font=("Arial", 10))
counter_label.grid(row=9, column=0, columnspan=2, pady=5)

root.mainloop()
