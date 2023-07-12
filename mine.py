from tmuxer import Session

website = Session("web", "~/code/flask-sites", "RUN.py")
casbot = Session("casbot", "~/code/casbot", "bot.py")

website.start()
casbot.start()