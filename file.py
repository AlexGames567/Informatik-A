import tkinter as tk
import random

class ZahlenratenGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Zahlenraten")

        self.angezeigt_versuche = 0
        self.nummer = random.randint(1, 100)

        # Anzeige
        self.label_info = tk.Label(root, text="Ich denke mir eine Zahl von 1 bis 100.")
        self.label_info.pack(padx=10, pady=(10, 5))

        self.label_status = tk.Label(root, text="Gib deinen Tipp ein und klicke auf 'Raten'.")
        self.label_status.pack(padx=10, pady=5)

        self.label_versuche = tk.Label(root, text="Versuche: 0")
        self.label_versuche.pack(padx=10, pady=(5, 10))

        # Eingabe
        self.entry = tk.Entry(root)
        self.entry.pack(padx=10, pady=5)
        self.entry.bind("<Return>", lambda event: self.raten())

        # Buttons
        self.btn_raten = tk.Button(root, text="Raten", command=self.raten)
        self.btn_raten.pack(padx=10, pady=5)

        self.btn_neustart = tk.Button(root, text="Neustart", command=self.neustart)
        self.btn_neustart.pack(padx=10, pady=(0, 10))

    def neustart(self):
        self.nummer = random.randint(1, 100)
        self.angezeigt_versuche = 0
        self.label_versuche.config(text="Versuche: 0")
        self.label_status.config(text="Neues Spiel. Gib deinen Tipp ein.")
        self.entry.delete(0, tk.END)
        self.entry.focus_set()

    def raten(self):
        eingabe = self.entry.get().strip()

        if eingabe.lower() in ("q", "quit", "exit"):
            self.root.destroy()
            return

        if not eingabe.isdigit():
            self.label_status.config(text="Bitte eine ganze Zahl eingeben.")
            return

        tipp = int(eingabe)
        self.angezeigt_versuche += 1
        self.label_versuche.config(text=f"Versuche: {self.angezeigt_versuche}")

        if tipp < self.nummer:
            self.label_status.config(text="Zu klein!")
        elif tipp > self.nummer:
            self.label_status.config(text="Zu groß!")
        else:
            self.label_status.config(text=f"Richtig! Die Zahl war {self.nummer}.")
            self.entry.config(state="disabled")
            self.btn_raten.config(state="disabled")

            # optional: Button wieder aktivieren über "Neustart"
            # (Neustart-Button bleibt aktiv)

if __name__ == "__main__":
    root = tk.Tk()
    app = ZahlenratenGUI(root)
    root.mainloop()
