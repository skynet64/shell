import sys
import os
import subprocess
import shlex
import tempfile
import tty
import termios
import dir
import file
import env


class IO:
    """Contains file descriptors for stdin, stdout, stderr"""
    stdin = sys.stdin
    stdout = sys.stdout
    stderr = sys.stderr


class Pipe:
    """Contains execution context for command line"""
    def __init__(self, _args):
        self.pipe = []
        self.args = _args
        self.closeStdin = False
        self.closeStdout = False
        self.closeStderr = False

    def open(self):
        """Open files for input / output redirection"""
        self.pipe.append(IO())
        for i in range(0, len(self.args) - 1):
            self.pipe.append(IO())
            self.pipe[i].stdout = tempfile.TemporaryFile(mode='w+b')
            self.pipe[i + 1].stdin = self.pipe[i].stdout

        i = 0
        arg = self.args[len(self.args) - 1]
        while i < len(arg):
            if arg[i] == '<':
                if i == len(arg) - 1:
                    raise ValueError('No file specified for input')

                if self.closeStdin:
                    raise ValueError('Too many files specified for input')

                try:
                    self.pipe[0].stdin = open(arg[i + 1], 'r')
                except Exception as e:
                    raise e

                self.closeStdin = True
                del arg[i:i + 2]
            elif arg[i] == '1>' or arg[i] == '>':
                if i == len(arg) - 1:
                    raise ValueError('No file specified for output')

                if self.closeStdout:
                    raise ValueError('Too many files specified for output')

                try:
                    self.pipe[len(self.pipe) - 1].stdout =\
                        open(arg[i + 1], 'w')
                except Exception as e:
                    raise e

                self.closeStdout = True
                del arg[i:i + 2]
            elif arg[i] == '1>>' or arg[i] == '>>':
                if i == len(arg) - 1:
                    raise ValueError('No file specified for output')

                if self.closeStdout:
                    raise ValueError('Too many files specified for output')

                try:
                    self.pipe[len(self.pipe) - 1].stdout =\
                        open(arg[i + 1], 'a')
                except Exception as e:
                    raise e

                self.closeStdout = True
                del arg[i:i + 2]
            elif arg[i] == '2>':
                if i == len(arg) - 1:
                    raise ValueError('No file specified for error output')

                if self.closeStderr:
                    raise ValueError(
                        'Too many files specified for error output')

                try:
                    file_e1 = open(arg[i + 1], 'w')
                except Exception as e:
                    raise e

                for e_pipe in self.pipe:
                    e_pipe.stderr = file_e1

                self.closeStderr = True
                del arg[i:i + 2]
            elif arg[i] == '2>>':
                if i == len(arg) - 1:
                    raise ValueError('No file specified for error output')

                if self.closeStderr:
                    raise ValueError(
                        'Too many files specified for error output')

                try:
                    file_e2 = open(arg[i + 1], 'a')
                except Exception as e:
                    raise e

                for e_pipe in self.pipe:
                    e_pipe.stderr = file_e2

                self.closeStderr = True
                del arg[i:i + 2]
            else:
                i += 1

    def close(self):
        """Close files that created for input / output redirection"""
        for e_pipe in self.pipe[0:len(self.pipe) - 1]:
            e_pipe.stdout.close()

        if self.closeStderr:
            self.pipe[0].stderr.close()

        if self.closeStdin:
            self.pipe[0].stdin.close()

        if self.closeStdout:
            self.pipe[len(self.pipe) - 1].stdout.close()

    def execute(self, cmd):
        """Execute current context"""
        for i in range(0, len(self.args)):
            if i > 0:
                self.pipe[i].stdin.seek(0)

            if self.args[i][0] in cmd.keys():
                cmd[self.args[i][0]](
                    args=self.args[i],
                    stdin=self.pipe[i].stdin,
                    stdout=self.pipe[i].stdout,
                    stderr=self.pipe[i].stderr)
            else:
                thread = subprocess.Popen(
                    args=self.args[i],
                    stdin=self.pipe[i].stdin,
                    stdout=self.pipe[i].stdout,
                    stderr=self.pipe[i].stderr)
                thread.wait()


def prompt():
    """Return invitation"""
    return '[' + os.getcwd() + ']$ '


def shellExit(args, stdin, stdout, stderr):
    """Exit from shell"""
    exit(int(args[1]) if len(args) > 1 else 0)


def cmdInput(inv):
    """Read input"""
    index = len(inv)
    minIndex = index
    input = inv
    while True:
        sys.stdout.write(u"\u001b[1000D")
        sys.stdout.write(u"\u001b[0K")
        sys.stdout.write(input)
        sys.stdout.write(u"\u001b[1000D")
        if index >= minIndex:
            sys.stdout.write(u"\u001b[" + str(index) + "C")
        sys.stdout.flush()

        char = ord(sys.stdin.read(1))

        if char == 3:  # Ctrl-C
            shellExit(['', '-1'], None, None, None)
        elif 32 <= char <= 126:  # Normal symbols
            input = input[:index] + chr(char) + input[index:]
            index += 1
        elif char in {10, 13}:  # New line
            sys.stdout.write(u'\n\u001b[1000D')
            return input
        elif char == 27:
            next1, next2 = ord(sys.stdin.read(1)), ord(sys.stdin.read(1))
            if next1 == 91:
                if next2 == 68:  # Left
                    index = max(minIndex, index - 1)
                elif next2 == 67:  # Right
                    index = min(len(input), index + 1)
        elif char == 127:  # Backspace
            if index > minIndex:
                input = input[:index - 1] + input[index:]
                index -= 1


if __name__ == '__main__':
    cmd = {'exit': shellExit}
    dir.init(cmd=cmd)
    file.init(cmd=cmd)
    env.init(cmd=cmd)

    while True:
        try:
            fd = sys.stdin.fileno()
            oldSettings = termios.tcgetattr(fd)
            tty.setraw(sys.stdin)
            args = [shlex.split(arg) for arg in cmdInput(prompt()).split('|')]
            termios.tcsetattr(fd, termios.TCSADRAIN, oldSettings)
            del args[0][0]
        except Exception as e:
            sys.stderr.write(e.__str__() + '\n')
        else:
            if args[0] or len(args) > 1:
                pipe = Pipe(args)
                try:
                    pipe.open()
                    pipe.execute(cmd=cmd)
                except IndexError:
                    sys.stderr.write('Invalid input\n')
                except Exception as e:
                    sys.stderr.write(e.__str__() + '\n')
                pipe.close()
