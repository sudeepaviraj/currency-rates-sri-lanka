import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO, BytesIO
import pdfplumber
import re

import csv
from datetime import datetime
import os

def save_daily_rates(cbsl, ntb, hsbc):
    file = "usd_rates_log.csv"
    today = datetime.now().strftime("%Y-%m-%d")

    def parse(rate):
        try:
            buy, sell = rate.split("/")
            return float(buy.strip()), float(sell.strip())
        except:
            return None, None

    data = [
        ("CBSL", *parse(cbsl)),
        ("NTB", *parse(ntb)),
        ("HSBC", *parse(hsbc)),
    ]

    file_exists = os.path.isfile(file)

    with open(file, mode="a", newline="") as f:
        writer = csv.writer(f)

        # Write header once
        if not file_exists:
            writer.writerow(["date", "source", "buy", "sell"])

        for source, buy, sell in data:
            writer.writerow([today, source, buy, sell])

# ---------------- CBSL ----------------
def get_cbsl():
    try:
        session = requests.Session()
        session.get("https://www.cbsl.gov.lk/cbsl_custom/exratestt/exratestt.php")

        response = session.post(
            'https://www.cbsl.gov.lk/cbsl_custom/exratestt/exrates_resultstt.php',
            data={
                "lookupPage": "lookup_daily_exchange_rates.php",
                "startRange": "2006-11-11",
                "rangeType": "dates",
                "txtStart": "2026-03-23",
                "txtEnd": "2026-03-23",
                "chk_cur[]": "USD~United States Dollar",
                "submit_button": "Submit"
            }
        )

        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find("table")

        df = pd.read_html(StringIO(str(table)))[0]

        buy = float(df.loc[0, 'Buy Rate (LKR)'])
        sell = float(df.loc[0, 'Sell Rate (LKR)'])

        return f"{buy:.2f} / {sell:.2f}"
    except:
        return "Error"


# ---------------- NTB ----------------
def get_ntb():
    try:
        response = requests.get(
            'https://www.nationstrust.com/foreign-exchange-rates',
            headers={"User-Agent": "Mozilla/5.0"}
        )

        soup = BeautifulSoup(response.text, 'html.parser')
        tds = soup.find_all("td")

        row_size = 8
        rows = []

        for i in range(0, len(tds), row_size):
            row = [td.get_text(strip=True) for td in tds[i:i+row_size]]
            rows.append(row)

        df = pd.DataFrame(rows, columns=[
            "Currency",
            "DD Buying", "DD Selling",
            "TT Buying", "TT Selling",
            "TT Buying 2", "TT Selling 2",
            "Import Bill Rate"
        ])

        usd = df[df["Currency"] == "USD"].iloc[0]

        return f"{usd['DD Buying']} / {usd['DD Selling']}"
    except:
        return "Error"


# ---------------- HSBC ----------------
def get_hsbc():
    try:
        import requests
        import pdfplumber
        from io import BytesIO
        import re

        url = "https://www.hsbc.lk/content/dam/hsbc/lk/documents/tariffs/foreign-exchange-rates.pdf"
        res = requests.get(url)

        with pdfplumber.open(BytesIO(res.content)) as pdf:

            for page in pdf.pages:
                text = page.extract_text()

                for line in text.split("\n"):
                    if "United States Dollar" in line:

                        print("RAW:", line)  # debug

                        # Extract ALL numeric parts (including broken ones)
                        raw_nums = re.findall(r"\d+\.?\d*", line)

                        # Rebuild numbers intelligently
                        fixed = []
                        i = 0

                        while i < len(raw_nums):
                            # Case: ["3", "07.11"] → merge
                            if (
                                i + 1 < len(raw_nums)
                                and len(raw_nums[i]) == 1
                                and "." in raw_nums[i+1]
                            ):
                                merged = raw_nums[i] + raw_nums[i+1]
                                fixed.append(merged)
                                i += 2
                            else:
                                fixed.append(raw_nums[i])
                                i += 1

                        # Now filter proper decimals only
                        decimals = [x for x in fixed if "." in x]

                        if len(decimals) >= 2:
                            buy = float(decimals[0])
                            sell = float(decimals[1])

                            return f"{buy} / {sell}"

        return "Not found"

    except Exception as e:
        print("HSBC error:", e)
        return "Error"
