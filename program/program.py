import win32gui, win32api, time, codecs, asyncio, websockets, mysql.connector, bcrypt, sys
from datetime import datetime, timedelta
from keys import mas, first, letters, num, symb
from multiprocessing import Process, Queue
from win32api import GetSystemMetrics
import kivy

kivy.require('1.11.1')

connect = mysql.connector.connect(host='localhost', port=3306, user='smallbro', password='smallbro', database='smallbro')
cursor = connect.cursor()
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy import Config
from kivy.core.window import Window
from kivy.lang.builder import Builder

Config.set('graphics', 'multisamples', '0')
Config.set('graphics', 'resizable', '0')
Config.write()
Window.size = (600, 500)
Window.clearcolor = (0.6, 0.85, 0.9176, 1)
Window.left = (GetSystemMetrics(0) / 2) - (Window.size[0] / 2)
Window.top = (GetSystemMetrics(1) / 2) - (Window.size[1] / 2)
with open("file/my.kv", encoding='utf8') as f:
    presentation = Builder.load_string(f.read())
empty1 = 0
empty2 = 0


def new_time():
    global time_to_idle_m, time_to_idle_s
    time_to_idle_m = time.strftime("%M")
    time_to_idle_s = time.strftime("%S")


window_dict = {}
url_dict = {}
skip = None
new_time()
idle_start = 0
browsers = ['Google Chrome', 'Mozilla Firefox', 'Microsoft Edge', 'Internet Explorer', 'Opera']


def sql_insert(window):
    global connect, cursor
    name = {'name': window}
    cursor.execute("""SELECT * FROM apps WHERE name = %(name)s""", name)
    app = cursor.fetchall()
    if not app:
        cursor.execute("""INSERT INTO apps VALUES(null, %(name)s, null)""", name)
        connect.commit()
        cursor.execute("""SELECT * FROM apps WHERE name = %(name)s""", name)
        date = {'date': str(datetime.today().date()), 'app_id': int(cursor.fetchall()[0][0])}
    else:
        date = {'date': str(datetime.today().date()), 'app_id': int(app[0][0])}
    cursor.execute("""INSERT INTO sessions VALUES(null, null, %(date)s, %(app_id)s, null)""", date)
    connect.commit()


def add_window(title, start_time, all_time, end_time):
    window_dict.update({title: [start_time, all_time, end_time]})
    global skip
    if skip == 1:
        skip = None


def check_window(title):
    get = window_dict.get(title)
    if isinstance(get, list):
        if get[2] != '':
            time_n = datetime.now().time().strftime("%H:%M:%S")
            time_ = datetime.strptime(time_n, '%H:%M:%S') - datetime.strptime(get[2], '%H:%M:%S')
            if time_ >= timedelta(hours=0, minutes=1, seconds=0):
                sql_insert(title)
                return True
            else:
                return True
    else:
        sql_insert(title)
        return True


def sql_update(window, duration):
    global connect, cursor
    name = {'name': window}
    cursor.execute("""SELECT * FROM apps WHERE name = %(name)s""", name)
    sql_id = cursor.fetchall()[0][0]
    time_l = {'id': sql_id}
    cursor.execute("""SELECT * FROM sessions WHERE app_id = %(id)s ORDER BY id DESC LIMIT 1""", time_l)
    sql_time = cursor.fetchall()
    duration = str(duration).split(':')
    duration = (int(duration[0]) * 3600) + (int(duration[1]) * 60) + int(duration[2])
    if isinstance(sql_time[0][4], int):
        duration = sql_time[0][4] + int(duration)
    time_l = {'id': sql_id, 'time': duration}
    cursor.execute("""UPDATE sessions SET duration=%(time)s WHERE app_id = %(id)s ORDER BY id DESC LIMIT 1""", time_l)
    connect.commit()


def idle(idle_s):
    if isinstance(idle_s, str):
        idle_end = datetime.now().time().strftime("%H:%M:%S")
        duration = datetime.strptime(idle_end, '%H:%M:%S') - datetime.strptime(idle_s, '%H:%M:%S')
        sql_update("IDLE режим", duration)
        global idle_start, skip
        idle_start = 0
        skip = 1


