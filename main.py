from tkinter import *
from tkinter import ttk, Text
from words_dict import words
import random

class Type_speed_test:
    def __init__(self) -> None:
        self.root = Tk()
        self.root.geometry("500x300")
        self.root.title("Typing Speed Test")
        self.frm = ttk.Frame(self.root, padding=10)
        self.frm.grid()
        self.style = ttk.Style()

        # words per minute
        self.wpm = 0
        self.wpm_label = ttk.Label(text=f"WPM: {self.wpm}")
        self.wpm_label.grid(row=0, column=1, padx=5, pady=5)
        
        self.cpm = 0
        self.cpm_label = ttk.Label(text=f"CPM: {self.cpm}")
        self.cpm_label.grid(row=0, column=2, padx=5, pady=5)

        # timer
        self.timer = None
        # time label
        self.time_label = ttk.Label(text="Time: 00:00")
        self.time_label.grid(row=0, column=3, padx=15, pady=5)

        # Word Paragraph
        self.word_list_shuffled = words
        init_passage = " ".join(self.word_list_shuffled)
        self.passage_text = Text(self.root,width=65, height=15, wrap= "word")
        self.passage_text.grid(row=1, column=0, columnspan=4, padx=20, pady=5)
        self.passage_text.insert(1.0, chars=init_passage)
        self.passage_text.config(state=DISABLED)

        # Test to highlight text on press of a button
        self.current_word = 0
        self.current_index=("1.-1", "1.-1")
        self.text_tag = "word_tag"

        self.style.configure('TEntry', background='white')
        input_word = StringVar()
        self.input_word_entry = ttk.Entry(textvariable=input_word, state='disabled', justify = CENTER, style='TEntry')
        self.input_word_entry.grid(row=3, column=0, columnspan=4, padx=20, pady=5)
        self.input_word_entry.bind("<Key>", self.char_entered)

        self.start_restart_button = ttk.Button(text="Start/Restart", command=self.restart_test)
        self.start_restart_button.grid(row=0, column=0, padx=20, pady=5)

    # count words per minute
    def count_words_per_minute(self, word):
        if word == self.word_list_shuffled[self.wpm]:
            self.cpm += 1
        self.wpm += 1
        self.wpm_label.config(text=f"WPM: {self.wpm}")
        self.cpm_label.config(text=f"CPM: {self.cpm}")

    # display words per minute
    def display_count_per_minute(self):
        self.update_time_label(1, 0)
        self.input_word_entry.config(state='disabled')
        self.wpm_label.config(text=f"WPM: {self.wpm}")
        self.cpm_label.config(text=f"CPM: {self.cpm}")
        self.input_word_entry.delete(0,END)
        self.passage_text.tag_remove(self.text_tag, "1.0", "end")


    # timer
    def update_time_label(self, mins, secs):
        self.time_label.config(text=f"Time: {mins:02}:{secs:02}")
        self.time_label.update()

    def start_restart_timer(self, timer_value_in_seconds):
        mins, secs = divmod(timer_value_in_seconds, 60)
        self.update_time_label(mins, secs)
        if timer_value_in_seconds > 1:
            self.timer = self.root.after(1000, self.start_restart_timer, timer_value_in_seconds - 1)
        else:
            self.display_count_per_minute()
    
    # shuffle passage
    def shuffle_passage(self):
        shuffled_words = self.word_list_shuffled
        random.shuffle(shuffled_words)
        self.word_list_shuffled = shuffled_words
        shuffled_passage =  " ".join(self.word_list_shuffled)
        self.passage_text.config(state="normal")
        self.passage_text.delete("1.0")
        self.passage_text.insert("1.0", shuffled_passage)
        self.passage_text.config(state="disabled")

    # highlight text
    def highlight_next(self):
        self.passage_text.tag_remove(self.text_tag, self.current_index[0], self.current_index[1])
        next_index_start = "1." + str(int(self.current_index[1].split(".")[1]) + 1)
        next_index_end = "1." + str(int(self.current_index[1].split(".")[1]) + 1 + len(self.word_list_shuffled[self.current_word]))
        self.passage_text.tag_add(self.text_tag, next_index_start, next_index_end)
        self.passage_text.tag_config(self.text_tag, background= "yellow", foreground= "black")
        self.current_index = [next_index_start, next_index_end]
        self.current_word += 1
        
    # Input Entry field
    def char_entered(self, key):
        if key.char == " ":
            current_input_word = self.input_word_entry.get().replace(" ", "")
            self.count_words_per_minute(current_input_word)
            self.input_word_entry.delete(0,END)
            self.highlight_next()
            return

    # Start and Restart text
    def restart_test(self):
        if self.timer is not None:
            self.root.after_cancel(self.timer)
        self.start_restart_timer(60)
        self.shuffle_passage()
        self.current_word = 0
        self.current_index=("1.-1", "1.-1")
        self.passage_text.tag_remove(self.text_tag, "1.0", "end")
        self.highlight_next()
        self.input_word_entry.config(state='normal')
        self.cpm = 0
        self.wpm = 0

typing_test = Type_speed_test()
typing_test.root.mainloop()
