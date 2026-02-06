import tkinter as tk

# ---------------- DATA ----------------
MENU = {
    "Margherita Pizza": 250,
    "Veg Burger": 180,
    "Pasta Alfredo": 220,
    "Paneer Tikka": 260,
    "Cold Coffee": 120
}

AVAILABILITY = {
    "2026-02-07": {"18:00": 10, "19:00": 6, "20:00": 4},
    "2026-02-08": {"18:00": 8, "19:00": 5, "20:00": 2}
}

USER_MEMORY = {}

user_name = ""
current_step = "ask_name"
booking = {}

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("Smart Dine Chatbot")
root.geometry("620x520")
root.configure(bg="#FFF1F2")

# ---------------- WELCOME PAGE ----------------
welcome_frame = tk.Frame(root, bg="#FFF1F2")
welcome_frame.pack(fill=tk.BOTH, expand=True)

tk.Label(
    welcome_frame,
    text="🍽 SMART DINE 🍽",
    font=("Helvetica", 26, "bold"),
    bg="#FFF1F2",
    fg="#C2185B"
).pack(pady=40)

tk.Label(
    welcome_frame,
    text="Your friendly dining reservation chatbot 🤖\n"
         "Book tables • Check availability • View summaries",
    font=("Helvetica", 13),
    bg="#FFF1F2",
    fg="#4A148C"
).pack(pady=20)


def open_chat():
    welcome_frame.pack_forget()
    chat_frame.pack(fill=tk.BOTH, expand=True)
    bot("👋 Hi! Welcome to Smart Dine 😊")
    bot("What's your name?")


tk.Button(
    welcome_frame,
    text="✨ Start Chatting ✨",
    font=("Helvetica", 14, "bold"),
    bg="#EC407A",
    fg="white",
    padx=25,
    pady=12,
    command=open_chat
).pack(pady=40)

# ---------------- CHATBOT PAGE ----------------
chat_frame = tk.Frame(root, bg="#FFFDE7")

chat = tk.Text(
    chat_frame,
    font=("Arial", 11),
    bg="white",
    fg="#263238",
    wrap=tk.WORD
)
chat.pack(padx=12, pady=12, expand=True, fill=tk.BOTH)

entry = tk.Entry(chat_frame, font=("Arial", 12))
entry.pack(fill=tk.X, padx=12, pady=6)


# ---------------- CHAT HELPERS ----------------
def bot(msg):
    chat.insert(tk.END, f"🤖 Bot: {msg}\n")
    chat.see(tk.END)


def user(msg):
    chat.insert(tk.END, f"🧑 You: {msg}\n")
    chat.see(tk.END)


# ---------------- CHAT LOGIC ----------------
def process_message():
    global user_name, current_step

    msg = entry.get().strip()
    entry.delete(0, tk.END)

    if not msg:
        return

    user(msg)

    if current_step == "ask_name":
        user_name = msg
        USER_MEMORY.setdefault(user_name, [])
        bot(f"Nice to meet you, {user_name}! 😊")
        bot("How can I help you today?\nMenu | Availability | Book | Summary | History")
        current_step = "idle"

    elif current_step == "idle":
        text = msg.lower()

        if "menu" in text:
            bot("🍽 Here's our menu:")
            for item, price in MENU.items():
                bot(f"{item} – ₹{price}")

        elif "availability" in text:
            bot("Sure 😊 Which date are you planning? (e.g., 2026-02-07)")
            current_step = "check_date"

        elif "book" in text:
            bot("Great! Let's book a table 🍽")
            bot("Which date? (e.g., 2026-02-07)")
            current_step = "book_date"

        elif "summary" in text:
            if USER_MEMORY[user_name]:
                r = USER_MEMORY[user_name][-1]
                bot(f"🧾 Your last booking was on {r['date']} at {r['time']} for {r['seats']} seats.")
            else:
                bot("You don't have any bookings yet.")

        elif "history" in text:
            if USER_MEMORY[user_name]:
                bot("📖 Your booking history:")
                for i, r in enumerate(USER_MEMORY[user_name], 1):
                    bot(f"{i}. {r['date']} at {r['time']} – {r['seats']} seats")
            else:
                bot("No booking history yet.")

        elif "exit" in text:
            bot("👋 Thanks for using Smart Dine! See you soon 💖")
            root.after(1200, root.destroy)

        else:
            bot("I can help with Menu, Availability, Booking, Summary or History 😊")

    elif current_step == "check_date":
        date = msg
        if date in AVAILABILITY:
            bot(f"Available slots on {date}:")
            for t, s in AVAILABILITY[date].items():
                bot(f"{t} → {s} seats")
        else:
            bot("Sorry, no availability on that date 😕")
            bot("📅 Here are our available dates:")
            for available_date in AVAILABILITY.keys():
                bot(f"• {available_date}")
        current_step = "idle"

    elif current_step == "book_date":
        booking["date"] = msg
        if msg in AVAILABILITY:
            bot(f"Great! Available times on {msg}:")
            for t, s in AVAILABILITY[msg].items():
                bot(f"{t} → {s} seats available")
            bot("What time would you prefer?")
            current_step = "book_time"
        else:
            bot("Sorry, we don't have availability on that date 😕")
            bot("📅 Here are our available dates:")
            for available_date in AVAILABILITY.keys():
                bot(f"• {available_date}")
            bot("Please try one of these dates:")
            current_step = "book_date"

    elif current_step == "book_time":
        booking["time"] = msg
        bot("How many seats do you need?")
        current_step = "book_seats"

    elif current_step == "book_seats":
        try:
            seats = int(msg)
        except ValueError:
            bot("Please enter a valid number of seats 🙂")
            return

        date = booking["date"]
        time = booking["time"]

        # ✅ FIXED: Check if date and time exist before checking seats
        if date not in AVAILABILITY:
            bot("❌ Sorry, that date is not available 😕")
            booking.clear()
            current_step = "idle"
            return

        if time not in AVAILABILITY[date]:
            bot("❌ That time slot is not available 😕")
            bot("Available times on this date:")
            for t, s in AVAILABILITY[date].items():
                bot(f"• {t} → {s} seats available")
            bot("Please choose one of these times ⏰")
            current_step = "book_time"
            return

        if AVAILABILITY[date][time] >= seats:
            # Booking successful
            AVAILABILITY[date][time] -= seats
            USER_MEMORY[user_name].append({
                "date": date,
                "time": time,
                "seats": seats
            })
            bot("✅ Your table has been booked successfully! 🎉")
            bot(f"{date} at {time} for {seats} seats 🍽️")
            booking.clear()
            current_step = "idle"
        else:
            # Not enough seats at this time
            bot(f"❌ Sorry, only {AVAILABILITY[date][time]} seats available at {time} 😕")

            # Find alternative slots on the same day
            available_slots = [(t, s) for t, s in AVAILABILITY[date].items() if s >= seats]

            if available_slots:
                bot("✅ Here are other available times on the same day:")
                for t, s in available_slots:
                    bot(f"• {t} → {s} seats available")
                bot("Please choose one of these times ⏰")
                current_step = "book_time"
            else:
                bot("Sorry, no slots with enough seats are available on this date 😔")
                booking.clear()
                current_step = "idle"


# ---------------- SEND BUTTON ----------------
tk.Button(
    chat_frame,
    text="Send",
    font=("Helvetica", 12, "bold"),
    bg="#EC407A",
    fg="white",
    command=process_message
).pack(pady=6)

# Bind Enter key to send message
entry.bind("<Return>", lambda e: process_message())

# ---------------- RUN ----------------
root.mainloop()