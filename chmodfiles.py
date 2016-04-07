#!/bin/python
import os 
import stat
import argparse

class MyChmod(object):
    def __init__(self, args):
        for key in args:
            setattr(self, key, args.get(key))

    def get_filepaths(self, version):
        """
        This function will generate the file names in a directory 
        tree by walking the tree either top-down or bottom-up. For each 
        directory in the tree rooted at directory top (including top itself), 
        it yields a 3-tuple (dirpath, dirnames, filenames).
        """
        file_paths_mode = {}  # List which will store all of the full filepaths.
        
        # Walk the tree.
        full_file_paths = self.path + version + "/"
        split = version + '/'
        for root, directories, files in os.walk(full_file_paths,topdown=True, followlinks=False):
            for dir in directories:
                dirpath = os.path.join(root, dir)
                rdirpath = dirpath.split(split,1)[1]
                file_paths_mode[rdirpath] = os.lstat(dirpath).st_mode
            for filename in files:
                # Join the two strings in order to form the full filepath.
                filepath = os.path.join(root, filename) 
                rfilepath = filepath.split(split,1)[1]
                file_paths_mode[rfilepath] = os.lstat(filepath).st_mode
        return file_paths_mode
    
    def change_mod(self, root, filename, split, old_file_paths_mode):
        filepath = os.path.join(root, filename)
        rfilepath = filepath.split(split,1)[1]
        statmode = os.lstat(filepath).st_mode
        # file relative path is the key in the file mode list
        if rfilepath in old_file_paths_mode:
            if old_file_paths_mode[rfilepath] != statmode:
                if self.verbose:
                    print "%d --> %d  %s" % (statmode, old_file_paths_mode[rfilepath], rfilepath)
                os.chmod(filepath, old_file_paths_mode[rfilepath])
        
    def change_modes(self):
        old = self.old
        new = self.new
        old_file_paths_mode = self.get_filepaths(old);
        
        # Walk the tree.
        full_file_paths = self.path + new + "/"
        split = new + '/'
        for root, directories, files in os.walk(full_file_paths, topdown=True, followlinks=False):
            for dir in directories:
                self.change_mod(root, dir, split, old_file_paths_mode)
            for filename in files:
                self.change_mod(root, filename, split, old_file_paths_mode)
            
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='change file mode')
    parser.add_argument('-p', '--path', required=True, help='Directory path: /shadow/')
    parser.add_argument('-o', '--old', required=True, help='old version') 
    parser.add_argument('-n', '--new', required=True, help='new version')
    parser.add_argument('-v', '--verbose', action='store_true', \
                        help='print out the files needed to be updated')
    
    args=parser.parse_args()
    opts=vars(args)
    
    mychmod = MyChmod(opts) 
    mychmod.change_modes()