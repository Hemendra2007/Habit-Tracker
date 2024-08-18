import json
from datetime import datetime

class HabitTracker:
    def __init__(self, filename='habits.json'):
        self.filename = filename
        self.habits = self.load_data()

    def load_data(self):
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_data(self):
        with open(self.filename, 'w') as file:
            json.dump(self.habits, file, indent=4)

    def add_habit(self, habit_name):
        if habit_name.strip() == '':
            print("Habit name cannot be empty.")
            return
        if habit_name not in self.habits:
            self.habits[habit_name] = {}
            print(f"Habit '{habit_name}' added.")
        else:
            print(f"Habit '{habit_name}' already exists.")
        self.save_data()

    def mark_habit(self, habit_name):
        today = datetime.now().strftime('%Y-%m-%d')
        if habit_name in self.habits:
            if today in self.habits[habit_name]:
                print(f"Habit '{habit_name}' already marked for today.")
            else:
                self.habits[habit_name][today] = True
                print(f"Habit '{habit_name}' marked for today.")
            self.save_data()
        else:
            print(f"Habit '{habit_name}' not found.")

    def display_habits(self):
        if not self.habits:
            print("No habits to display.")
            return
        for habit, dates in sorted(self.habits.items()):
            print(f"\nHabit: {habit}")
            if dates:
                for date in sorted(dates):
                    print(f"  - {date}")
            else:
                print("  No records yet.")

    def delete_habit(self, habit_name):
        if habit_name in self.habits:
            del self.habits[habit_name]
            print(f"Habit '{habit_name}' deleted.")
            self.save_data()
        else:
            print(f"Habit '{habit_name}' not found.")

    def edit_habit(self, old_name, new_name):
        if old_name in self.habits:
            if new_name.strip() == '':
                print("New habit name cannot be empty.")
                return
            if new_name in self.habits:
                print(f"Habit '{new_name}' already exists.")
                return
            self.habits[new_name] = self.habits.pop(old_name)
            print(f"Habit '{old_name}' renamed to '{new_name}'.")
            self.save_data()
        else:
            print(f"Habit '{old_name}' not found.")

def main():
    tracker = HabitTracker()
    while True:
        print("\nHabit Tracker")
        print("1. Add Habit")
        print("2. Mark Habit")
        print("3. Display Habits")
        print("4. Delete Habit")
        print("5. Edit Habit")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            habit_name = input("Enter habit name: ")
            tracker.add_habit(habit_name)
        elif choice == '2':
            habit_name = input("Enter habit name to mark: ")
            tracker.mark_habit(habit_name)
        elif choice == '3':
            tracker.display_habits()
        elif choice == '4':
            habit_name = input("Enter habit name to delete: ")
            tracker.delete_habit(habit_name)
        elif choice == '5':
            old_name = input("Enter old habit name: ")
            new_name = input("Enter new habit name: ")
            tracker.edit_habit(old_name, new_name)
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
