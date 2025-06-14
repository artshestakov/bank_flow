from svc_bot.main import main as bot
from svc_register.main import main as register
from svc_card.main import main as card
from svc_transaction.main import main as transaction
from svc_notify.main import main as notify
from svc_profile.main import main as profile
from svc_audit.main import main as audit
# ----------------------------------------------------------------------------------------------------------------------
import threading
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":

    t_bot = threading.Thread(target=bot)
    t_register = threading.Thread(target=register)
    t_card = threading.Thread(target=card)
    t_transaction = threading.Thread(target=transaction)
    t_notify = threading.Thread(target=notify)
    t_profile = threading.Thread(target=profile)
    t_audit = threading.Thread(target=audit)

    t_bot.start()
    t_register.start()
    t_card.start()
    t_transaction.start()
    t_notify.start()
    t_profile.start()
    t_audit.start()

    t_bot.join()
    t_register.join()
    t_card.join()
    t_transaction.join()
    t_notify.join()
    t_profile.join()
    t_audit.join()
# ----------------------------------------------------------------------------------------------------------------------
