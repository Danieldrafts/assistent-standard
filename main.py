from assistent import Assistent

if __name__ == '__main__':
    assistent = Assistent()
    assistent.awake()
    try:
        assistent.start()
    except KeyboardInterrupt:  # allow Ctrl + C to shut down the program
        exit("Bye")
