from logic import SaveEntry, CreateEntry

def main():
    mein_neuer_eintrag = CreateEntry()
    
    # 2. Speichere das Ergebnis sauber ab
    SaveEntry(mein_neuer_eintrag)
    print("\n[SUCCESS] Passwort erfolgreich in 'passwords.json' gespeichert!")

if __name__ == "__main__":
    main()