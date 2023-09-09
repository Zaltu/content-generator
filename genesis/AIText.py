"""
Subprocess a call to alpaca.cpp for AI text generation.
"""
import os

import subprocess
from threading import Thread, Event

EXEC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "alpaca-chat"))
MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(EXEC_PATH), "alpaca-model.bin"))
CHAT_START_COMMAND = [EXEC_PATH, "--model", MODEL_PATH]
PROMPT_COMMAND = [EXEC_PATH, "--model", MODEL_PATH, "-p"]


class AIBOT():
    def __init__(self):
        self.ready = False
        self.done = Event()
        self._observerThread = Thread(target=self._capture_output)
        self._subprocess = subprocess.Popen(CHAT_START_COMMAND, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, universal_newlines=True)
        self._observerThread.start()
        self.output = ""

    def chat(self, prompt):
        if not self.ready:
            return "Still processing previous request."
        prompt = prompt.replace("\n", "\\").removesuffix("\\")+"\n"
        self.ready = False
        self.done = Event()
        self._subprocess.stdin.write(prompt)
        self._subprocess.stdin.flush()
        if self.done.wait(timeout=60):
            return self.get_output()
        return "Timed out..."

    
    def get_output(self):
        if not self.output:
            return None
        boutput = self.output.removeprefix("\x1b[33m\n").removeprefix("> \x1b[1m\x1b[32m\x1b[0m").removesuffix("\x1b[0m\n")
        self.output = ""
        return boutput

    def _capture_output(self):
        for line in iter(self._subprocess.stdout.readline, ""):
            self.output+=line
            if line in [">", "\x1b[33m\n"] or line.endswith("\x1b[0m\n"):
                self.ready = True
                self.done.set()


    def exit(self):
        """
        Remember to terminate the process before it gains self-awareness.
        """
        self._subprocess.terminate()
        # terminating the process should end the readline loop
        self._observerThread.join()



def from_prompt(prompt):
    alpacas = subprocess.run(PROMPT_COMMAND+[prompt], capture_output=True, text=True, universal_newlines=True)
    return alpacas.stdout


if __name__ == "__main__":
    print(
        from_prompt("What does the fox say?")
    )
