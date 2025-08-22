from textnode import *
from htmlnode import *
from split_delimiter import *
from markdown_blocks import *
import os
import shutil

def remove_filetree(target_dir):
    if os.path.exists(target_dir):
        shutil.rmtree(f"{target_dir}/")

def copy_directory(dir, target_dir, is_initial_call=True):
    if is_initial_call:
        remove_filetree(target_dir)


    #check for dir and target dir existence
    if not os.path.exists(dir):
        raise Exception("directory does not exist")

    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    # list the contents of the directory
    directory_list = os.listdir(dir)
    #target_dir_list = os.listdir(target_dir)
    
    
    #recursive copying
    for item in directory_list:
        joined_path = os.path.join(dir, item)
        if os.path.isdir(joined_path):
            new_target = os.path.join(target_dir, item)
            copy_directory(joined_path, new_target, is_initial_call=False)
        if os.path.isfile(joined_path):
            shutil.copy(joined_path, target_dir)
        #print(f"target_list = {target_dir_list}, dir_list = {directory_list}")
    



    

def main():
    copy_directory("static/", "public/")


if __name__ == "__main__":
    main()

    