import pyfirmata2 as pyfirmata
import time
import json
import tkinter as tk
from tkinter import ttk
import threading



with open('values.json', 'r') as file:
    vars = json.load(file)

arduino = vars['values']['arduino']['port']

board = pyfirmata.Arduino(f"{arduino}")
board.samplingOn(1000)

people_in_que = 0
state = 'leeg'

is_green_blinking = False
is_red_blinking = False
is_yellow_blinking = False

empty_mark = vars['values']['watermarks']['empty_mark']
low_mark = vars['values']['watermarks']['low_mark']
high_mark = vars['values']['watermarks']['high_mark']
full_mark = vars['values']['watermarks']['full_mark']
overload_mark = vars['values']['watermarks']['overload_mark']

red_pin = vars['values']['pinout']['red_led']
yellow_pin = vars['values']['pinout']['yellow_led']
green_pin = vars['values']['pinout']['green_led']

red_led = board.get_pin(f'd:{red_pin}:o')
yellow_led = board.get_pin(f'd:{yellow_pin}:o')
green_led = board.get_pin(f'd:{green_pin}:o')



def blink_red_led():
    while is_red_blinking:
        red_led.write(1)
        time.sleep(0.5)
        red_led.write(0)
        time.sleep(0.5)

def blink_yellow_led():
    while is_yellow_blinking:
        yellow_led.write(1)
        time.sleep(0.5)
        yellow_led.write(0)
        time.sleep(0.5)

def blink_green_led():
    while is_green_blinking:
        green_led.write(1)
        time.sleep(0.5)
        green_led.write(0)
        time.sleep(0.5)

def print_tick(to_print, interval):
    print(f'Status wachtrij: {to_print}')
    time.sleep(interval)

def check_amount_people(people):
    global overload_mark, full_mark, high_mark, low_mark, empty_mark
    if people < empty_mark:
        status = 'leeg'
    elif empty_mark <= people < low_mark:
        status = 'zo goed als leeg'
    elif low_mark <= people < high_mark:
        status = 'gevuld'
    elif high_mark <= people_in_que < full_mark:
        status = 'bijna vol'
    elif full_mark <= people_in_que < overload_mark:
        status = 'vol'
    elif people_in_que >= overload_mark:
        status = 'overload'
    elif people_in_que == 0:
        status = 'leeg'
    if status:
        return status
    else:
        status = 'leeg'
        return status

def led_on(led, blinking):
    global is_red_blinking, is_yellow_blinking, is_green_blinking
    if led == 'green' and not blinking:
        green_led.write(1)
        yellow_led.write(0)
        red_led.write(0)
        is_red_blinking = False
        is_yellow_blinking = False
        is_green_blinking = False
    if led == 'green' and blinking:
        if not is_green_blinking:
            is_green_blinking = True
            threading.Thread(target=blink_green_led, daemon=True).start()
    elif led == 'yellow' and not blinking:
        green_led.write(0)
        yellow_led.write(1)
        red_led.write(0)
        is_red_blinking = False
        is_yellow_blinking = False
        is_green_blinking = False
    elif led == 'yellow' and blinking:
        if not is_yellow_blinking:
            is_yellow_blinking = True
            threading.Thread(target=blink_yellow_led, daemon=True).start()
    elif led == 'red' and not blinking:
        green_led.write(0)
        yellow_led.write(0)
        red_led.write(1)
        is_red_blinking = False
        is_yellow_blinking = False
        is_green_blinking = False
    elif led == 'red' and blinking:
        if not is_red_blinking:
            is_red_blinking = True
            threading.Thread(target=blink_red_led, daemon=True).start()
        is_green_blinking = False
        is_yellow_blinking = False
        is_yellow_blinking = False

def que_join(value):
    global people_in_que
    if value:
        people_in_que += 1
        if people_in_que > overload_mark:
            people_in_que = overload_mark
            print("Exit Sensor levert foutieve waardes: Wachtrij te vol")
        print(f"in de wachtrij: {people_in_que}")

def que_leave(value):
    global people_in_que
    if value:
        people_in_que -= 1
        if people_in_que < 0:
            people_in_que = 0
            print("Entrance Sensor levert foutieve waardes: Negatief bezoekersaantal")
        print(f"in de wachtrij: {people_in_que}")

class StatusApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wachtrij")
        self.root.geometry("800x600")

        self.mark_vars = {
            "Empty Mark": {"value": empty_mark, "entry": None},
            "Low Mark": {"value": low_mark, "entry": None},
            "High Mark": {"value": high_mark, "entry": None},
            "Full Mark": {"value": full_mark, "entry": None},
            "Overload Mark": {"value": overload_mark, "entry": None},
        }

        self.stateVar = tk.StringVar(value=f"{state}")
        self.queueVar = tk.IntVar(value=people_in_que)

        ttk.Label(root, text="Wachtrij Status:", font=("Helvetica", 14)).grid(row=0, column=0, padx=10, pady=5,
                                                                              sticky="w")
        self.var1_label = ttk.Label(root, textvariable=self.stateVar)
        self.var1_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(root, text="Aantal bezoekers in wachtrij", font=("Helvetica", 14)).grid(row=1, column=0, padx=10,
                                                                                          pady=5, sticky="w")
        self.var2_label = ttk.Label(root, textvariable=self.queueVar)
        self.var2_label.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(root, text="Watermerk Instellingen (attractie X)", font=("Helvetica", 16, "bold")).grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        for i, (label, data) in enumerate(self.mark_vars.items(), start=1):
            ttk.Label(root, text=label, font=("Helvetica", 14)).grid(row=i+2, column=0, padx=10, pady=5, sticky="w")
            entry = ttk.Entry(root)
            entry.insert(0, str(data["value"]))
            entry.grid(row=i+2, column=1, padx=10, pady=5, sticky="w")
            self.mark_vars[label]["entry"] = entry


        self.canvas = tk.Canvas(root, width=100, height=100)
        self.canvas.grid(row=len(self.mark_vars) + 3, column=0, padx=10, pady=5)

        self.circle = self.canvas.create_oval(25, 25, 75, 75, fill="gray")

        self.update_button = ttk.Button(root, text="Update alle Watermarks", command=self.update_marks)
        self.update_button.grid(row=len(self.mark_vars) + 4, column=0, columnspan=3, pady=20)

        self.update_ui()


    def update_marks(self):
        global overload_mark, full_mark, high_mark, low_mark, empty_mark

        try:
            overload_mark = int(self.mark_vars["Overload Mark"]["entry"].get())
            full_mark = int(self.mark_vars["Full Mark"]["entry"].get())
            high_mark = int(self.mark_vars["High Mark"]["entry"].get())
            low_mark = int(self.mark_vars["Low Mark"]["entry"].get())
            empty_mark = int(self.mark_vars["Empty Mark"]["entry"].get())

            vars['values']['watermarks']['overload_mark'] = overload_mark
            vars['values']['watermarks']['full_mark'] = full_mark
            vars['values']['watermarks']['high_mark'] = high_mark
            vars['values']['watermarks']['low_mark'] = low_mark
            vars['values']['watermarks']['empty_mark'] = empty_mark

            with open('values.json', 'w') as file:
                json.dump(vars, file, indent=4)

            self.update_ui()
            print(f"Nieuwe waarden: overload_mark={overload_mark}, full_mark={full_mark}, high_mark={high_mark}, low_mark={low_mark}, empty_mark={empty_mark}")
        except ValueError:
            print("Voer geldige gehele getallen in voor alle markeringen.")


    def update_circle(self, colour, blinking):
        if colour == 'green' and blinking:
            self.canvas.itemconfig(self.circle, fill="pale green")
        if colour == 'green' and not blinking:
            self.canvas.itemconfig(self.circle, fill=colour)
        if colour == 'yellow' and blinking:
            self.canvas.itemconfig(self.circle, fill="orange")
        if colour == 'yellow' and not blinking:
            self.canvas.itemconfig(self.circle, fill=colour)
        if colour == 'red' and blinking:
            self.canvas.itemconfig(self.circle, fill="red4")
        if colour == 'red' and not blinking:
            self.canvas.itemconfig(self.circle, fill=colour)

    def update_ui(self):
        self.stateVar.set(state)
        self.queueVar.set(people_in_que)

        if state == "leeg":
            StatusApp.update_circle(self, "green", True)
        elif state == "zo goed als leeg":
            StatusApp.update_circle(self, "green", False)
        elif state == "gevuld":
            StatusApp.update_circle(self, "yellow", False)
        elif state == "bijna vol":
            StatusApp.update_circle(self, "red", False)
        elif state == "vol":
            StatusApp.update_circle(self, "red", True)

        self.root.after(100, self.update_ui)

def setup():
    input6 = vars['values']['inputs']['entrance_sensor']
    input7 = vars['values']['inputs']['exit_sensor']

    detection_pin6 = board.get_pin(f'd:{input6}:i')
    print(f"Entrance sensor pin: {detection_pin6}")
    detection_pin6.register_callback(que_join)
    detection_pin6.enable_reporting()

    detection_pin7 = board.get_pin(f'd:{input7}:i')
    print(f"Exit sensor pin: {detection_pin7}")
    detection_pin7.register_callback(que_leave)
    detection_pin7.enable_reporting()

def main_loop():
    while True:
        global state

        state = check_amount_people(people_in_que)

        match state:
            case 'leeg':
                led_on('green', True)
            case 'zo goed als leeg':
                led_on('green', False)
            case 'gevuld':
                led_on('yellow', False)
            case 'bijna vol':
                led_on('red', False)
            case 'vol':
                led_on('red', True)
        
        time.sleep(0.1)

if __name__ == '__main__':
    setup()
    threading.Thread(target=main_loop, daemon=True).start()

    root = tk.Tk()
    app = StatusApp(root)
    root.mainloop()


    board.exit()