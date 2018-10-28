# Provides useful functions for a new script.

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--version",action="store_true", help="Show version")
parser.add_argument("-q", "--quiet", action="store_true", help="Disable output")
parser.add_argument("--no-color", action="store_true", help="Disable colored output")
parser.add_argument("--dry-run", action="store_true", help="Run without making changes")
parser.add_argument("--verbose", action="store_true", help="Show verbose output")
parser.add_argument("--debug", action="store_true", help="Show debug output")
parser.add_argument("--warn", action="store_true", help="Show warnings")
parser.add_argument("--error", action="store_true", help="Show errors")
args = parser.parse_args()

# Terminal Colors
bcolors = {
    "cyan"  : "\033[96m",
    "yellow": "\033[93m",
    "red"   : "\033[91m",
    "normal"  : "\033[0m"
}

# Instead of checking the args on every call, check once
# and if it shouldn't run, define it as a do nothing function.
# Modifying flags during the running of the program will no
# re-enable these functions.

if args.quiet:
    def print_color(*args, **kwargs):
        pass
elif args.no_color:
    def print_color(*args, **kwargs):
        for arg in args:
            print(arg)
else:
    def print_color(*args, **kwargs):
        # Get color or default to normal.
        color = bcolors.get(kwargs["color"], bcolors["normal"])
        for arg in args:
            print(color + arg + bcolors["normal"])

# FYI, these functions depend on print_color
if args.verbose and not args.quiet:
    def print_verbose(*args, **kwargs):
        for arg in args:
            print_color(arg, color="normal")
else:
    def print_verbose(*args, **kwargs):
        pass

if args.debug:
    def print_debug(*args, **kwargs):
        for arg in args:
            print_color(arg, color="cyan")
else:
    def print_debug(*args, **kwargs):
        pass

if args.warn:
    def print_warn(*args, **kwargs):
        for arg in args:
            print_color(arg, color="yellow")
else:
    def print_warn(*args, **kwargs):
        pass

if args.error:
    def print_error(*args, **kwargs):
        for arg in args:
            print_color(arg, color="red")
else:
    def print_error(*args, **kwargs):
        pass