# ---------------- UI ----------------
# ---------------- UI ----------------
def update_rates():
    cbsl = get_cbsl()
    ntb = get_ntb()
    hsbc = get_hsbc()

    cbsl_var.set(cbsl)
    ntb_var.set(ntb)
    hsbc_var.set(hsbc)

    highlight_best(cbsl, ntb, hsbc)
    save_daily_rates(cbsl, ntb, hsbc)

    root.after(60000, update_rates)


# Highlight best BUY rate
def highlight_best(cbsl, ntb, hsbc):
    try:
        values = {}

        for name, val in [("CBSL", cbsl), ("NTB", ntb), ("HSBC", hsbc)]:
            buy = float(val.split("/")[0])
            values[name] = buy

        best = min(values, key=values.get)

        # Reset colors
        cbsl_label.configure(foreground="white")
        ntb_label.configure(foreground="white")
        hsbc_label.configure(foreground="white")

        # Highlight best
        if best == "CBSL":
            cbsl_label.configure(foreground="#00ff9c")
        elif best == "NTB":
            ntb_label.configure(foreground="#00ff9c")
        elif best == "HSBC":
            hsbc_label.configure(foreground="#00ff9c")

    except:
        pass


# ---------------- Window ----------------
root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)
root.attributes("-alpha", 0.80)

# ---------------- Position (top-right) ----------------
root.update_idletasks()
width = 260

x = root.winfo_screenwidth() - width - 10
y = 10

root.geometry(f"+{x}+{y}")

# ---------------- Style ----------------
style = ttk.Style()
style.theme_use("clam")

BG = "#121826"
CARD = "#1e293b"
ACCENT = "#38bdf8"
TEXT = "#e2e8f0"

style.configure("TFrame", background=BG)
style.configure("Card.TFrame", background=CARD)
style.configure("TLabel", background=CARD, foreground=TEXT)

# ---------------- Main Frame ----------------
frame = ttk.Frame(root, style="TFrame", padding=10)
frame.pack(fill="both", expand=True)

# ---------------- Dragging ----------------
def start_move(event):
    root.x = event.x_root
    root.y = event.y_root

def do_move(event):
    dx = event.x_root - root.x
    dy = event.y_root - root.y
    x = root.winfo_x() + dx
    y = root.winfo_y() + dy
    root.geometry(f"+{x}+{y}")
    root.x = event.x_root
    root.y = event.y_root

frame.bind("<Button-1>", start_move)
frame.bind("<B1-Motion>", do_move)

# ---------------- Header ----------------
header = ttk.Frame(frame, style="Card.TFrame")
header.pack(fill="x", pady=(0, 8))

ttk.Label(header, text="💱 USD Rates", font=("Segoe UI", 11, "bold"),
          foreground=ACCENT).pack(side="left")

ttk.Button(header, text="✕", command=root.destroy).pack(side="right")

# ---------------- Variables ----------------
cbsl_var = tk.StringVar(value="Loading...")
ntb_var = tk.StringVar(value="Loading...")
hsbc_var = tk.StringVar(value="Loading...")

# ---------------- Card builder ----------------
def create_row(parent, name, var):
    row = ttk.Frame(parent, style="Card.TFrame")
    row.pack(fill="x", pady=4)

    ttk.Label(row, text=name, width=6).pack(side="left")

    value_label = ttk.Label(row, textvariable=var, font=("Segoe UI", 10, "bold"))
    value_label.pack(side="right")

    return value_label

# ---------------- Rows ----------------
cbsl_label = create_row(frame, "CBSL", cbsl_var)
ntb_label = create_row(frame, "NTB", ntb_var)
hsbc_label = create_row(frame, "HSBC", hsbc_var)

# ---------------- Start ----------------
update_rates()

root.mainloop()