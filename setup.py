import os, random, sqlite3
import pyautogui as py

if not "password.txt" in os.listdir():
    with open("password.txt", "w") as f:
        pwd_ = int(py.password(text="Set your password:", title="Password Setup"))
        random.seed(pwd_)
        f.write(str(random.randint(1, 1000000000)))

con = sqlite3.connect("database.db")
cur = con.cursor()
cur.execute("CREATE TABLE Defaultroom (name VARCHAR PRIMARY KEY, dates VARCHAR);")
cur.execute("INSERT INTO Defaultroom (name, dates) VALUES ('Default', '1.1.2000');")
con.commit()
con.close()

with open("rooms.txt", "w", encoding="utf-8") as f:
    f.write("defaultroom")

py.alert("Setup completed! Thanks for using Setup Wizard for GoodFoodServer 1.0", "Completed")