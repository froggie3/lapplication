import atexit
import readline
import sys


class Input:
    RESET = "\001" "\033[0m" "\002"
    CYAN = "\001" "\033[36m" "\002"

    @classmethod
    def input(cls, default_input=input, *args, **kwargs):
        prompt = ">>> "
        return default_input(f"{cls.CYAN}{prompt}{cls.RESET}", *args, **kwargs)


def app():
    histfile = "/tmp/.history"

    try:
        readline.read_history_file(histfile)
        readline.set_history_length(1000)
    except FileNotFoundError:
        pass

    atexit.register(readline.write_history_file, histfile)

    _input = Input.input
    import timer

    tmr = timer.Timer()
    tmr.start()
    while True:
        try:
            _input()
        except KeyboardInterrupt:
            lap = tmr.lap()
            sys.stdout.write("\n%s\n" % (lap,))
        except EOFError:
            sys.stdout.write("\n")
            break


if __name__ == "__main__":
    app()
