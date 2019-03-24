import os
import shutil


def init(cmd):
    """Add new commands to commands dictionary"""
    cmd.update({'cp': copyFile,
                'mv': moveFile,
                'rm': removeFile})


def copyFile(args, stdin, stdout, stderr):
    """Copy file / directory"""
    if len(args) > 2:
        try:
            if os.path.isdir(args[1]):
                shutil.copytree(args[1], args[2])
            else:
                shutil.copy2(args[1], args[2])
        except Exception as e:
            stderr.write(e.__str__() + '\n')
    else:
        stderr.write('No file / directory name specified\n')


def moveFile(args, stdin, stdout, stderr):
    """Move file / directory"""
    if len(args) > 2:
        try:
            shutil.move(args[1], args[2])
        except Exception as e:
            stderr.write(e.__str__() + '\n')
    else:
        stderr.write('No file / directory name specified\n')


def removeFile(args, stdin, stdout, stderr):
    """Remove file / directory"""
    if len(args) > 1:
        try:
            os.remove(args[1])
        except Exception as e:
            stderr.write(e.__str__() + '\n')
    else:
        stderr.write('No file name specified\n')
