import tkinter as tk
from tkinter import messagebox, font
import random
import time
from datetime import datetime
from playsound import playsound
from load_names import names_to_import
from load_prizes import prizes_to_import
from load_consolation_prize import consolation_prize_to_import


class RaffleDrawApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BSIS Christmas Raffle")
        self.root.configure(bg="#ADD8E6")

        current_date = datetime.now()
        self.formatted_date = current_date.strftime("%B %d, %Y")

        self.participants = names_to_import
        self.prizes = prizes_to_import
        self.consolation_prizes = consolation_prize_to_import

        left_frame = tk.Frame(root, bg="#ADD8E6", padx=10, pady=10)
        left_frame.grid(row=0, column=0, sticky="nsew")

        right_frame = tk.Frame(root, bg="#ADD8E6", padx=10, pady=10)
        right_frame.grid(row=0, column=1, sticky="nsew")

        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)

        # Define custom fonts
        self.title_font = font.Font(family="Helvetica", size=14, weight="bold")
        self.label_font = font.Font(family="Helvetica", size=12)
        self.button_font = font.Font(family="Helvetica", size=12, weight="bold")

        self.raffle_label = tk.Label(left_frame, text=f"BSIS Christmas Raffle\nDate: {self.formatted_date}",
                                     bg="#ADD8E6", font=self.title_font)
        self.raffle_label.grid(row=0, column=0, pady=5)

        self.winners_label = tk.Label(left_frame, text="Number of Winners:", bg="#ADD8E6", font=self.label_font)
        self.winners_label.grid(row=1, column=0, pady=5)

        self.winners_entry = tk.Entry(left_frame, width=10, font=self.label_font)
        self.winners_entry.grid(row=1, column=1, pady=5)
        self.winners_entry.insert(0, "3")

        self.consolation_label = tk.Label(left_frame, text="Number of Consolation Prizes:", bg="#ADD8E6", font=self.label_font)
        self.consolation_label.grid(row=2, column=0, pady=5)

        self.consolation_entry = tk.Entry(left_frame, width=10, font=self.label_font)
        self.consolation_entry.grid(row=2, column=1, pady=5)
        self.consolation_entry.insert(0, "4")

        self.participants_label = tk.Label(left_frame, text="Participants:", bg="#ADD8E6", font=self.label_font)
        self.participants_label.grid(row=3, column=0, pady=5)

        self.participants_frame = tk.Frame(left_frame, bg="#ADD8E6")
        self.participants_frame.grid(row=4, column=0, pady=5)

        self.populate_participants()

        self.prizes_label = tk.Label(left_frame, text="Prizes:", bg="#ADD8E6", font=self.label_font)
        self.prizes_label.grid(row=5, column=0, pady=5, sticky="w")

        self.prizes_list_label = tk.Label(left_frame, text="\n".join(self.prizes), bg="#ADD8E6", justify="left", font=self.label_font)
        self.prizes_list_label.grid(row=6, column=0, pady=5, sticky="w")

        self.consolation_label = tk.Label(left_frame, text="Consolation Prizes:", bg="#ADD8E6", font=self.label_font)
        self.consolation_label.grid(row=7, column=0, pady=5 , sticky="w")

        self.consolation_list_label = tk.Label(left_frame, text="\n".join(self.consolation_prizes), bg="#ADD8E6",
                                               justify="left", font=self.label_font)
        self.consolation_list_label.grid(row=8, column=0, pady=5, sticky="w")

        self.instructions_label = tk.Label(left_frame, text=(
            "Instructions:\n"
            "1. Enter the number of winners and consolation prizes.\n"
            "2. Click 'Start Draw' to begin the raffle.\n"
            "3. Results will be saved to 'raffle_results.txt'."),
                                           bg="#ADD8E6", justify="left")
        self.instructions_label.grid(row=9, column=0, pady=10, sticky="w")

        # Move the draw button to the right_frame
        self.draw_button = tk.Button(right_frame, text="Start Draw", command=self.draw_all_winners, font=self.button_font)
        self.draw_button.grid (row=1, column=0, pady=10)

        self.canvas = tk.Canvas(right_frame, width=400, height=400, bg="#FFFFFF")
        self.canvas.grid(row=0, column=0, padx=10, pady=10)

        self.winner_frame = tk.Frame(root, bg="#ADD8E6", padx=10, pady=10)
        self.winner_frame.grid(row=1, column=1, sticky="nsew")

        self.current_winner_index = 0
        self.winners = []
        self.consolation_recipients = []

    def generate_random_color(self):
        return "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def populate_participants(self):
        for widget in self.participants_frame.winfo_children():
            widget.destroy()

        row, col = 0, 0
        for participant in self.participants:
            random_color = self.generate_random_color()
            participant_button = tk.Button(self.participants_frame, text=participant, width=20, height=2,
                                           bg=random_color, font=self.label_font)
            participant_button.grid(row=row, column=col, padx=5, pady=5)

            col += 1
            if col > 2:
                col = 0
                row += 1

    def draw_all_winners(self):
        playsound('spin.mp3', block=False)
        try:
            num_winners = int(self.winners_entry.get())
            num_consolation = int(self.consolation_entry.get())
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter valid numbers for winners and consolation prizes.")
            return

        if num_winners < 1 or num_consolation < 1:
            messagebox.showwarning("Invalid Input", "There must be at least 1 winner and 1 consolation prize.")
            return

        if len(self.participants) < num_winners + num_consolation:
            messagebox.showwarning("Not Enough Participants",
                                   "There are not enough participants to draw the requested number of winners and consolation prizes.")
            return

        for widget in self.winner_frame.winfo_children():
            widget.destroy()

        self.current_winner_index = 0
        self.winners = []
        self.consolation_recipients = []

        # Show the next winner button
        self.next_winner_button = tk.Button(self.winner_frame, text="Next Winner", command=self.spin_for_winner, font=self.button_font)
        self.next_winner_button.grid(row=1, column=0, pady=10)

        self.spin_for_winner()

    def spin_for_winner(self):
        playsound('spin.mp3', block=False)
        if self.current_winner_index < int(self.winners_entry.get()):
            self.animate_spinner()
            winner = random.choice(self.participants)
            prize = self.prizes[self.current_winner_index]
            self.winners.append((winner, prize))
            self.participants.remove(winner)

            self.populate_participants()
            playsound('winner.mp3', block=False)
            winner_label = tk.Label(self.winner_frame, text=f"{winner}: {prize}", bg="#ADD8E6", font=self.label_font)
            winner_label.grid(row=2 + self.current_winner_index, column=0, pady=5)

            messagebox.showinfo("Winner", f"Winner {self.current_winner_index + 1}: {winner}\nPrize: {prize}")

            self.current_winner_index += 1
        else:
            self.draw_consolation_prizes()

    def draw_consolation_prizes(self):
        if not self.consolation_prizes:
            messagebox.showinfo("All Prizes Drawn", "All winners and consolation prizes have been drawn!")
            self.save_results(self.winners, self.consolation_recipients)
            return

        for idx in range(int(self.consolation_entry.get())):
            playsound('spin.mp3', block=False)
            if self.participants:
                self.animate_spinner()
                consolation_recipient = random.choice(self.participants)
                consolation_prize = self.consolation_prizes.pop(0)
                self.consolation_recipients.append((consolation_recipient, consolation_prize))
                self.participants.remove(consolation_recipient)

                self.populate_participants()
                playsound('winner.mp3', block=False)
                messagebox.showinfo("Consolation Prize",
                                    f"Consolation Prize {idx + 1}: {consolation_recipient}\nPrize: {consolation_prize}")

        self.save_results(self.winners, self.consolation_recipients)

    def animate_spinner(self):
        for _ in range(30):
            random_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
            self.canvas.delete("all")
            self.canvas.create_arc(10, 10, 380, 380, start=random.randint(0, 360),
                                   extent=120, fill=random_color)
            self.root.update()
            time.sleep(0.1)

    def save_results(self, winners, consolation_recipients):
        try:
            with open("raffle_results.txt", "a") as file:
                file.write(f"Raffle Date: {self.formatted_date}\n")
                file.write("Top Winners:\n")
                for winner, prize in winners:
                    file.write(f"{winner}: {prize}\n")

                file.write("\n" + "=" * 30 + "\n")
                file.write("Consolation Prizes:\n")
                for recipient, prize in consolation_recipients:
                    file.write(f"{recipient}: {prize}\n")

                file.write("\n" + "=" * 30 + "\n")
            playsound('success.mp3', block=False)
            messagebox.showinfo("Saved", "Results have been saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the results: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = RaffleDrawApp(root)
    root.mainloop()