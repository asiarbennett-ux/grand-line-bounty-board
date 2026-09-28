import json
import os

FILENAME = "bounty_data.json"

def load_bounty_data():
    """Loads bounty targets from the JSON file with error handling."""
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, "r", encoding="utf-8") as file:
        return json.load(file)

def save_bounty_data(targets):
    """Saves updated target list back to the JSON file."""
    with open(FILENAME, "w", encoding="utf-8") as file:
        json.dump(targets, file, indent=4)

def display_bounty_board(targets=None):
    """Parses target data and formats it into a terminal-styled Wanted Board."""
    if targets is None:
        targets = load_bounty_data()
        
    if not targets:
        print("\n[-] No bounty targets found in the database.")
        return
    
    print("\n" + "=" * 60)
    print("🏴‍☠️  WORLD GOVERNMENT / HUNTER ASSOCIATION WANTED BOARD  🏴‍☠️")
    print("=" * 60)
    
    for idx, target in enumerate(targets, start=1):
        print(f"\n[TARGET #{idx} - DEAD OR ALIVE]")
        print(f"  • Name:   {target['name']} (\"{target['epitaph']}\")")
        print(f"  • Bounty: {target['bounty']}")
        print(f"  • Power:  {target['devil_fruit']}")
        print(f"  • Status: {target['status']}")
        print("-" * 60)

def search_target():
    """Searches for targets by name or epitaph keyword."""
    query = input("\nEnter character name or keyword to search: ").strip().lower()
    targets = load_bounty_data()
    
    matches = [
        t for t in targets 
        if query in t['name'].lower() or query in t['epitaph'].lower()
    ]
    
    if matches:
        print(f"\n[+] Found {len(matches)} match(es) for '{query}':")
        display_bounty_board(matches)
    else:
        print(f"\n[-] No targets matched '{query}'.")

def add_target():
    """Prompts user for new target details and saves them to JSON."""
    print("\n--- ADD NEW WANTED TARGET ---")
    name = input("Enter character name: ").strip()
    epitaph = input("Enter epitaph/title (e.g. Pirate Hunter): ").strip()
    bounty = input("Enter bounty amount (e.g. 500,000,000 Beli): ").strip()
    devil_fruit = input("Enter power / Devil Fruit: ").strip()
    status = input("Enter status (e.g. Active Threat, Elusive): ").strip()

    if not name or not bounty:
        print("\n[-] Error: Name and Bounty cannot be empty.")
        return

    new_target = {
        "name": name,
        "epitaph": epitaph,
        "bounty": bounty,
        "devil_fruit": devil_fruit,
        "status": status
    }

    targets = load_bounty_data()
    targets.append(new_target)
    save_bounty_data(targets)
    print(f"\n[+] Success! {name} has been added to the database and saved to JSON.")

def main_menu():
    """Runs the main interactive terminal controller."""
    while True:
        print("\n=== 🏴‍☠️ GRAND LINE BOUNTY MANAGEMENT SYSTEM 🏴‍☠️ ===")
        print("1. View All Wanted Targets")
        print("2. Search Target by Name")
        print("3. Add New Wanted Target")
        print("4. Exit")
        
        choice = input("\nSelect an option (1-4): ").strip()
        
        if choice == "1":
            display_bounty_board()
        elif choice == "2":
            search_target()
        elif choice == "3":
            add_target()
        elif choice == "4":
            print("\nSetting sail... Goodbye, Hunter!")
            break
        else:
            print("\n[-] Invalid choice. Please choose a number between 1 and 4.")

if __name__ == "__main__":
    main_menu()