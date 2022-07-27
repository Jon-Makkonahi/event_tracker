import pickle
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

Form, Window = uic.loadUiType("tracker.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()


def save_to_file():
    global start_date, calc_date, description
    data_to_save = {
        "start": start_date,
        "end": calc_date,
        "description": description
    }
    file1 = open("configuration.txt", "wb")
    pickle.dump(data_to_save, file1)
    file1.close()

def read_from_file():
    global start_date, calc_date, description, now_date
    try:
        file1 = open("configuration.txt", "rb")
        data_to_load = pickle.load(file1)
        file1.close()
        start_date = data_to_load["start"]
        calc_date = data_to_load["end"]
        description = data_to_load["description"]
        form.calendarWidget.setSelectedDate(calc_date)
        form.dateEdit.setDate(calc_date)
        form.plainTextEdit.setPlainText(description)
        delta_days_left = start_date.daysTo(now_date)
        delta_days_right = now_date.daysTo(calc_date)
        days_total = start_date.daysTo(calc_date)
        procent = int(delta_days_left * 100 / days_total)
        form.progressBar.setProperty("value", procent)
    except:
        print("Невозможно прочитать файл")

def on_click():
    global calc_date, description, start_date
    start_date = now_date
    calc_date = form.calendarWidget.selectedDate()
    description = form.plainTextEdit.toPlainText()
    save_to_file()

def on_click_calendar():
    global start_date, calc_date
    form.dateEdit.setDate(form.calendarWidget.selectedDate())
    calc_date = form.calendarWidget.selectedDate()
    delta_days = start_date.daysTo(calc_date)
    form.label_3.setText("До события осталось:  %s дней" % delta_days)

def on_dateedit_change():
    global start_date, calc_date
    form.calendarWidget.setSelectedDate(form.dateEdit.date())
    calc_date = form.dateEdit.date()
    delta_days = start_date.daysTo(calc_date)
    form.label_3.setText("До события осталось:  %s дней" % delta_days)

form.pushButton.clicked.connect(on_click)
form.calendarWidget.clicked.connect(on_click_calendar)
form.dateEdit.dateChanged.connect(on_dateedit_change)

start_date = form.calendarWidget.selectedDate()
now_date = form.calendarWidget.selectedDate()
calc_date = form.calendarWidget.selectedDate()
description = form.plainTextEdit.toPlainText()
read_from_file()

form.label.setText("Трекер события от %s " % start_date.toString('dd.MM.yyyy'))
on_click_calendar()

app.exec_()
