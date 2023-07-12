import subprocess
import os

def tmux_run(command: str) -> str:
    return subprocess.getoutput(f"tmux {command}")

def tmux_sendcommand(session: str, command: str) -> str:
    sk_out = tmux_run(f"send-keys -t {session} \"{command}\" C-m")
    if sk_out:
        log(f"Session '{session}': message when sending command '{command}' as follows:\n{sk_out}")
    return sk_out

def log(message: str):
    print(f"[tmuxer] {message}")

def import_file(filename: str) -> list:
    if not os.path.isfile(filename):
        log(f"File '{filename}' does not exist!")

    with open(filename, "r") as f:
        data = f.read()

    sessions = []
    for line in data.splitlines():
        line = line.strip()
        
        if line[0] == "#":
            continue
        
        line_split = line.split("\t")
        if len(line_split) != 3:
            continue
        
        sessions.append(Session(*line_split))

    if not sessions:
        return None
    
    return sessions

class Session:
    def __init__(self, name: str, directory: str, pyscript: str):
        self.name = name
        self.directory = os.path.expanduser(directory)
        self.pyscript = pyscript

    def start(self):
        ns_out = tmux_run(f"new-session -d -s {self.name}")
        
        if ns_out:
            if ns_out == f"duplicate session: {self.name}":
                log(f"Session '{self.name}' start: A session with that name already exists!")
            else:
                log(f"Session '{self.name}' start: tmux error as follows:\n{ns_out}")

            return ns_out

        tmux_sendcommand(self.name, f"cd '{self.directory}'")
        tmux_sendcommand(self.name, f"python3 '{self.pyscript}'")

        log(f"Session '{self.name}' has been started and commands have been sent!")

    def kill(self):
        kill_out = tmux_run(f"kill-session -t {self.name}")
        if kill_out:
            if kill_out == f"can't find session: {self.name}":
                log(f"Session '{self.name}' kill: not started so can't be killed!")
            else:
                log(f"Session '{self.name}' kill: tmux error as follows:\n{kill_out}")

            return kill_out
        
        log(f"Session '{self.name}' killed successfully!")

    def exists(self):
        list_out = tmux_run("list-sessions")

        if list_out.startswith("no server running on") or not list_out:
            return False

        else:
            session_names = []
            for line in list_out.splitlines():
                session_names.append(line.split(":")[0])

            if self.name in session_names:
                return True
            else:
                return False
        
    def restart(self):
        if self.exists():
            self.kill()
            self.start()
            log(f"Session '{self.name}' restarted")

        else:
            self.start()
            log(f"Session '{self.name}' restarted -> started")
