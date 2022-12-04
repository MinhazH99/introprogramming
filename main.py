import pyfiglet
from home import home

def main():
    print(pyfiglet.figlet_format("Emergency Planner",font = "big"))
    home()


if __name__ == '__main__':
    main()