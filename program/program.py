import win32gui, win32api, datetime, time, codecs, os
from keys import mas, first

"""Запуск сервера для обработки поступающей из расширения информации"""
os.popen("python server.py")

now = datetime.datetime.now()
file = codecs.open('program.txt', 'a', "utf-8")
file.write("\n\nProgram is running\n" + (time.strftime("%Y-%m-%d | %H:%M:%S")))
time_to_idle = time.strftime("%M")


def window_search():
    window = win32gui.GetForegroundWindow()
    active_window_name = win32gui.GetWindowText(window)
    return active_window_name


first_window = str(window_search())
file.write("\n" + first_window)
file.close()
while __name__ == "__main__":
    file = codecs.open('program.txt', 'a', "utf-8")
    if first_window != str(window_search()):
        time_to_idle = time.strftime("%M")
        if str(window_search()) == '':
            file.write("\nWindows")
            first_window = str(window_search())
        else:
            file.write("\n" + str(window_search()))
            first_window = str(window_search())
    for m in mas:
        state_left = win32api.GetKeyState(m)
        if state_left != first[hex(m)][1]:
            first[hex(m)][1] = state_left
            if state_left < 0:
                file.write("\n" + first[hex(m)][0])
                time_to_idle = time.strftime("%M")
    min_ = 60 - int(time_to_idle)
    if min_ <= 10:
        if (int(time.strftime("%M")) + min_ - 10) == 0:
            file.write("\nОсуществлён переход в IDLE режим " + time.strftime("%Y-%m-%d") + " в " + time.strftime("%H:%M"))
            time_to_idle = 0

    else:
        if (int(time.strftime("%M")) - 10) == int(time_to_idle):
            file.write("\nОсуществлён переход в IDLE режим " + time.strftime("%Y-%m-%d") + " в " + time.strftime("%H:%M"))
            time_to_idle = 0
    file.close()
