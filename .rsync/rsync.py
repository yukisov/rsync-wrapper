#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
rsync wrapper


- Python 3 supported

@author Yuki <yukisov@gmail.com>
@created 2014-06-18

"""

import sys
import os

__all__ = (
        'MyRsyncException',
        'FileNotFoundError',
        'RsyncObj',
        )

__revision__ = '1.0'

class MyRsyncException(Exception):
    pass

class FileNotFoundError(MyRsyncException):
    pass

class RsyncObj(object):
    u"""Rsync Object"""

    # target on server
    _SERVER_TARGET_REAL = 'username@host:path/'

    # exclude file path
    _EXCLUDE_FILE_PATH = '.rsync/rsync_exclude.txt'

    # mode: 1. Normal execution
    # mode: 2. Confirm the command to be excuted
    _mode = 1
    MODE_NORMAL = 1
    MODE_VERIFY_COMMAND = 2

    _local_target = ''
    _server_target = ''
    _exclude_file_path = ''

    def __init__(self, mode=None, dry_run=True):
        u"""constructor."""

        if mode is None: mode = RsyncObj.MODE_NORMAL
        self._mode = mode

        # get the values that will be arguments for rsync command
        self._local_target, self._server_target, self._exclude_file_path = self._getFileVals()

        # create a command string
        commandCreator = CommandCreator(
            self._local_target,
            self._server_target,
            self._exclude_file_path,
        )
        self._command = commandCreator.create(dry_run)

    def execute(self):
        u"""execute rsync"""
        # check the existence of an exclude file
        if self._mode == RsyncObj.MODE_NORMAL:
            if not os.path.exists(self._exclude_file_path):
                raise FileNotFoundError("exclude file is NOT found.(" + self._exclude_file_path + ")")

        # Normal execution
        if self._mode == RsyncObj.MODE_NORMAL:
            print(self._command)
            os.system(self._command)
        # Confirm the command to be excuted
        elif self._mode == RsyncObj.MODE_VERIFY_COMMAND:
            print(self._command)

    def _getServerTarget(self, cur_path):
        u"""return the $SERVER_TARGET string"""
        return self._SERVER_TARGET_REAL

    def _getFileVals(self):
        u"""get the info related to the current path"""
        # get the current path
        cur_path = os.getcwd()
        cur_dir_name = os.path.basename(cur_path) # the directory name
        #print(cur_path)
        #print(cur_dir_name)

        # LOCAL_TARGET
        local_target = ''.join([cur_path, '/'])

        # SERVER_TARGET
        server_target = self._getServerTarget(cur_path)

        # EXCLUDE_FILE_PATH
        exclude_file_path = ''.join([cur_path, '/', self._EXCLUDE_FILE_PATH])

        return (local_target, server_target, exclude_file_path)

class CommandCreator(object):
    u"""create an command strin

    rsync $RSYNC_OPT $LOCAL_TARGET $SERVER_TARGET
    """

    def __init__(self, local_target, server_target, exclude_file_path):
        u"""constructor."""
        self._local_target = local_target
        self._server_target = server_target
        self._exclude_file_path = exclude_file_path

    def create(self, dry_run=True):
        u"""main method"""
        self._dry_run = dry_run
        option = self._createOption()
        local_target = self._createLocalTarget()
        server_target = self._createServerTarget()

        return "rsync %s %s %s" % (option, local_target, server_target)

    def _createOption(self):
        u"""create the option string and return it
        - NOT need a space character as the first character of an option variable
        - Please replace '-v' with '-vv' or '-vvv' if you wanna know details
        """
        option = ' --archive -v --checksum --rsh=ssh' \
                 ' --exclude-from=' + self._exclude_file_path
        if self._dry_run: option += ' --dry-run'
        return option

    def _createLocalTarget(self):
        u"""create LOCAL_TARGET string and return it"""
        return self._local_target

    def _createServerTarget(self):
        u"""create SERVER_TARGET string and return it"""
        return self._server_target

#---------------------
# Main
#---------------------
def main():
    # process for arguments
    # rsync execute with dry-run if there's not '-a' option
    dry_run = True
    mode = RsyncObj.MODE_NORMAL
    if len(sys.argv) == 2:
        if sys.argv[1] == '-a':
            dry_run = False
        elif sys.argv[1] == '-c':
            mode = RsyncObj.MODE_VERIFY_COMMAND
        elif sys.argv[1] == '-h':
            print(" No params:\n\texecute rsync with dry-run\n" \
                    + " -a:\n\texecute rsync in effect\n" \
                    + " -c:\n\tshow the command string to be executed\n" \
                    + " -h:\n\tshow this")
            return

    try:
        rsyncObj = RsyncObj(mode, dry_run)
        rsyncObj.execute()
    except FileNotFoundError as strerror:
        print("File Not Found Error: %s" % strerror)

if __name__ == '__main__':
    main()
