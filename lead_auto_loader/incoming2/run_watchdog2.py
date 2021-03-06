#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import sys
import time
import subprocess


from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

logging.basicConfig(level=logging.ERROR)

class MyEventHandler(FileSystemEventHandler):
    def __init__(self, observer, filename):
        self.observer = observer
        self.filename = filename

    def on_created(self, event):
        #print "e=", event
        if not event.is_directory and event.src_path.endswith(self.filename):
            print "file created"
            self.observer.stop()

        #cwd = os.getcwd()  # Get the current working directory (cwd)
        #files = os.listdir(cwd)  # Get all the files in that directory
        #print("Files in '%s': %s" % (cwd, files))

        os.system('py -2 ../check_master2.py')

        # Because another file is created which is out_lead.json
        # Watchdog runs the clean_leads script again.
        # But because there is no lead.json because spider.py hasen't
        # It throws a missing file error.
        # Currently this is fine for now.
        # But eventually a solution should be for Watchdog to watch 
        # For specific file.

        # Watchdog runs the clean_leads.py with os.system.
        # Because the run_watchdog.py file is located in test_leads
        # When clean_leads.py is run
        # All files paths are relative to the run_watchdog.py file.

def main(argv=None):
    path = "."
    filename = "test"
    observer = Observer()
    event_handler = MyEventHandler(observer, filename)
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    observer.join()
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))