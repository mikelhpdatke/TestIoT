import os
import time
import subprocess
import shlex
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Watcher:
    DIRECTORY_TO_WATCH = "/home/tom/test/"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif (event.event_type == 'created' and (event.src_path.find(".pcap") != -1)):
            # Take any action here when a file is first created.
            #proc = subprocess.Popen('bro', '-r',event.src_path, 'darpa2gurekddcup.bro','>','conn.list',stdout=subprocess.PIPE)
            #proc = subprocess.Popen('./a.out','conn.list')
            #proc = subprocess.Popen('ls','-lah', stdout=subprocess.PIPE)
            #tmp = proc.stdout.read()

            time.sleep(2)
            cmd = "bro -r " + event.src_path + " darpa2gurekddcup.bro >> conn.list"
            try:
                if (os.system(cmd) == 0):
                    cmd2 = "/home/tom/test/a.out conn.list"
                    args = shlex.split(cmd2)
                    proc = subprocess.Popen(args, stdout=subprocess.PIPE)
                    proc.wait()
                    print (proc.stdout.read())
            except:
                pass
        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            pass


if __name__ == '__main__':
    w = Watcher()
    w.run()
