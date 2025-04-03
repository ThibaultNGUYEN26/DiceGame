import os
import random
import time
import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict
import threading
from PIL import Image, ImageTk

class DiceGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Dice Game")
        self.root.geometry("800x600")
        self.root.configure(bg="#282c34")
        self.root.resizable(False, False)
        
        # Game state
        self.money = 500
        self.stats = {"games_played": 0, "wins": 0, "losses": 0, "biggest_win": 0}
        self.history = []
        self.bet = 0
        self.bet_type = None
        self.choose_low_high = None
        self.choose_number = None
        
        # Load dice images
        self.dice_images = []
        for i in range(1, 7):
            # Create dice images programmatically
            img = self._create_dice_image(i)
            self.dice_images.append(ImageTk.PhotoImage(img))
        
        # Create widgets
        self._create_widgets()
        
    def _create_dice_image(self, value):
        """Create a dice image programmatically"""
        img_size = 100
        img = Image.new('RGBA', (img_size, img_size), (255, 255, 255, 0))
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        
        # Draw dice outline
        draw.rounded_rectangle([(0, 0), (img_size-1, img_size-1)], radius=10, 
                              fill='white', outline='black', width=2)
        
        # Draw pips based on value
        pip_color = '#222'
        pip_size = 12
        
        # Positions for the pips
        positions = {
            1: [(img_size//2, img_size//2)],
            2: [(img_size//4, img_size//4), (3*img_size//4, 3*img_size//4)],
            3: [(img_size//4, img_size//4), (img_size//2, img_size//2), (3*img_size//4, 3*img_size//4)],
            4: [(img_size//4, img_size//4), (img_size//4, 3*img_size//4), 
                (3*img_size//4, img_size//4), (3*img_size//4, 3*img_size//4)],
            5: [(img_size//4, img_size//4), (img_size//4, 3*img_size//4), (img_size//2, img_size//2),
                (3*img_size//4, img_size//4), (3*img_size//4, 3*img_size//4)],
            6: [(img_size//4, img_size//4), (img_size//4, img_size//2), (img_size//4, 3*img_size//4),
                (3*img_size//4, img_size//4), (3*img_size//4, img_size//2), (3*img_size//4, 3*img_size//4)]
        }
        
        # Draw pips for the current value
        for pos in positions[value]:
            draw.ellipse([pos[0]-pip_size//2, pos[1]-pip_size//2, pos[0]+pip_size//2, pos[1]+pip_size//2], fill=pip_color)
        
        return img
        
    def _create_widgets(self):
        """Create all widgets for the game interface"""
        # Game title
        title_frame = tk.Frame(self.root, bg="#282c34")
        title_frame.pack(pady=10)
        
        title_label = tk.Label(
            title_frame,
            text="Dice Game",
            font=("Arial", 24, "bold"),
            fg="#61afef",
            bg="#282c34"
        )
        title_label.pack()
        
        # Main content frame with two columns
        main_frame = tk.Frame(self.root, bg="#282c34")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left column - Game Play
        self.game_frame = tk.Frame(main_frame, bg="#282c34", width=400)
        self.game_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.game_frame.pack_propagate(False)
        
        # Right column - Stats and History
        self.stats_frame = tk.Frame(main_frame, bg="#21252b", width=400)
        self.stats_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.stats_frame.pack_propagate(False)
        
        # Balance display
        balance_frame = tk.Frame(self.game_frame, bg="#282c34")
        balance_frame.pack(pady=10)
        
        balance_label = tk.Label(
            balance_frame, 
            text="Current Balance:", 
            font=("Arial", 14),
            fg="#abb2bf",
            bg="#282c34"
        )
        balance_label.pack(side=tk.LEFT)
        
        self.balance_value = tk.Label(
            balance_frame, 
            text=f"${self.money}", 
            font=("Arial", 14, "bold"),
            fg="#98c379",
            bg="#282c34"
        )
        self.balance_value.pack(side=tk.LEFT, padx=5)
        
        # Dice display
        self.dice_frame = tk.Frame(self.game_frame, bg="#282c34", height=120)
        self.dice_frame.pack(pady=10)
        
        self.dice_labels = []
        for i in range(2):
            label = tk.Label(self.dice_frame, image=self.dice_images[0], bg="#282c34")
            label.pack(side=tk.LEFT, padx=10)
            self.dice_labels.append(label)
            
        # Result display
        self.result_frame = tk.Frame(self.game_frame, bg="#282c34")
        self.result_frame.pack(pady=5)
        
        self.result_label = tk.Label(
            self.result_frame,
            text="",
            font=("Arial", 16, "bold"),
            bg="#282c34",
            fg="#61afef"
        )
        self.result_label.pack()
        
        # Betting options
        betting_frame = tk.LabelFrame(
            self.game_frame, 
            text="Betting Options", 
            font=("Arial", 12),
            fg="#c678dd",
            bg="#282c34", 
            bd=2
        )
        betting_frame.pack(pady=10, fill=tk.X, padx=20)
        
        # Bet amount
        bet_amount_frame = tk.Frame(betting_frame, bg="#282c34")
        bet_amount_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            bet_amount_frame, 
            text="Bet Amount: $", 
            font=("Arial", 12),
            fg="#abb2bf",
            bg="#282c34"
        ).pack(side=tk.LEFT)
        
        self.bet_amount = tk.Scale(
            bet_amount_frame,
            from_=1,
            to=self.money,
            orient=tk.HORIZONTAL,
            length=200,
            bg="#282c34",
            fg="#abb2bf",
            highlightthickness=0,
            troughcolor="#21252b"
        )
        self.bet_amount.set(10)
        self.bet_amount.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Bet type selection
        bet_type_frame = tk.Frame(betting_frame, bg="#282c34")
        bet_type_frame.pack(fill=tk.X, pady=5)
        
        self.bet_type_var = tk.IntVar(value=1)
        
        tk.Radiobutton(
            bet_type_frame,
            text="Low/High (2x payout)",
            variable=self.bet_type_var,
            value=1,
            command=self._update_betting_options,
            font=("Arial", 12),
            fg="#abb2bf",
            bg="#282c34",
            selectcolor="#21252b"
        ).pack(anchor=tk.W)
        
        tk.Radiobutton(
            bet_type_frame,
            text="Exact Number (6x payout, 8x for betting on 7)",
            variable=self.bet_type_var,
            value=2,
            command=self._update_betting_options,
            font=("Arial", 12),
            fg="#abb2bf",
            bg="#282c34",
            selectcolor="#21252b"
        ).pack(anchor=tk.W)
        
        # Low/High or Exact number options
        self.bet_options_frame = tk.Frame(betting_frame, bg="#282c34")
        self.bet_options_frame.pack(fill=tk.X, pady=5)
        
        self.low_high_var = tk.IntVar(value=1)
        self.number_var = tk.IntVar(value=7)
        
        # Low/High options (default)
        self.low_high_frame = tk.Frame(self.bet_options_frame, bg="#282c34")
        self.low_high_frame.pack(fill=tk.X)
        
        tk.Radiobutton(
            self.low_high_frame,
            text="Low (2-6)",
            variable=self.low_high_var,
            value=1,
            font=("Arial", 12),
            fg="#abb2bf",
            bg="#282c34",
            selectcolor="#21252b"
        ).pack(side=tk.LEFT, padx=20)
        
        tk.Radiobutton(
            self.low_high_frame,
            text="High (8-12)",
            variable=self.low_high_var,
            value=2,
            font=("Arial", 12),
            fg="#abb2bf",
            bg="#282c34",
            selectcolor="#21252b"
        ).pack(side=tk.LEFT, padx=20)
        
        # Exact number options (initially hidden)
        self.number_frame = tk.Frame(self.bet_options_frame, bg="#282c34")
        # Hidden initially: self.number_frame.pack(fill=tk.X)
        
        tk.Label(
            self.number_frame,
            text="Select a number (2-12):",
            font=("Arial", 12),
            fg="#abb2bf",
            bg="#282c34"
        ).pack(side=tk.LEFT)
        
        self.number_spinner = tk.Spinbox(
            self.number_frame,
            from_=2,
            to=12,
            width=3,
            textvariable=self.number_var,
            font=("Arial", 12),
            bg="#21252b",
            fg="#abb2bf"
        )
        self.number_spinner.pack(side=tk.LEFT, padx=10)
        
        # Game control buttons
        control_frame = tk.Frame(self.game_frame, bg="#282c34")
        control_frame.pack(pady=20, fill=tk.X)
        
        self.roll_button = tk.Button(
            control_frame,
            text="Roll Dice",
            command=self._play_round,
            font=("Arial", 14, "bold"),
            bg="#98c379",
            fg="#282c34",
            padx=20,
            pady=10,
            bd=0,
            cursor="hand2"
        )
        self.roll_button.pack(pady=10)
        
        # Stats section in right panel
        stats_header = tk.Label(
            self.stats_frame,
            text="Game Statistics",
            font=("Arial", 16, "bold"),
            fg="#61afef",
            bg="#21252b"
        )
        stats_header.pack(pady=10)
        
        self.stats_content = tk.Frame(self.stats_frame, bg="#21252b")
        self.stats_content.pack(fill=tk.X, padx=20, pady=5)
        
        # Stats labels
        stats_labels = [
            ("Games Played:", "games_played"),
            ("Wins:", "wins"),
            ("Losses:", "losses"),
            ("Win Rate:", "win_rate"),
            ("Biggest Win:", "biggest_win")
        ]
        
        self.stats_values = {}
        
        for label_text, key in stats_labels:
            frame = tk.Frame(self.stats_content, bg="#21252b")
            frame.pack(fill=tk.X, pady=2)
            
            tk.Label(
                frame,
                text=label_text,
                font=("Arial", 12),
                fg="#abb2bf",
                bg="#21252b",
                anchor="w",
                width=15
            ).pack(side=tk.LEFT)
            
            value_label = tk.Label(
                frame,
                text="0",
                font=("Arial", 12, "bold"),
                fg="#98c379" if "Win" in label_text else "#abb2bf",
                bg="#21252b",
                anchor="w"
            )
            value_label.pack(side=tk.LEFT, padx=5)
            self.stats_values[key] = value_label
        
        # Game history section
        history_header = tk.Label(
            self.stats_frame,
            text="Game History",
            font=("Arial", 16, "bold"),
            fg="#61afef",
            bg="#21252b"
        )
        history_header.pack(pady=(20, 10))
        
        history_frame = tk.Frame(self.stats_frame, bg="#21252b")
        history_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        
        # Scrollable history
        scrollbar = tk.Scrollbar(history_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_list = tk.Listbox(
            history_frame,
            bg="#282c34",
            fg="#abb2bf",
            font=("Arial", 11),
            bd=0,
            highlightthickness=0,
            selectbackground="#3e4451",
            height=10
        )
        self.history_list.pack(fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.history_list.yview)
        self.history_list.config(yscrollcommand=scrollbar.set)
        
        # Update stats
        self._update_stats_display()
        
    def _update_betting_options(self):
        """Update the betting options based on selected type"""
        bet_type = self.bet_type_var.get()
        
        # Clear current options
        for widget in self.bet_options_frame.winfo_children():
            widget.pack_forget()
        
        if bet_type == 1:
            self.low_high_frame.pack(fill=tk.X)
        else:
            self.number_frame.pack(fill=tk.X)
    
    def _play_round(self):
        """Play a round of the dice game"""
        # Get bet details
        self.bet = self.bet_amount.get()
        bet_type = self.bet_type_var.get()
        
        # Check if bet is valid
        if self.bet > self.money:
            messagebox.showerror("Invalid Bet", "You don't have enough money for that bet!")
            return
        
        # Disable roll button during roll
        self.roll_button.config(state=tk.DISABLED)
        
        # Update game stats
        self.stats["games_played"] += 1
        
        # Get bet settings
        if bet_type == 1:
            self.choose_low_high = self.low_high_var.get()
            self.choose_number = None
        else:
            self.choose_low_high = None
            self.choose_number = self.number_var.get()
        
        # Deduct bet from money
        self.money -= self.bet
        self._update_balance_display()
        
        # Start dice rolling animation
        threading.Thread(target=self._animate_dice_roll).start()
    
    def _animate_dice_roll(self):
        """Animate dice rolling"""
        result_display = self.result_label
        result_display.config(text="Rolling dice...")
        
        # Animate dice
        for _ in range(10):
            dice_values = [random.randint(1, 6) for _ in range(2)]
            for i, value in enumerate(dice_values):
                self.dice_labels[i].config(image=self.dice_images[value-1])
            self.root.update()
            time.sleep(0.1)
        
        # Final dice roll
        dice = [random.randint(1, 6) for _ in range(2)]
        result = sum(dice)
        
        # Update dice display
        for i, value in enumerate(dice):
            self.dice_labels[i].config(image=self.dice_images[value-1])
        
        # Determine outcome
        won = False
        winnings = 0
        
        if self.choose_low_high is not None:
            if (self.choose_low_high == 1 and result < 7) or (self.choose_low_high == 2 and result > 7):
                winnings = self.bet * 2
                won = True
        else:
            if self.choose_number == result:
                if self.choose_number == 7:
                    winnings = self.bet * 8
                else:
                    winnings = self.bet * 6
                won = True
        
        # Update money and display result
        if won:
            self.money += winnings
            self.stats["wins"] += 1
            self.stats["biggest_win"] = max(self.stats["biggest_win"], winnings)
            result_display.config(text=f"You won ${winnings}!", fg="#98c379")
        else:
            self.stats["losses"] += 1
            result_display.config(text=f"You lost ${self.bet}.", fg="#e06c75")
        
        # Add to history
        self.history.append({
            "bet": self.bet,
            "result": result,
            "won": won,
            "winnings": winnings if won else 0,
            "balance": self.money
        })
        
        # Update UI
        self._update_balance_display()
        self._update_stats_display()
        self._update_history_display()
        
        # Re-enable roll button
        self.roll_button.config(state=tk.NORMAL)
        
        # Check if game over
        if self.money <= 0:
            messagebox.showinfo("Game Over", "You're out of money! Game over.")
            self.roll_button.config(state=tk.DISABLED)
    
    def _update_balance_display(self):
        """Update the balance display"""
        self.balance_value.config(text=f"${self.money}")
        self.bet_amount.config(to=self.money)
        self.bet_amount.set(min(self.bet_amount.get(), self.money))
    
    def _update_stats_display(self):
        """Update the statistics display"""
        self.stats_values["games_played"].config(text=str(self.stats["games_played"]))
        self.stats_values["wins"].config(text=str(self.stats["wins"]))
        self.stats_values["losses"].config(text=str(self.stats["losses"]))
        
        win_rate = 0 if self.stats["games_played"] == 0 else (self.stats["wins"] / self.stats["games_played"]) * 100
        self.stats_values["win_rate"].config(text=f"{win_rate:.1f}%")
        self.stats_values["biggest_win"].config(text=f"${self.stats['biggest_win']}")
    
    def _update_history_display(self):
        """Update the history display"""
        # Clear listbox
        self.history_list.delete(0, tk.END)
        
        # Add history items (most recent first)
        for item in reversed(self.history):
            result_text = f"Win: ${item['winnings']}" if item["won"] else f"Loss: ${item['bet']}"
            self.history_list.insert(tk.END, f"Roll: {item['result']} - {result_text} - Balance: ${item['balance']}")
            
            # Color code wins and losses
            idx = self.history_list.size() - 1
            if item["won"]:
                self.history_list.itemconfig(idx, fg="#98c379")
            else:
                self.history_list.itemconfig(idx, fg="#e06c75")

if __name__ == "__main__":
    # Create main window
    root = tk.Tk()
    app = DiceGameGUI(root)
    root.mainloop()
