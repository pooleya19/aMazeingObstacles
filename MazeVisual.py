from Display import Display

display = Display()

def main():
    display.start()

    while True:
        display.update()

if __name__ == '__main__':
    main()