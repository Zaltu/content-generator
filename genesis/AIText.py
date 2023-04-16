"""
Subprocess a call to alpaca.cpp for AI text generation.
"""
import os

import subprocess
from threading import Thread

EXEC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "alpaca-chat"))
PROMPT_COMMAND = [EXEC_PATH, "-p"]


class AIBOT():
    def __init__(self):
        self._observerThread = Thread(target=self._print_output)
        self._subprocess = subprocess.Popen(EXEC_PATH, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, universal_newlines=True)
        self._observerThread.start()
        self.ready = False
        self.output = ""

    def chat(self, prompt):
        if not self.ready:
            return "Still processing previous request."
        self.ready = False
        self._subprocess.stdin.write(prompt)
        self._subprocess.stdin.flush()
    
    def get_output(self):
        if not self.output:
            return None
        boutput = self.output.removeprefix("\x1b[33m\n").removeprefix("> \x1b[1m\x1b[32m\x1b[0m").removesuffix("\x1b[0m\n")
        self.output = ""
        return boutput
    

    def _print_output(self):
        for line in iter(self._subprocess.stdout.readline, ""):
            if (line == token for token in [">", "\x1b[33m\n"]):
                self.ready = True
            self.output+=line


    def exit(self):
        """
        Remember to terminate the process before it gains self-awareness.
        """
        self._subprocess.terminate()
        # terminating the process should end the readline loop
        self._observerThread.join()



def from_prompt(prompt):
    print(prompt)
    alpacas = subprocess.run(PROMPT_COMMAND+[prompt], capture_output=True, text=True)
    return alpacas.stdout


if __name__ == "__main__":
    print(from_prompt("What does the fox say?"))
