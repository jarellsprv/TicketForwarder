from Logger import logger
from Config import CONFIG
from Functions import check_inbox
import time, imaplib


def main():
    logger.info("Made by Jarell 👻👻")
    mail = imaplib.IMAP4_SSL(CONFIG["IMAP_SERVER"], CONFIG["IMAP_PORT"])
    mail.login(CONFIG["EMAIL_ACCOUNT"], CONFIG["APP_PASSWORD"])
    logger.suc(f"Successfully logged into the email {CONFIG["EMAIL_ACCOUNT"]}")

    while True:
        try:
            logger.info("Checking inbox..")
            check_inbox(mail)
            logger.info("Finished Checking inbox.. Waiting 30 seconds.")
            time.sleep(30)

        except Exception as e:
            logger.err(f"Error happened. {e}")


if __name__ == "__main__":
    main()
