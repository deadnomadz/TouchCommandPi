# TouchCommandPi

A simple, customizable menu for the Raspberry Pi (or any Linux system) using Tkinter and YAML. 

GREAT FOR TOUCH SCREENS!

---

## Features

- **Python 3 compatible**
- **Easy menu configuration via YAML**
- **Direct command execution:**  
  Define any shell command for a menu item—no need for wrapper scripts.
- **Customizable icons, colors, and labels**
- **Hierarchical (multi-level) menus**
- **Simple, touch-friendly interface**

---

## Installation

1. **Clone this repository:**
   ```sh
   git clone https://github.com/deadnomadz/TouchCommandPi.git
   cd TouchCommandPi
   ```

2. **Install dependencies:**
   ```sh
   pip install pyyaml
   sudo apt install python3-tk
   ```

3. **Run the menu:**
   ```sh
   python TouchCommandPi.py
   ```

   To start in fullscreen mode:
   ```sh
   python TouchCommandPi.py fs
   ```
   UNZIP ICO.ZIP FIRST!
---

## Configuration

All menu items are defined in `pimenu.yaml` (in the same directory as `TouchCommandPi.py`).

### Example `pimenu.yaml`

```yaml
- label: Shutdown
  icon: shutdown
  color: "#b91d47"
  command: "shutdown now"

- label: Reboot
  icon: reboot
  color: "#e3a21a"
  command: "reboot"

- label: Utilities
  icon: tools
  color: "#2b5797"
  items:
    - label: List Files
      icon: folder
      color: "#00a300"
      command: "ls -l /home/pi"
    - label: Show Date
      icon: clock
      color: "#e3a21a"
      command: "date"
```

### Menu Item Fields

- **label**: Text shown on the button.
- **icon**: Name of the icon file (PNG or GIF, placed in the `ico/` folder).
- **color**: Button color (hex code).
- **command**: (Optional) Shell command to execute when pressed.
- **items**: (Optional) List of submenu items.

If a menu item has a `command`, it will be executed directly in the shell.  
If it has `items`, it will open a submenu.

---

## Icons

- Place your PNG or GIF icons in the `ico/` directory.
- The icon name in YAML should match the filename (without extension).

---

## Notes & Crucial Info

- **Commands are executed as the user running the menu.**  
  Be careful with commands that require elevated privileges.
- **Output of commands** is shown in a popup window after execution.
- **Menu auto-reloads** if you edit and save `pimenu.yaml` (restart required for some changes).
- **Touchscreen friendly:** Large buttons and simple navigation.

---

## License

This project is based on [splitbrain/pimenu](https://github.com/splitbrain/pimenu)

---

## Credits

- Support: [E](https://github.com/deadnomadz)
