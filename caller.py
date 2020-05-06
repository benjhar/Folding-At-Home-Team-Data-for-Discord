import subprocess
import atexit
import datetime
import sys

popen = None

def execute(cmd, log_timestamps=False):
    try:
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
        print(f'New child created [{datetime.datetime.now()}]') if log_timestamps else print('New child created')
        for stdout_line in iter(popen.stdout.readline, ""):
            yield stdout_line
        popen.stdout.close()
        return_code = popen.wait()
        if return_code:
            print(return_code)
            return
    except KeyboardInterrupt:
        print("Manual shutdown requested... killing process and child.")
        popen.kill()
        sys.exit()


def update():
    print(f'{"-"*10}{"\n"*4}')
    for path in execute(["yes", "|", "git", "pull", "https://github.com/thenamesweretakenalready/Folding-At-Home-Team-Data-for-Discord"]):
        print(path, end="")
    print(f'{"-"*10}{"\n"*4}')


if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) > 1:
        if sys.argv[1] == "-log_timestamps":
            while True:
                for path in execute(["python3", "bot.py"], log_timestamps=True):
                    print(path, end="")
    else:
        while True:
            for path in execute(["python3", "bot.py"]):
                if path in ['restart', 'update']:
                    if path == 'restart':
                        print('Automatic restart requested... killing child and restarting.')
                        popen.kill()
                    else:
                        print('Automatic update requested... killing child and beginning update.')
                        popen.kill()
                        update()
                else:
                    print(path, end="")

    atexit.register(popen.kill)
