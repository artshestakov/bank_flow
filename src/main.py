from svc_bot.main import main as bot
from svc_register.main import main as register
import threading

if __name__ == "__main__":
    t_bot = threading.Thread(target=bot)
    t_register = threading.Thread(target=register)

    t_bot.start()
    t_register.start()

    t_bot.join()
    t_register.join()
