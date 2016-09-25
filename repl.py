import cmd
import readline
import traceback
import visp

class VispShell(cmd.Cmd):
    intro = 'Welcome to the Visp shell. Type help or ? to list commands.\n'
    prompt = '> '
    env = None

    def do_repr(self, line):
        self.default(line, to_string=repr)

    def default(self, line, to_string=str):
        try:
            print(to_string(visp.evaluate(visp.read(line), self.env)))
        except Exception as exc:
            print(traceback.format_exc())

    def do_EOF(self, line):
        print()
        return True

if __name__ == '__main__':
    vs = VispShell()
    vs.env = visp.Env()
    vs.cmdloop()
