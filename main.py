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
        if habit_name not in self.habits:
            self.habits[habit_name] = {}
        self.save_data()

    def mark_habit(self, habit_name):
        today = datetime.now().strftime('%Y-%m-%d')
        if habit_name in self.habits:
            self.habits[habit_name][today] = True
            self.save_data()
        else:
            print(f"Habit '{habit_name}' not found.")

    def display_habits(self):
        for habit, dates in self.habits.items():
            print(f"Habit: {habit}")
            for date in dates:
                print(f"  - {date}")
def main():
    tracker = HabitTracker()
    while True:
        print("\nHabit Tracker")
        print("1. Add Habit")
        print("2. Mark Habit")
        print("3. Display Habits")
        print("4. Exit")
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
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
