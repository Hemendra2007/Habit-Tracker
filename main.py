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

    def add_habit(self, habit_name, category):
        if habit_name.strip() == '':
            print("Habit name cannot be empty.")
            return
        if habit_name not in self.habits:
            self.habits[habit_name] = {
                'dates': [], 'streak': 0, 'category': category, 'start_date': datetime.now().strftime('%Y-%m-%d')
            }
            print(f"Habit '{habit_name}' added under category '{category}'.")
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

    def calculate_completion_percentage(self, habit_name):
        if habit_name in self.habits:
            start_date = datetime.strptime(self.habits[habit_name]['start_date'], '%Y-%m-%d')
            today = datetime.now()
            total_days = (today - start_date).days + 1
            completed_days = len(self.habits[habit_name]['dates'])
            completion_percentage = (completed_days / total_days) * 100
            print(f"Completion percentage for '{habit_name}': {completion_percentage:.2f}%")
        else:
            print(f"Habit '{habit_name}' not found.")

    def reset_habit(self, habit_name):
        if habit_name in self.habits:
            self.habits[habit_name]['dates'] = []
            self.habits[habit_name]['streak'] = 0
            print(f"Habit '{habit_name}' has been reset.")
            self.save_data()
        else:
            print(f"Habit '{habit_name}' not found.")

    def display_habit_summary(self):
        total_habits = len(self.habits)
        total_categories = len(set(h['category'] for h in self.habits.values()))
        print(f"\nTotal Habits: {total_habits}")
        print(f"Total Categories: {total_categories}")
        self.display_longest_streak()

    def display_habits(self):
        if not self.habits:
            print("No habits to display.")
            return
        for habit, details in sorted(self.habits.items()):
            print(f"\nHabit: {habit}")
            print(f"  Category: {details['category']}")
            print(f"  Streak: {details['streak']} days")
            if details['dates']:
                for date in sorted(details['dates']):
                    print(f"  - {date}")
            else:
                print("  No records yet.")

    def display_habits_by_category(self, category):
        print(f"\nHabits under category '{category}':")
        found = False
        for habit, details in self.habits.items():
            if details['category'].lower() == category.lower():
                print(f"  - {habit} (Streak: {details['streak']} days)")
                found = True
        if not found:
            print(f"No habits found in category '{category}'.")

    def display_habits_by_date_range(self, start_date, end_date):
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        print(f"\nHabits between {start_date.strftime('%Y-%m-%d')} and {end_date.strftime('%Y-%m-%d')}:")
        for habit, details in self.habits.items():
            print(f"\nHabit: {habit}")
            for date in details['dates']:
                date_obj = datetime.strptime(date, '%Y-%m-%d')
                if start_date <= date_obj <= end_date:
                    print(f"  - {date}")

    def display_longest_streak(self):
        if not self.habits:
            print("No habits to display.")
            return
        longest_streak = 0
        longest_habit = None
        for habit, details in self.habits.items():
            if details['streak'] > longest_streak:
                longest_streak = details['streak']
                longest_habit = habit
        if longest_habit:
            print(f"The habit with the longest streak is '{longest_habit}' with {longest_streak} days.")
        else:
            print("No streaks found.")

    def backup_data(self, backup_filename):
        with open(backup_filename, 'w') as file:
            json.dump(self.habits, file, indent=4)
        print(f"Data backed up to '{backup_filename}'.")

    def restore_data(self, backup_filename):
        try:
            with open(backup_filename, 'r') as file:
                self.habits = json.load(file)
            self.save_data()
            print(f"Data restored from '{backup_filename}'.")
        except FileNotFoundError:
            print(f"Backup file '{backup_filename}' not found.")

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
        print("6. Reset Habit")
        print("7. View Habit Progress")
        print("8. Display Habits by Category")
        print("9. Display Longest Streak")
        print("10. Backup Data")
        print("11. Restore Data")
        print("12. Display Habits by Date Range")
        print("13. Display Habit Summary")
        print("14. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            habit_name = input("Enter habit name: ")
            category = input("Enter habit category: ")
            tracker.add_habit(habit_name, category)
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
            tracker.calculate_completion_percentage(habit_name)
        elif choice == '8':
            category = input("Enter category to display habits: ")
            tracker.display_habits_by_category(category)
        elif choice == '9':
            tracker.display_longest_streak()
        elif choice == '10':
            backup_filename = input("Enter backup filename: ")
            tracker.backup_data(backup_filename)
        elif choice == '11':
            backup_filename = input("Enter backup filename to restore: ")
            tracker.restore_data(backup_filename)
        elif choice == '12':
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            tracker.display_habits_by_date_range(start_date, end_date)
        elif choice == '13':
            tracker.display_habit_summary()
        elif choice == '14':
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
