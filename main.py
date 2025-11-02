from PyWSGIRef import *
import random

__version__ = "0.3.0"
APP_NAME = "GoodFood Server"

BETA.enable()

addSchablone("main", loadFromFile("./templates/main.pyhtml"))

def checkPwd(fs: FieldStorage) -> bool:
    try:
        with open("password.txt", "r") as f:
            stored_pwd = f.read().strip()
        input_pwd = fs.getvalue("password").strip()
        random.seed(int(input_pwd))
        input_pwd_ = str(random.randint(0, 1000000000))
        return stored_pwd == input_pwd_
    except:
        return False

def main(path: str, fs: FieldStorage):
    match path:
        case "/version":
            return __version__
        case "/main":
            return SCHABLONEN["main"].decodedContext(globals())
        case "/getDB":
            if checkPwd(fs):
                with open("database.db", "rb") as f:
                    return f.read()
            else:
                return "Invalid password!"
        case "/setDB":
            if checkPwd(fs):
                db_data = fs.getvalue("file")
                with open("database.db", "wb") as f:
                    f.write(db_data)
                return "Database updated successfully!"
            else:
                return "Invalid password!"
        case "/getRooms":
            if checkPwd(fs):
                with open("rooms.txt", "r", encoding="utf-8") as f:
                    return f.read()
            else:
                return "Invalid password!"
        case "/setRooms":
            if checkPwd(fs):
                rooms_data = fs.getvalue("rooms")
                with open("rooms.txt", "w", encoding="utf-8") as f:
                    f.write(rooms_data)
                return "Rooms updated successfully!"
            else:
                return "Invalid password!"
        case "/stats":
            return STATS.export_stats()
        case "/" | _:
            return "Not found..."
app = makeApplicationObject(main, advanced=True, getStats=True, customEncoding=True, setContentType=True)

if __name__ == "__main__":
    server = setUpServer(app)
    print("Serving...")
    server.serve_forever()