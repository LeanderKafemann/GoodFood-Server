from PyWSGIRef import *
import random
from typing import *

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

def returnDefault(content: str) -> Tuple[List[str], str, str]:
    return ([content.encode("utf-8")], "text/html", "200 OK")

def main(path: str, fs: FieldStorage):
    st = "200 OK"
    match path:
        case "/version":
            returnDefault(__version__)
        case "/main":
            returnDefault(SCHABLONEN["main"].decodedContext(globals()))
        case "/getDB":
            if checkPwd(fs):
                with open("database.db", "rb") as f:
                    return [f.read()], "application/octet-stream", "200 OK"
            else:
                returnDefault("Invalid password!")
        case "/setDB":
            if checkPwd(fs):
                db_data = fs.getvalue("file")
                with open("database.db", "wb") as f:
                    f.write(db_data)
                returnDefault("Database updated successfully!")
            else:
                returnDefault("Invalid password!")
        case "/getRooms":
            if checkPwd(fs):
                with open("rooms.txt", "r", encoding="utf-8") as f:
                    returnDefault(f.read())
            else:
                returnDefault("Invalid password!")
        case "/setRooms":
            if checkPwd(fs):
                rooms_data = fs.getvalue("rooms")
                with open("rooms.txt", "w", encoding="utf-8") as f:
                    f.write(rooms_data)
                returnDefault("Rooms updated successfully!")
            else:
                returnDefault("Invalid password!")
        case "/stats":
            returnDefault(STATS.export_stats())
        case "/" | _:
            return ["Not found..."], "text/plain", "404 Not Found"
app = makeApplicationObject(main, advanced=True, getStats=True, setAdvancedHeaders=True, customEncoding=True)

if __name__ == "__main__":
    server = setUpServer(app)
    print("Serving...")
    server.serve_forever()