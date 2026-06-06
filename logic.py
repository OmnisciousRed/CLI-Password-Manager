import string
import secrets
import json
import os

def GetUserPasswordSettings():
    
    lengthInput = input("\n[Recommended: at least 16 characters] Password Length: ")
    length: int = int(lengthInput)

    lowerLetterInput = input("Lower Letter (y/n): ")
    lowerLetter: bool = lowerLetterInput.lower() == "y"

    upperLetterInput = input("upper Letter (y/n): ")
    upperLetter: bool = upperLetterInput.lower() == "y"

    numberInput = input("Number (y/n): ")
    number: bool = numberInput.lower() == "y"

    symbolInput = input("Symbol (y/n): ")
    symbol: bool = symbolInput.lower() == "y"

    return length, lowerLetter, upperLetter, number, symbol

def CreatePasswordCharacterPool(useLower: bool, useUpper: bool, useNumber: bool, useSymbol: bool):
    
    pool = ""

    if useLower:
        pool = pool + string.ascii_lowercase

    if useUpper:
        pool = pool + string.ascii_uppercase

    if useNumber:
        pool = pool + string.digits

    if useSymbol:
        pool = pool + string.punctuation
    
    return pool

def GeneratePassword():

    print("\n----------------------------")
    print("---- GENERATE PASSWORD -----")
    print("----------------------------")

    settingApproved = False

    length = 16
    lower = upper = number = symbol = True

    while not settingApproved:
        
        length, lower, upper, number, symbol = GetUserPasswordSettings()

        print("\n---------------------------")
        print("---- Choosen Settings -----")
        print("---------------------------")
        print(f"\nLength: {length}")
        print(f"Lowercase: {'Yes' if lower else 'No'}")
        print(f"Uppercase: {'Yes' if upper else 'No'}")
        print(f"Numbers: {'Yes' if number else 'No'}")
        print(f"Symbols: {'Yes' if symbol else 'No'}")
        print("----------------------------")

        confirmSettingsInput = input("\nAre you happy with these settings? (y/n): ")

        settingApproved = confirmSettingsInput.lower() == "y"

    charPool = CreatePasswordCharacterPool(lower, upper, number, symbol)
    
    passwordApproved = False

    while not passwordApproved:
        password = ""
        for i in range(length):
            randomChar = secrets.choice(charPool)
            password = password + randomChar

        confirmPasswordInput = input(f"\nAre you happy with the password {password} ? (y/n): ")
        passwordApproved = confirmPasswordInput.lower() == "y"

    
    return password

def SaveEntry(newEntry):

    currentList = LoadEntries()

    currentList.append(newEntry)

    jsonText = json.dumps(currentList)

    with open("passwords.json", "w") as file:
        file.write(jsonText)

def SaveAllEntries(entries_list):
    """Überschreibt die JSON-Datei mit der modifizierten Liste"""
    jsonText = json.dumps(entries_list, indent=4)
    with open("passwords.json", "w") as file:
        file.write(jsonText)

def LoadEntries():

    if not os.path.exists("passwords.json"):
        return []
    
    with open("passwords.json", "r") as file:
        content = file.read()

        list = json.loads(content)
        return list

def CreateEntry():

    password = GeneratePassword()
    title = input("\nEnter Title for this password (e.g. Netflix): ")
    description = input("Enter Description: ")

    entry = {
        "title": title,
        "description": description,
        "password": password
    }

    return entry

def ShowExistingEntry():

    entries = LoadEntries()

    for index, entry in enumerate(entries, start=1):
        print(f"\n------ ENTRY [{index}] -----------")
        print(f"Title: {entry['title']}")
        print(f"Description: {entry['description']}")
        print(f"Password {entry['password']}")
        print("-------------------------")

    return True

def EditExistingEntry():

    if not ShowExistingEntry():
        return
    
    entries = LoadEntries()

    try:
        toEditEntry = input("\nwhich entry (Enter a number): ").strip()
        choiceIndex = int(toEditEntry) - 1

        if choiceIndex < 0 or choiceIndex >= len(entries):
            print("\n[!] invalid Number")
            return
    
    except ValueError:
        print("\n[!] Please enter a valid number")
        return
    
    editOrDelete = input("wanna edit [1] or delete [2]: ")
    match editOrDelete:
        case "1":
            selectedEntry = entries[choiceIndex]
            print(f"\nyou are currently editing: {selectedEntry['title']}")
            print("\nLeave the fields blank (press Enter) if you don't want to change them")

            newTitle = input(f"New Title: ").strip()
            if newTitle:
                selectedEntry['title'] = newTitle

            newDescription = input(f"New Description: ").strip()
            if newDescription:
                selectedEntry['description'] = newDescription

            newPassword = input(f"New Password (y/n): ").strip().lower()
            if newPassword == "y":
                password = GeneratePassword()
                selectedEntry['password'] = password

            SaveAllEntries(entries)
        
        case "2":
            deleteEntry = entries.pop(choiceIndex)
            SaveAllEntries(entries)
        case _:
            print("\n [!] Invalid selection. Please choose [1] for editing | [2] for deleting an Entry")

    print("\n[SUCCESS] Entry succesfully updated")

def HandleMenu():

    while True:
        print("\n1. Create Password")
        print("2. Read the existing Passwords")
        print("3. Edit an existing Passwords")
        print("4. End Program")

        inputChoose = input(f"Choose (1-4): ").strip()

        match inputChoose:
            case "1":
                newEntry = CreateEntry()
                SaveEntry(newEntry)
                print("\n[SUCCESS] Password successfully saved in 'passwords.json'")
            case "2":
                ShowExistingEntry()
                print("\n[SUCCESS] Passwords were successfully retrieved")
            case "3":
                EditExistingEntry()
            case "4":
                print("\n[SUCCESS] PROGRAM EXIT")
                break
            case _:
                print("\n [!] Invalid selection. Please choose one of the numbers listed")

      
