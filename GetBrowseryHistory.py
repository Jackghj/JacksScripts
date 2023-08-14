### Get full history from Chrome, firefox and edge from all users on a computer.
import sqlite3
import shutil
import os
import datetime
import time
import ctypes

user_directories = [d for d in os.listdir("C:\\Users") if os.path.isdir(f"C:\\Users\\{d}")]

for user in user_directories:
    history_file = f"C:\\Users\\{user}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History"
    if os.path.exists(history_file):
        shutil.copyfile(history_file, "C:\\Temp\\History")
        con = sqlite3.connect("C:\\Temp\\History")
        cur = con.cursor()

        for row in cur.execute('SELECT * from urls ORDER BY last_visit_time DESC;'):
            timestamp = int(row[5])
            date = datetime.datetime(1601,1,1) + datetime.timedelta(microseconds=timestamp)
            formatted_date = date.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{user};Chrome;{formatted_date};{row[1]};{row[2]};")
        
        con.close()
        os.remove("C:\\Temp\\History")

    firefox_dir = f"C:\\Users\\{user}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles"
    if os.path.exists(firefox_dir):
        for folder in os.listdir(firefox_dir):
            history_file = os.path.join(firefox_dir, folder, 'places.sqlite')
            if os.path.exists(history_file):
                shutil.copyfile(history_file, "C:\\Temp\\History_Firefox")
                con = sqlite3.connect("C:\\Temp\\History_Firefox")
                cur = con.cursor()
                for row in cur.execute('SELECT v.visit_date, u.url, u.title FROM moz_historyvisits v JOIN moz_places u ON v.place_id = u.id ORDER BY v.visit_date DESC;'):
                    timestamp = row[0]
                    date = datetime.datetime.fromtimestamp(timestamp/1000000)
                    formatted_date = date.strftime("%Y-%m-%d %H:%M:%S")
                    print(f"{user};Firefox;{formatted_date};{row[1]};{row[2]};")
                con.close()
                os.remove("C:\\Temp\\History_Firefox")
                break
        else:
            pass
    else:
        pass
    
    
    edge_history_file = f"C:\\Users\\{user}\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\History"
    if os.path.exists(edge_history_file):
        shutil.copyfile(edge_history_file, "C:\\Temp\\History_Edge")
        con = sqlite3.connect("C:\\Temp\\History_Edge")
        cur = con.cursor()
        for row in cur.execute('SELECT * from urls ORDER BY last_visit_time DESC;'):
            timestamp = int(row[5])
            date = datetime.datetime(1601,1,1) + datetime.timedelta(microseconds=timestamp)
            formatted_date = date.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{user};Edge;{formatted_date};{row[1]};{row[2]};")
        con.close()
        os.remove("C:\\Temp\\History_Edge")
else:
    pass