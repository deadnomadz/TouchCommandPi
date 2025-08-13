#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import tkinter as Tk
from tkinter import messagebox
from tkinter import PhotoImage, Frame, Button, Label, TclError, Scrollbar, Text, Toplevel
from math import sqrt, floor, ceil
import yaml


class FlatButton(Button):
    def __init__(self, master=None, cnf=None, **kw):
        Button.__init__(self, master, cnf, **kw)

        self.config(
            compound=Tk.TOP,
            relief=Tk.FLAT,
            bd=0,
            bg="#b91d47",  # dark-red
            fg="white",
            activebackground="#b91d47",  # dark-red
            activeforeground="white",
            highlightthickness=0
        )

    def set_color(self, color):
        self.configure(
            bg=color,
            fg="white",
            activebackground=color,
            activeforeground="white"
        )


class PiMenu(Frame):
    framestack = []
    icons = {}
    path = ''
    lastinit = 0

    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")
        self.parent = parent
        self.pack(fill=Tk.BOTH, expand=1)

        self.path = os.path.dirname(os.path.realpath(sys.argv[0]))
        self.initialize()

    def initialize(self):
        try:
            with open(os.path.join(self.path, 'pimenu.yaml'), 'r') as f:
                doc = yaml.safe_load(f)
            self.lastinit = os.path.getmtime(os.path.join(self.path, 'pimenu.yaml'))
        except FileNotFoundError:
            messagebox.showerror("Error", "Configuration file (pimenu.yaml) not found!")
            sys.exit(1)
        except yaml.YAMLError as e:
            messagebox.showerror("Error", f"Error reading the YAML configuration: {e}")
            sys.exit(1)

        if len(self.framestack):
            self.destroy_all()
            self.destroy_top()

        self.show_items(doc)

    def has_config_changed(self):
        return self.lastinit != os.path.getmtime(os.path.join(self.path, 'pimenu.yaml'))

    def show_items(self, items, upper=None):
        if upper is None:
            upper = []
        num = 0

        wrap = Frame(self, bg="black")

        if len(self.framestack):
            self.hide_top()
            back = FlatButton(
                wrap,
                text='Back…',
                image=self.get_icon("arrow.left"),
                command=self.go_back,
            )
            back.set_color("#00a300")  # green
            back.grid(row=0, column=0, padx=1, pady=1, sticky=Tk.W + Tk.E + Tk.N + Tk.S)
            num += 1

        self.framestack.append(wrap)
        self.show_top()

        allitems = len(items) + num
        rows = floor(sqrt(allitems))
        cols = ceil(allitems / rows)

        for x in range(int(cols)):
            wrap.columnconfigure(x, weight=1)
        for y in range(int(rows)):
            wrap.rowconfigure(y, weight=1)

        for item in items:
            act = upper + [item['name']]

            if 'icon' in item:
                image = self.get_icon(item['icon'])
            else:
                image = self.get_icon(f'scrabble.{item["label"][0:1].lower()}')

            btn = FlatButton(
                wrap,
                text=item['label'],
                image=image
            )

            if 'items' in item:
                btn.configure(command=lambda act=act, item=item: self.show_items(item['items'], act),
                              text=item['label'] + '…')
                btn.set_color("#2b5797")  # dark-blue
            else:
                if 'command' in item:
                    btn.configure(command=lambda cmd=item['command']: self.go_action(command=cmd))
                else:
                    btn.configure(command=lambda act=act: self.go_action(actions=act))

            if 'color' in item:
                btn.set_color(item['color'])

            btn.grid(
                row=int(floor(num / cols)),
                column=int(num % cols),
                padx=1,
                pady=1,
                sticky=Tk.W + Tk.E + Tk.N + Tk.S
            )
            num += 1

    def get_icon(self, name):
        if name in self.icons:
            return self.icons[name]

        ico = os.path.join(self.path, 'ico', f'{name}.png')
        if not os.path.isfile(ico):
            ico = os.path.join(self.path, 'ico', f'{name}.gif')
            if not os.path.isfile(ico):
                ico = os.path.join(self.path, 'ico', 'cancel.gif')

        try:
            self.icons[name] = PhotoImage(file=ico)
        except TclError:
            self.icons[name] = PhotoImage(file=os.path.join(self.path, 'ico', 'cancel.gif'))

        return self.icons[name]

    def hide_top(self):
        self.framestack[len(self.framestack) - 1].pack_forget()

    def show_top(self):
        self.framestack[len(self.framestack) - 1].pack(fill=Tk.BOTH, expand=1)
        self.parent.after(500, lambda: self.parent.update())

    def destroy_top(self):
        self.framestack[len(self.framestack) - 1].destroy()
        self.framestack.pop()

    def destroy_all(self):
        while len(self.framestack) > 1:
            self.destroy_top()

    def go_action(self, actions=None, command=None):
        self.hide_top()
        delay = Frame(self, bg="#2d89ef")
        delay.pack(fill=Tk.BOTH, expand=1)
        label = Label(delay, text="Executing...", fg="white", bg="#2d89ef", font="Sans 30")
        label.pack(fill=Tk.BOTH, expand=1)
        self.parent.update()

        output = ""
        try:
            if command:
                result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=300, text=True)
                output = result.stdout
            else:
                result = subprocess.run([os.path.join(self.path, 'pimenu.sh')] + actions, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=30, text=True)
                output = result.stdout
        except subprocess.TimeoutExpired:
            output = "Error: Command timed out."
        except subprocess.CalledProcessError as e:
            output = f"Error executing command: {e}"

        delay.destroy()
        self.show_output_popup(output, command_text=command if command else ' '.join(actions))
        self.destroy_all()
        self.show_top()

    def show_output_popup(self, output, command_text=None):
        popup = Toplevel(self)
        popup.title("Command Output")
        popup.geometry("400x300")
        popup.configure(bg="white")

        frame = Frame(popup, bg="white")
        frame.pack(fill=Tk.BOTH, expand=1)

        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=Tk.RIGHT, fill=Tk.Y)

        text = Text(frame, wrap=Tk.WORD, yscrollcommand=scrollbar.set, bg="white", fg="black")
        text.insert(Tk.END, output)
        text.config(state=Tk.DISABLED)
        text.pack(fill=Tk.BOTH, expand=1)

        scrollbar.config(command=text.yview)

        button_frame = Frame(popup, bg="white")
        button_frame.pack(fill=Tk.X, pady=5)

        def save_output():
            from datetime import datetime
            import re

            home = os.path.expanduser("~")
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

            if command_text:
                name = re.sub(r'[^\w.-]', '_', command_text.strip().split()[0])
            else:
                name = "pimenu_output"

            filename = f"{name}_{timestamp}.txt"
            filepath = os.path.join(home, filename)

            try:
                with open(filepath, "w") as f:
                    f.write(output)
                messagebox.showinfo("Saved", f"Output saved to:\n{filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{e}")

        save_btn = Button(button_frame, text="Save Output", command=save_output, bg="#0078d7", fg="white")
        save_btn.pack(side=Tk.LEFT, padx=10, expand=True, fill=Tk.X)

        close_btn = Button(button_frame, text="Close", command=popup.destroy, bg="#0078d7", fg="white")
        close_btn.pack(side=Tk.RIGHT, padx=10, expand=True, fill=Tk.X)

    def go_back(self):
        if self.has_config_changed():
            self.initialize()
        else:
            self.destroy_top
def main():
    root = Tk.Tk()
    root.geometry("320x240")
    root.wm_title('PiMenu')
    if len(sys.argv) > 1 and sys.argv[1] == 'fs':
        root.wm_attributes('-fullscreen', True)
    PiMenu(root)
    root.mainloop()


if __name__ == '__main__':
    main()