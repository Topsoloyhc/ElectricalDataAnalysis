import time
import os
import sys


class Logger(object):

    def __init__(self, stream=sys.stdout):
        output_dir = "../output/log"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        log_name = '{}.log'.format(time.strftime('%Y-%m-%d-%H-%M'))
        filename = os.path.join(output_dir, log_name)

        self.terminal = stream
        self.log = open(filename, 'a+')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass


class Out2txt(object):

    def __init__(self, stream=sys.stdout, file_type=""):
        output_dir = "../output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        file_name = '{}.txt'.format(time.strftime('%Y-%m-%d-%H-%M'))
        filename = os.path.join(output_dir, file_type+"_"+file_name)

        self.terminal = stream
        self.file = open(filename, 'a+')

    def write(self, message):
        self.terminal.write(message)
        self.file.write(message)

    def flush(self):
        pass
