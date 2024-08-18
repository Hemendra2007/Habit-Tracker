import json
from datetime import datetime, timedelta

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
            self.habits[habit_name] = {'dates': [], 'streak': 0}
            print(f"Habit '{habit_name}' added.")
        else:
            print(f"Habit '{habit_name}' already exists.")
        self.save_data()

    def mark_habit(self, habit_name):
        today = datetime.now().strftime('%Y-%m-%d')
        if habit_name in self.habits:
            if today in self.habits[habit_name]['dates']:
                print(f"Habit '{habit_name}' already marked for today.")
            else:
                self.habits[habit_name]['dates'].append(today)
                self.update_streak(habit_name)
                print(f"Habit '{habit_name}' marked for today.")
            self.save_data()
        else:
            print(f"Habit '{habit_name}' not found.")

    def update_streak(self, habit_name):
        dates = self.habits[habit_name]['dates']
        if len(dates) < 2:
            self.habits[habit_name]['streak'] = len(dates)
        else:
            streak = 1
            for i in range(len(dates) - 1, 0, -1):
                current_date = datetime.strptime(dates[i], '%Y-%m-%d')
                prev_date = datetime.strptime(dates[i - 1], '%Y-%m-%d')
                if (current_date - prev_date).days == 1:
                    streak += 1
                else:
                    break
            self.habits[habit_name]['streak'] = streak

    def display_habits(self):
        if not self.habits:
            print("No habits to display.")
            return
        for habit, details in sorted(self.habits.items()):
            print(f"\nHabit: {habit}")
            print(f"  Streak: {details['streak']} days")
            if details['dates']:
                for date in sorted(details['dates']):
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

    def reset_habit(self, habit_name):
        if habit_name in self.habits:
            self.habits[habit_name]['dates'] = []
            self.habits[habit_name]['streak'] = 0
            print(f"Habit '{habit_name}' reset.")
            self.save_data()
        else:
            print(f"Habit '{habit_name}' not found.")

    def view_habit_progress(self, habit_name):
        if habit_name in self.habits:
            print(f"\nProgress for '{habit_name}':")
            if self.habits[habit_name]['dates']:
                for date in sorted(self.habits[habit_name]['dates']):
                    print(f"  - {date}")
                print(f"Current streak: {self.habits[habit_name]['streak']} days")
            else:
                print("  No records yet.")
        else:
            print(f"Habit '{habit_name}' not found.")

def main():
    tracker = HabitTracker()
    while True:
        print("\nHabit Tracker")
        print("1. Add Habit")
        print("2. Mark Habit")
        print("3. Display Habits")
        print("4. Delete Habit")
        print("5. Edit Habit")
        print("6. Reset Habit")
        print("7. View Habit Progress")
        print("8. Exit")
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
            habit_name = input("Enter habit name to reset: ")
            tracker.reset_habit(habit_name)
        elif choice == '7':
            habit_name = input("Enter habit name to view progress: ")
            tracker.view_habit_progress(habit_name)
        elif choice == '8':
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
