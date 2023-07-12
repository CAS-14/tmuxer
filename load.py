import tmuxer

sessions = tmuxer.import_file("sessions.txt")

for session in sessions:
    session.restart()