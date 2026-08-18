import random

# Ein simples "GUI" ohne Libraries:
# - nutzt nur Textausgabe + Eingabe
# - verwaltet trotzdem Eingabefelder/Buttons-ähnlich durch Menüs

def gui_start():
    niedrig, hoch = 1, 100
    ziel = random.randint(niedrig, hoch)
    versuche = 0

    print("====================================")
    print("       ZAHLRATEN (GUI-Style)       ")
    print("====================================")
    print(f"Bereich: {niedrig} bis {hoch}")
    print("Bedienung:")
    print("  Tipp eingeben = raten")
    print("  N = Neustart")
    print("  Q = Beenden")
    print("------------------------------------")

    while True:
        print(f"\nVersuche: {versuche}")
        eingabe = input("Tipp (oder N/Q): ").strip().upper()

        if eingabe == "Q":
            print("Spiel beendet.")
            return

        if eingabe == "N":
            niedrig, hoch = 1, 100
            ziel = random.randint(niedrig, hoch)
            versuche = 0
            print("Neues Spiel gestartet!")
            continue

        if not eingabe.isdigit():
            print("❌ Bitte eine ganze Zahl eingeben.")
            continue

        tipp = int(eingabe)
        if tipp < niedrig or tipp > hoch:
            print(f"❌ Zahl außerhalb des Bereichs ({niedrig}–{hoch}).")
            continue

        versuche += 1

        if tipp < ziel:
            print("Zu klein!")
        elif tipp > ziel:
            print("Zu groß!")
        else:
            print(f"✅ Richtig! Die Zahl war {ziel}.")
            print(f"Gesamtversuche: {versuche}")
            # nach Erfolg automatisch Neustart anbieten
            weiter = input("Nochmal spielen? (J/N): ").strip().upper()
            if weiter == "J":
                ziel = random.randint(niedrig, hoch)
                versuche = 0
                print("Neues Spiel gestartet!")
            else:
                print("Spiel beendet.")
                return

if __name__ == "__main__":
    gui_start()
