const userInput = document.querySelector("#user-input")
const manualGrade = document.querySelector("#manual-grade")
const submitButton = document.querySelector("#submit-button")
const resetDataButton = document.querySelector("#reset-data")

const specialStudentName = "Šimon"

const inputStates = Object.freeze({
    ENTER_NAME: "ENTER_NAME",
    ENTER_GRADE: "ENTER_GRADE"
})
let inputState = inputStates.ENTER_NAME

let userData = localStorage.getItem("userData")
if (!userData) {
    userData = {
        students: []
    }
}
else {
    userData = JSON.parse(userData)
}

function changeBackgroundColor(grade) {
    const bodyStyle = document.body.style

    switch (grade) {
        case 1:
            bodyStyle.background = "linear-gradient(45deg, limegreen, green)"

            break
        case 2:
            bodyStyle.background = "linear-gradient(45deg, green, yellow)"

            break
        case 3:
            bodyStyle.background = "linear-gradient(45deg, yellow, orange)"

            break
        case 4:
            bodyStyle.background = "linear-gradient(45deg, orange, red)"

            break
        default:
            bodyStyle.background = "linear-gradient(45deg, red, darkred)"

            break
    }
}

function handleData(grade, name) {
    let studentExists = false

    for (let i = 0; i < userData.students.length; i++) {
        const student = userData.students[i]

        if (student.name !== name) continue

        studentExists = true

        student.grades.push(grade)
    }

    if (!studentExists) {
        let newStudent = {
            name: name,
            grades: [grade]
        }

        userData.students.push(newStudent)
    }

    changeBackgroundColor(grade)

    localStorage.setItem("userData", JSON.stringify(userData))

    userInput.value = ""
    manualGrade.value = ""
    userInput.readOnly = false

    userInput.focus()
}

function userInputSubmit() {
    let grade = Math.floor(Math.random() * 5) + 1
    let name = userInput.value

    if (name === specialStudentName) {
        manualGrade.style.display = "block"
        userInput.readOnly = true

        inputState = inputStates.ENTER_GRADE

        manualGrade.focus()
    }
    else {
        handleData(grade, name)
    }
}

function manualGradeSubmit() {
    let input = manualGrade.value
    let grade = parseInt(input)

    if (!grade) {
        console.warn("Známka nemůže být " + grade)

        return
    }

    if (grade < 1 || grade > 5) {
        console.warn("Známka musí být v rozmezí 1-5")

        return
    }

    handleData(grade, specialStudentName)

    manualGrade.style.display = "none"

    inputState = inputStates.ENTER_NAME
}

userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        userInputSubmit()
    }
})

manualGrade.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        manualGradeSubmit()
    }
})

submitButton.addEventListener("click", () => {
    if (inputState === inputStates.ENTER_NAME) {
        userInputSubmit()
    }
    else if (inputState === inputStates.ENTER_GRADE) {
        manualGradeSubmit()
    }
})

resetDataButton.addEventListener("click", () => {
    localStorage.removeItem("userData")

    window.location = ""
})