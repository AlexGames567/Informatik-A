import random
def zahlenraten():    
    zufall = random.randint(1, 100)    
    versuche = 0
    print("Zahlenraten: Ich denke mir eine Zahl von 1 bis 100.")    
    print("Tippe eine Zahl ein. Mit Eingabe 'q' beendest du.")
    while True:        
        eingabe = input("Dein Tipp: ").strip().lower()        
        if eingabe == "q":            
            print("Spiel beendet.")            
            break
        if not eingabe.isdigit():            
            print("Bitte eine ganze Zahl eingeben.")            
            continue
        tipp = int(eingabe)        
        versuche += 1
        if tipp < zufall:            
            print("Zu klein!")        
        elif tipp > zufall:            
            print("Zu groß!")       
        else:            
            print(f"Richtig! Die Zahl war {zufall}. Versuche: {versuche}")            
            break
if __name__ == "__main__":    
    zahlenraten()