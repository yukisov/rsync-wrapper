rsync-util
==========

rsync wrapper program.

##How to Use

1. Clone this repo specifying a directory name.
    ```
    $ git clone https://github.com/yukisov/rsync-util.git specific-topic-dir
    ```

2. Set up the rsync-util
    ```
    $ rm README.md
    # configure some setting values
    $ vi .rsync/rsync.py
    # configure excluded paths
    $ vi .rsync/rsync_exclude.txt
    $ chmod u+x .rsync/rsync.py
    ```

3. Create some files related your specific topic for this directory. 
    ```
    $ cd specific-topic-dir
    $ vi some_files
    ```
You'll want to backup this directory onto other machine.

4. Confirm the rsync command to be excluded
    ```
    $ ./.rsync/rsync.py -c
    ```

5. Execute rsync with dry-run
    ```
    $ ./.rsync/rsync.py
    ```

6. Execute rsync in effect
    ```
    $ ./.rsync/rsync.py -a
    ```
