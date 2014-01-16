from PyQt5.QtCore import QObject, pyqtSignal
import inspect, sys

cmd_dict = {}

def register_all():
    def is_cmd(obj):
        return (inspect.isclass(obj) and obj.__module__ == __name__ and
                obj.__name__.endswith('Cmd'))

    for (name, cls) in inspect.getmembers(sys.modules[__name__], is_cmd):
        cls.bind()

class CommandParser(QObject):
    def parse(self, text):
        parts = text.strip().split()
        cmd = parts[0]
        argv = parts[1:]
        obj = cmd_dict[cmd]
        try:
            obj.check(argv)
        except TypeError:
            # TODO
            raise
        obj.run(argv)

class Command(QObject):
    nargs = 0
    name = ''
    signal = None

    @classmethod
    def bind(cls):
        if cls.name:
            cmd_dict[cls.name] = cls()

    def check(self, argv):
        if ((isinstance(self.nargs, int) and len(argv) != self.nargs) or
                      (self.nargs == '?' and len(argv) > 1) or
                      (self.nargs == '+' and len(argv) < 1)):
            raise TypeError("Invalid argument count!")

    def run(self, argv):
        if not self.signal:
            raise NotImplementedError
        self.signal.emit()

class OpenCmd(Command):
    nargs = 1
    name = 'open'
    signal = pyqtSignal(str)

    def run(self, argv):
        self.signal.emit(argv[0])

class TabOpenCmd(Command):
    nargs = 1
    name = 'tabopen'
    signal = pyqtSignal(str)

    def run(self, argv):
        self.signal.emit(argv[0])

class QuitCmd(Command):
    nargs = 0
    name = 'quit'
    signal = pyqtSignal()

register_all()
