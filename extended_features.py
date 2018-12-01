# Provides useful functions

import os
import sys
import argparse
import subprocess
import signal

# Default arguments
ex_parser = argparse.ArgumentParser()
ex_parser.add_argument("-V", "--version",action="store_true", help="Show version")
ex_parser.add_argument("-q", "--quiet", action="store_true", help="Disable output")
ex_parser.add_argument("--no-color", action="store_true", help="Disable colored output")
ex_parser.add_argument("--dry-run", action="store_true", help="Run without making changes")
ex_parser.add_argument("-v", "--verbose", action="store_true", help="Show verbose output")
ex_parser.add_argument("-d", "--debug", action="store_true", help="Show debug output")
ex_parser.add_argument("--no-warn", action="store_true", help="Disable warnings")
ex_parser.add_argument("--no-error", action="store_true", help="Disable errors")

# Allow the user to define more arguments in the main script.
options, args = ex_parser.parse_known_args()

# Bash Terminal Colors
bcolors = {
    "red"     : "\033[31m",
    "green"   : "\033[32m",
    "yellow"  : "\033[33m",
    "blue"    : "\033[34m",
    "purple"  : "\033[35m",
    "cyan"    : "\033[36m",
    "normal"  : "\033[0m"
}

# Instead of checking the args on every call, check once
# and if it shouldn't run, define it as a do nothing function.
# Modifying flags during the running of the program will no
# re-enable these functions.

if options.quiet:
    def print_color(*args, **kwargs):
        pass
elif options.no_color:
    def print_color(*args, **kwargs):
        for arg in args:
            print(arg)
else:
    def print_color(*args, color="normal"):
        # Get color or default to normal.
        color = bcolors.get(color, bcolors["normal"])
        for arg in args:
            print(color + arg + bcolors["normal"])

# FYI, these functions depend on print_color
if options.verbose:
    def print_verbose(*args):
        for arg in args:
            print_color("VERBOSE: {}".format(arg), color="normal")
else:
    def print_verbose(*args):
        pass

if options.debug:
    def print_debug(*args):
        for arg in args:
            print_color("DEBUG: {}".format(arg), color="cyan")
else:
    def print_debug(*args):
        pass

if options.no_warn:
    def print_warn(*args):
        pass
else:
    def print_warn(*args):
        for arg in args:
            print_color("WARN: {}".format(arg), color="yellow")

if options.no_error:
    def print_error(*args):
        pass
else:
    def print_error(*args):
        for arg in args:
            print_color("ERROR: {}".format(arg), color="red")

# Version Check
def RequireVersion(version):
    if sys.version_info[0] < version:
        print_error("Python {} or higher is required.".format(version))
        sys.exit(1)

# Root Check
def require_root():
    if (os.geteuid() != 0):
        print_error("This script must be run as root")
        sys.exit(-1)

def require_file(path, type="file", provider="none"):
    """
    Checks if a required file is present. 
    Allows additional information such as filetype (file, deb, csv)
    and provider (apt, github)
    """
    
    if not os.path.isfile(path):
        print_error("File Required: {}".format(path))
        sys.exit(-1)
        
def require_single_instance(process_name):
    """
    Checks if a process of the same name already exists and terminates if one does.
    """
    
    # Restrict results to only python processes
    child = subprocess.Popen("""pgrep -lf python |
                             grep {} |
                             grep -v grep |
                             grep -v {}""".format(process_name, os.getpid())
                            shell=True, stdout=subprocess.PIPE)
    child.communicate()[0]
    if (child.returncode == 0):
        print_warn("Process already running. Terminating.")
        sys.exit(-1)
        
def lock_file(path, message=os.getpid()):
    lockfile = "{0}.lock".format(path)
    if not os.path.isfile(lockfile):
        try:
            f = open(lockfile, "w")
            f.write(str(message))
            f.close()
        except OSError as e:
            print_error(e)
    else:
        print_warn("Lockfile already exists")

def unlock_file(path):
    lockfile = "{0}.lock".format(path)
    is os.path.isfile(lockfile):
        try:
            os.remove(lockfile)
        except OSError as e:
            print_error(e)

def test_lockfile(path):
    lockfile = "{0}.lock".format(path)
    if os.path.isfile(lockfile):
        return True
    else:
        return False
    
class GracefulKiller:
    """
    Ref: https://stackoverflow.com/a/31464349/5339918/
    
    Catches terminations and interrupts that can be tested for
    at regular intervals and allow graceful process shutdown.
    """
    
    kill_now = False
    warn = False
    
    def __init__(self, warn=False):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)
        self.warn = warn
        
    def exit_gracefully(self, signum, frame):
        if self.warn:
            print_warn("Termination signal caught. Stopping...")
        self.kill_now = True
