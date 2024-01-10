import pathlib, time, datetime, os, re,\
    threading, sys, itertools, requests
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
    global doneEvent
    def spinner(doneEvent):  # Function to display a simple spinner animation
        spinnerSymbols = itertools.cycle(['-', '\\', '|', '/'])
        loadingMsg = "Loading "
        while not doneEvent.is_set():
            sys.stdout.write(loadingMsg + next(spinnerSymbols))  # Write the next spinner symbol
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write('\b' * (len(loadingMsg) + 1))  # Use backspace to remove the spinner symbol

    def wrapper(*args, **kwargs):
        doneEvent = threading.Event()  # Use threading.Event to control the spinner
        spinnerThread = threading.Thread(target=spinner, args=(doneEvent,))  # Pass the Event to the spinner thread
        spinnerThread.start()  # Start the spinner thread

        # Run the decorated function and pass the Event to it
        result = func(*args, **kwargs, doneEvent=doneEvent)
        
        doneEvent.set()  # Signal that the task is done
        spinnerThread.join()  # Wait for the spinner thread to finish
        return result
    return wrapper

PATHS = pths()
LMURL = os.environ["LMSTUDIOURL"]
CONAPI = os.environ["CONGRESSAPI"]
DEFAULT = not os.getenv("DEFAULTS", "true") == "true"