import base64
import os
import platform
from asyncio.windows_events import NULL
from datetime import date, datetime, timedelta

from cryptography.fernet import Fernet
from rich import print
from rich.console import Console
from rich.prompt import Confirm, Prompt
from tinydb import Query, TinyDB

# JSON Storage for capsules
database = TinyDB("db.json")
message = Query()


# Key for encryption and decryption
def checkKey():
    keyFile = "key.txt"
    if os.path.exists(keyFile) and os.path.getsize(keyFile) == 0:
        # Generate key
        key = Fernet.generate_key()
        with open(keyFile, "wb") as keyFile:
            keyFile.write(key)


def checkCapsule():
    # Check current time
    now_time = datetime.now().timestamp()

    # Accessing JSON Data
    parse = database.all()

    # Parse the unlocking time
    unlock_time = NULL

    # Check the dictionary for possible unlockable capsules using a loop
    for i, unlock in enumerate(parse, start=0):
        if now_time >= unlock_time:
            unlock_time = parse[i]["time_limit"]
            print("[green][bold]You can now unlock your Capsule No." + f" {i}")
        if now_time < unlock_time:
            print(
                "[red][bold]Your capsule No.[/][/]"
                + f" {i} [red][bold]is not unlockable yet.[/][/]"
            )


def interactive(console: Console):
    while True:
        console.clear()

        checkKey()

        # Main Menu
        action = Prompt.ask(
            "[bold][cyan]Time Capsule[/][/] \n[bold][white]Select an option:[/][/] \n\n[green]1.[/] [yellow]Create capsule[/]\n[green]2.[/] [yellow]Check for unlockable capsules[/]",
            choices=["1", "2", "exit"],
        )

        if action == "exit":
            break
        elif action == "1":
            print("\n[white][bold]Dear Future Me,[/]")

            # Input & Encryption'
            keyFile = "key.txt"

            # Parse key from key.txt
            with open(keyFile, "rb") as keyFile:
                readKey = keyFile.read()
                f = Fernet(readKey)

            message = f.encrypt(input().encode())
            print("[white][bold]Set time limit:[/][/][gray](i.e: 2 (Day/s))[/]")
            time_limit = datetime.now() + timedelta(days=int(input()))
            if isinstance(time_limit, datetime):
                database.insert(
                    {
                        "message": str(message),
                        "time_limit": time_limit.timestamp(),
                        "current_time": str(datetime.now()),
                    }
                )
                print("[red][bold]Your message has been capsulized!")

            else:
                print("[red]Invalid time format. Please enter amount of days.[/]")
        elif action == "2":
            checkCapsule()


# Define the interactive function.
def main() -> None:
    console = Console()
    interactive(console)


# Run the main function if this script is executed.
if __name__ == "__main__":
    main()
