from flask import Flask, request
import os
import json
import subprocess

app = Flask(__name__)


class SignalApplication:

    def __init__(self):
        self.signal_application_pid = subprocess.Popen(
            SignalApplication.__signal_command(["daemon", "--system"])).pid
        from time import sleep
        sleep(1)
        print("Process started")

    @staticmethod
    def __signal_command(command):
        return [f'/{os.environ["SIGNAL_CLI_PATH"]}/bin/signal-cli',
                "--config",
                os.environ["SIGNAL_CONFIG_PATH"],
                "-u",
                os.environ["PHONE_NUMBER"],
                *command]

    def send_message(self, number, message_to_send, attachement=None):
        my_command = subprocess.run(([f'/{os.environ["SIGNAL_CLI_PATH"]}/bin/signal-cli', '--dbus-system', 'send', '-m', message_to_send, number]), capture_output=True)
        print(my_command)


signal = SignalApplication()


@app.route('/message', methods=['POST'])
def message():
    message_to_send = request.get_json()
    print(json.dumps(message_to_send, indent=4, sort_keys=True))
    number = message_to_send['number']
    message_content = message_to_send['content']
    signal.send_message(number, message_content)
    return "ok"


if __name__ == "__main__":
    app.run(debug=False)