def window_search():
    window = win32gui.GetForegroundWindow()
    active_window_name = win32gui.GetWindowText(window)
    if str(active_window_name) == '':
        active_window_name = "Windows"
    else:
        active_window_name = str(active_window_name).split(' - ')[-1]
    return str(active_window_name)


def browser_search():
    window = win32gui.GetForegroundWindow()
    active_window_name = win32gui.GetWindowText(window)
    return str(active_window_name)


def server(q):
    async def get_url(websocket, path):
        while True:
            url = await websocket.recv()
            url = str(url).split('/')
            q.put_nowait(url[2])

    Window.hide()
    start_server = websockets.serve(get_url, '127.0.0.1', 8080)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


def update(f_window, get):
    time_now = datetime.now().time().strftime("%H:%M:%S")
    time_all = datetime.strptime(time_now, '%H:%M:%S') - datetime.strptime(get, '%H:%M:%S')
    add_window(f_window, str(get), str(time_all), str(time_now))
    sql_update(f_window, time_all)


def program(q):
    Window.hide()
    first_window = window_search()
    window_start_time = str(datetime.now().time().strftime("%H:%M:%S"))
    add_window(first_window, window_start_time, '', '')
    sql_insert(first_window)
    global window_dict, url_dict, time_to_idle_m, idle_start, browsers
    url = 0
    while True:
        if (not q.empty()) & (first_window != browser_search()) & (window_search() != "Windows") & (
                window_search() in browsers):
            new_time()
            idle(idle_start)
            if not first_window.split(' - ')[-1] in browsers:
                get_w = window_dict.get(first_window)
                if isinstance(get_w, list) & (skip != 1):
                    update(first_window, get_w[0])
            if first_window.split(' - ')[-1] in browsers:
                get_w = window_dict.get(url)
                if isinstance(get_w, list) & (skip != 1):
                    update(url, get_w[0])
            url = q.get_nowait()
            first_window = browser_search()
            if check_window(url):
                add_window(url, str(datetime.now().time().strftime("%H:%M:%S")), '', '')
        if (first_window != window_search()) & (window_search() != "Windows") & (not window_search() in browsers):
            new_time()
            idle(idle_start)
            if not first_window.split(' - ')[-1] in browsers:
                get_w = window_dict.get(first_window)
                if isinstance(get_w, list) & (skip != 1):
                    update(first_window, get_w[0])
            if first_window.split(' - ')[-1] in browsers:
                get_w = window_dict.get(url)
                if isinstance(get_w, list) & (skip != 1):
                    update(url, get_w[0])
            first_window = window_search()
            if check_window(first_window):
                add_window(first_window, str(datetime.now().time().strftime("%H:%M:%S")), '', '')
        for m in mas:
            state_left = win32api.GetKeyState(m)
            if state_left != first[hex(m)][1]:
                first[hex(m)][1] = state_left
                if state_left < 0:
                    idle(idle_start)
                    # file.write("\n" + first[hex(m)][0])
                    new_time()
        min_ = 60 - int(time_to_idle_m)
        if min_ <= 1:
            idle_time = 0
        else:
            min_ = 0
            idle_time = int(time_to_idle_m)
        if ((int(time.strftime("%M")) + min_ - 1) == idle_time) & (int(time_to_idle_s) == int(time.strftime("%S"))):
            idle_start = str(datetime.now().time().strftime("%H:%M:%S"))
            get_w = window_dict.get(first_window)
            time_now = datetime.now().time().strftime("%H:%M:%S")
            time_all = datetime.strptime(time_now, '%H:%M:%S') - datetime.strptime(get_w[0], '%H:%M:%S')
            add_window(first_window, str(get_w[0]), str(time_all), str(time_now))
            sql_update(first_window, time_all)
            sql_insert("IDLE режим")
            time_to_idle_m = 0


process_1 = None
process_2 = None


def main():
    qe = Queue()
    global process_1, process_2
    process_1 = Process(target=server, args=(qe,))
    process_2 = Process(target=program, args=(qe,))
    process_1.start()
    process_2.start()


