import pyfiglet
from home import home
import os

# os.system(pip install -r requirement.txt)

def main():
    print(pyfiglet.figlet_format("Welcome to EMS",font = "big"))
    home()


if __name__ == '__main__':
    main()
