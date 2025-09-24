from typing import Final
import random
import json
import tkinter as tk

SPECIAL_STUDENT_NAME: Final[str] = "Šimon"
GUI_BACKGROUND: Final[str] = "grey"
BUTTON_BACKGROUND: Final[str] = "white"
ENTRY_BACKGROUND: Final[str] = "white"

grade: int = 0
name: str = ""

user_data: dict

created_gui_elements: list = []
create_user_allowed: bool = False
main_grade_button: tk.Button

def load_data() -> None:
    global user_data

    try:
        with open("znamky.json", "r") as file:
            user_data = json.load(file)
    except:
        user_data = {
            "students": []
        }

def save_data() -> None:
    global user_data

    with open("znamky.json", "w") as file:
        json.dump(user_data, file, indent=4)

def grade_student() -> None:
    global grade, name, user_data

    student_exists: bool = False

    for student in user_data["students"]:
        student_name: str = student["name"]

        if student_name != name:
            continue

        student_exists = True

        if len(student["grades"]) > 255:
            print(f"Student nemůže mít více známek než {255}")
        else:
            student["grades"].append(grade)

    if not student_exists:
        if create_user_allowed:
            new_student: dict = {
                "name": name,
                "grades": [grade]
            }

            user_data["students"].append(new_student)
        else:
            print(f"Student {name} neexistuje")

def get_student_grades(selected_student_name: str) -> list[int]:
    global user_data

    grades: list[int] = []

    for student in user_data["students"]:
        student_name: str = student["name"]

        if student_name != selected_student_name:
            continue

        grades = student["grades"]

    return grades

def round_average_grade(grade: float) -> float:
    rounded_grade: float = grade

    rounded_grade = round(rounded_grade, 2)

    return rounded_grade

def get_average_grade(grades: list[int]) -> None:
    average_grade: float = 0

    for grade in grades:
        average_grade += grade

    average_grade /= len(grades)

    average_grade = round_average_grade(average_grade)

    return average_grade

def remove_created_gui() -> None:
    for gui_element in created_gui_elements:
        gui_element.destroy()

def special_student_gui(gui_root: tk.Tk, student_name: tk.Entry) -> None:
    global created_gui_elements

    manual_grade: tk.Entry = tk.Entry(gui_root, justify="center", background=ENTRY_BACKGROUND, font=("arial", 15))
    manual_grade.pack(pady=5)
    created_gui_elements.append(manual_grade)

    def add_custom_grade() -> None:
        global grade

        current_name: str = student_name.get()

        if current_name != SPECIAL_STUDENT_NAME:
            remove_created_gui()

            return

        custom_grade_string: str = manual_grade.get()
        custom_grade: int = 0

        try:
            custom_grade = int(custom_grade_string)
        except:
            print(f"Tato známka nejde přidělit: {custom_grade_string}")
                
        if custom_grade < 1 or custom_grade > 5:
            print(f"Tato známka nejde přidělit: {custom_grade}")
                
        grade = custom_grade

        grade_student()
        save_data()

    manual_grade_confirm: tk.Button = tk.Button(gui_root, text="Přidat známku", command=add_custom_grade, background=BUTTON_BACKGROUND, font=("arial", 10))
    manual_grade_confirm.pack()
    created_gui_elements.append(manual_grade_confirm)

def create_gui_content() -> None:
    global main_grade_button

    gui_root: tk.Tk = tk.Tk()
    gui_root.title("Známkování")
    gui_root.geometry("400x400")
    gui_root.config(background=GUI_BACKGROUND)
    gui_root.resizable(False, False)

    label: tk.Label = tk.Label(gui_root, text="Zadat jméno studenta", background=GUI_BACKGROUND, font=("arial", 15))
    label.pack()

    student_name: tk.Entry

    def on_student_name_change(*args) -> None:
        global name, main_grade_button

        show_grades()

        if name != SPECIAL_STUDENT_NAME:
            remove_created_gui()

            main_grade_button.pack()
        else:
            special_student_gui(gui_root, student_name)

            main_grade_button.forget()

    student_name_variable: tk.StringVar = tk.StringVar()
    student_name_variable.trace_add("write", on_student_name_change)

    student_name = tk.Entry(gui_root, justify="center", background=ENTRY_BACKGROUND, font=("arial", 15), textvariable=student_name_variable)
    student_name.pack()

    checkbox_var: tk.IntVar = tk.IntVar()

    def change_user_creation_state() -> None:
        global create_user_allowed

        checkbox_state: int = checkbox_var.get()

        create_user_allowed = bool(checkbox_state)

    create_user: tk.Checkbutton = tk.Checkbutton(
        gui_root, text="Vytvořit studenta, pokuď neexistuje", command=change_user_creation_state, variable=checkbox_var, background=GUI_BACKGROUND,
        selectcolor="white", font=("arial", 10)
    )
    create_user.pack()

    def on_click() -> None:
        global name, grade, create_user_allowed

        grade = random.randint(1, 5)
        name = student_name.get()

        if name == SPECIAL_STUDENT_NAME:
            remove_created_gui()
        else:
            remove_created_gui()
            grade_student()
            save_data()
            show_grades()

    student_grades: tk.Label = tk.Label(gui_root, text="", background=GUI_BACKGROUND, wraplength=350)
    student_grades.pack()

    student_average: tk.Label = tk.Label(gui_root, text="", background=GUI_BACKGROUND, font=("arial", 10))
    student_average.pack()

    enter: tk.Button = tk.Button(gui_root, text="Přidělit známku", command=on_click, background=BUTTON_BACKGROUND, font=("arial", 10))
    enter.pack()

    main_grade_button = enter

    def show_grades() -> None:
        global name

        name = student_name.get()

        grades: list[int] = get_student_grades(name)
        grades_string: str = "Známky: "

        if len(grades) == 0:
            student_grades.config(text="")
            student_average.config(text="")

            return

        for grade in grades:
            grades_string += str(grade) + ", "
        
        grades_string = grades_string[0:len(grades_string) - 2]

        average_grade: float = get_average_grade(grades)

        average_grade_string: str = f"Průměr: {average_grade}"
        
        average_color: str = "black"

        if average_grade < 1.5:
            average_color = "green"
        elif average_grade < 2.5:
            average_color = "yellow"
        elif average_grade < 3.5:
            average_color = "orange"
        elif average_grade >= 3.5:
            average_color = "red"

        student_grades.config(text=grades_string)
        student_average.config(text=str(average_grade_string), foreground=average_color)

    gui_root.mainloop()

def main() -> None:
    load_data()

    create_gui_content()

if __name__ == "__main__":
    main()