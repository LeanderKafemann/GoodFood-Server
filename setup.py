import os, random
import pyautogui as py

if not "password.txt" in os.listdir():
    with open("password.txt", "w") as f:
        pwd_ = int(py.password(text="Set your password:", title="Password Setup"))
        random.seed(pwd_)
        f.write(str(random.randint(0, 1000000000)))
py.alert("Setup completed! Thanks for using Setup Wizard for GoodFoodServer 1.0", "Completed")