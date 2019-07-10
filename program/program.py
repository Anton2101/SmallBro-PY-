import win32gui, win32api, time, codecs, asyncio, websockets, mysql.connector
from datetime import datetime, timedelta
from keys import mas, first
from multiprocessing import Process, Queue


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
    connect = mysql.connector.connect(host='localhost', port=3306, user='root', password='root',
                                      database='small_bro')
    cursor = connect.cursor()
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
    connect.close()


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
    connect = mysql.connector.connect(host='localhost', port=3306, user='root', password='root',
                                      database='small_bro')
    cursor = connect.cursor()
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
    connect.close()


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

    start_server = websockets.serve(get_url, '127.0.0.1', 8080)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


def update(f_window, get):
    time_now = datetime.now().time().strftime("%H:%M:%S")
    time_all = datetime.strptime(time_now, '%H:%M:%S') - datetime.strptime(get, '%H:%M:%S')
    add_window(f_window, str(get), str(time_all), str(time_now))
    sql_update(f_window, time_all)


def main(q):
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


if __name__ == '__main__':
    qe = Queue()
    process_1 = Process(target=server, args=(qe,))
    process_2 = Process(target=main, args=(qe,))
    process_1.start()
    process_2.start()
    process_1.join()
    process_2.join()
    process_1.close()
    process_2.close()