def signin(email, password):
    global connect, cursor
    email = {'email': email}
    cursor.execute("""SELECT * FROM users WHERE email = %(email)s""", email)
    user = cursor.fetchall()
    if len(user) == 0:
        error = "Такой почты не существует"
        return {'result': False, 'comment': error}
    elif user[0][2] != password:
        error = "Неправильный пароль"
        return {'result': False, 'comment': error}
    else:
        return {'result': True}


class LoginScreen(Screen):
    input1 = ObjectProperty(None)
    error1 = ObjectProperty(None)
    input2 = ObjectProperty(None)
    error2 = ObjectProperty(None)
    pass

    def check_email(self):
        error_msg = 0
        global empty1
        if (len(self.input1.text) == 0) & (empty1 == 0):
            empty1 = 1
        elif (len(self.input1.text) == 0) & (empty1 == 1):
            error_msg = 'Поле не может быть пустым'
        elif self.input1.text.find('@') == -1:
            error_msg = 'Введён неправильный или некорректный e-mail'
        elif self.input1.text.split('@')[1].find('.') == -1:
            error_msg = 'Введён неправильный или некорректный e-mail'
        elif (self.input1.text.split('@')[0] == '') | (self.input1.text.split('@')[1] == ''):
            error_msg = 'Введён неправильный или некорректный e-mail'
        elif (len(self.input1.text.split('@')[1].split('.')[1]) < 2) | (
                len(self.input1.text.split('@')[1].split('.')[1]) > 63):
            error_msg = 'Введён неправильный или некорректный e-mail'
        elif (self.input1.text.find(' ') != -1) | (len(self.input1.text) > 320):
            error_msg = 'Введён неправильный или некорректный e-mail'
        if isinstance(error_msg, str):
            self.error1.text = error_msg
            self.error1.size_hint = 1, None
            self.error1.size = 0, 20
        else:
            if self.error1.text != "Такой почты не существует":
                self.error1.text = ''
                self.error1.size_hint = 1, 0
                self.error1.size = 0, 0

    def check_pass(self):
        error_msg = 0
        global empty2
        if (len(self.input2.text) == 0) & (empty2 == 0):
            empty2 = 1
        elif (len(self.input2.text) == 0) & (empty2 == 1):
            error_msg = 'Поле не может быть пустым'
        elif (len(self.input2.text) < 6) & (empty2 == 1):
            error_msg = 'Пароль должен состоять минимум из 6 символов'
        else:
            error_msg = self.symbol(letters)
            if error_msg == 0:
                error_msg = self.symbol(num)
            if error_msg == 0:
                error_msg = self.symbol(symb)
        if isinstance(error_msg, str):
            self.error2.text = error_msg
            self.error2.size_hint = 1, None
            self.error2.size = 0, 20
        else:
            if self.error2.text != "Неправильный пароль":
                self.error2.text = ''
                self.error2.size_hint = 1, 0
                self.error2.size = 0, 0

    def symbol(self, symb):
        count = 0
        for let in symb:
            if (self.input2.text.lower().find(let) != -1) & (count <= 2):
                count += 1
                if self.input2.text.lower().find(let) != self.input2.text.lower().rfind(let):
                    count += 1
            if count == 2:
                break
        if count != 2:
            return 'Пароль должен содержать минимум 2 буквы, цифры и спец. символа'
        else:
            return 0

    def sign(self):
        error = signin(self.input1.text, self.input2.text)
        if not error['result']:
            if error['comment'] == "Такой почты не существует":
                self.error1.text = error['comment']
                self.error1.size_hint = 1, None
                self.error1.size = 0, 20
            elif error['comment'] == "Неправильный пароль":
                self.error2.text = error['comment']
                self.error2.size_hint = 1, None
                self.error2.size = 0, 20
        elif error['result']:
            self.error1.text = self.error2.text = ''
            self.error1.size_hint = self.error2.size_hint = 1, 0
            self.error1.size = self.error2.size = 0, 0
            self.manager.current = 'program'


class ProgramScreen(Screen):
    pass

    def start(self):
        main()


sm = ScreenManager()
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(ProgramScreen(name='program'))


class MyApp(App):

    def build(self):
        self.title = "Вход"
        return sm

    def on_stop(self):
        global connect, process_2, process_1
        process_1.kill()
        process_2.kill()
        connect.commit()
        connect.close()


if __name__ == '__main__':
    MyApp().run()
