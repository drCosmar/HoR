import pathlib, time, datetime, os, requests, re, threading, sys, itertools
from dotenv import load_dotenv
load_dotenv()

class pths:
    root = pathlib.Path(__file__).parent.parent.resolve()
    src = root / "src"
    data = root / "data"
    congressData = data / "congress"

class Timer:
    def __init__(self, name):
        self.name = name
        self.start = time.time()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.duration = self.end - self.start
        print(f"{self.name} took {self.duration:.2f} seconds")
# a tool that makes manipulating date values easier by turning them into a datetime object.
def timeStamp(day:int=None, month:int=None, year:int=None):
    date = datetime.datetime.now().date()
    if day != None:
        date = date.replace(day=day)
    if month != None:
        date = date.replace(month=month)
    if year != None:
        date = date.replace(year=year)
    return date

def stringToDatetime(date:str) -> datetime.datetime:
    date = re.sub(r"[^\d]", "", date)
    date = datetime.datetime.strptime(date, "%Y%m%d")
    return date

def loadingIndicator(func):
    def spinner():  # Function to display a simple spinner animation
        spinner_symbols = itertools.cycle(['-', '\\', '|', '/'])
        while not done:
            sys.stdout.write(next(spinner_symbols))  # Write the next spinner symbol
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write('\b')  # Use backspace to remove the spinner symbol

    def wrapper(*args, **kwargs):
        global done
        done = False
        spinner_thread = threading.Thread(target=spinner)  # Create a thread for the spinner
        spinner_thread.start()  # Start the spinner thread
        result = func(*args, **kwargs)  # Run the decorated function
        done = True  # Indicate that the task is done
        spinner_thread.join()  # Wait for the spinner thread to finish
        return result

    return wrapper

PATHS = pths()
LMURL = os.environ["LMSTUDIOURL"]
CONAPI = os.environ["CONGRESSAPI"]
DEFAULT = not os.getenv("DEFAULTS", "true") == "true"