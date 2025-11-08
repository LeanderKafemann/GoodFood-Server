from PyWSGIRef import *
import random
from typing import *

__version__ = "1.1.0--BETA"
APP_NAME = "GoodFood Server"

BETA.enable()

addSchablone("main", loadFromFile("./templates/main.pyhtml"))

def checkPwd(fs: FieldStorage) -> bool:
    try:
        with open("password.txt", "r") as f:
            stored_pwd = f.read().strip()
        input_pwd = fs.getvalue("password")
        if input_pwd is None:
            return False
        if isinstance(input_pwd, bytes):
            input_pwd = input_pwd.decode("utf-8")
        input_pwd = input_pwd.strip()
        random.seed(int(input_pwd))
        input_pwd_ = str(random.randint(0, 1000000000))
        return stored_pwd == input_pwd_
    except:
        return False

def returnDefault(content: str) -> Tuple[List[bytes], str, str]:
    return ([content.encode("utf-8")], "text/html", "200 OK")

def main(path: str, fs: FieldStorage):
    st = "200 OK"
    match path:
        case "/version":
            return returnDefault(__version__)
        case "/main":
            return returnDefault(SCHABLONEN["main"].decodedContext(globals()))
        case "/getDB":
            if checkPwd(fs):
                with open("database.db", "rb") as f:
                    return [f.read()], "application/octet-stream", "200 OK"
            else:
                return returnDefault("Invalid password!")
        case "/setDB":
            if checkPwd(fs):
                db_data = fs.getvalue("file")
                if isinstance(db_data, str):
                    db_data = db_data.encode("utf-8")
                with open("database.db", "wb") as f:
                    f.write(db_data)
                return returnDefault("Database updated successfully!")
            else:
                return returnDefault("Invalid password!")
        case "/getRooms":
            if checkPwd(fs):
                with open("rooms.txt", "r", encoding="utf-8") as f:
                    return returnDefault(f.read())
            else:
                return returnDefault("Invalid password!")
        case "/setRooms":
            if checkPwd(fs):
                rooms_data = fs.getvalue("rooms")
                if isinstance(rooms_data, bytes):
                    rooms_data = rooms_data.decode("utf-8")
                with open("rooms.txt", "w", encoding="utf-8") as f:
                    f.write(rooms_data)
                return returnDefault("Rooms updated successfully!")
            else:
                return returnDefault("Invalid password!")
        case "/stats":
            return returnDefault(STATS.export_stats())
        case "/" | _:
            return ([b"Not found..."], "text/plain", "404 Not Found")
app = makeApplicationObject(main, advanced=True, getStats=True, setAdvancedHeaders=True, customEncoding=True)

if __name__ == "__main__":
    server = setUpServer(app)
    print("Serving...")
    server.serve_forever()