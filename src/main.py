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
    



def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    if not os.path.exists(dest_path):
        with open(dest_path, "x") as f:
            pass
    #read and store the from path and template
    from_path_file = open(from_path, "r")
    fromfile = from_path_file.read()
    template_path_file = open(template_path, "r")
    template_file = template_path_file.read()
    dest_path_file = open(dest_path, "r")
    #dest_file = dest_path_file.read()

    md_html_node = markdown_to_html_node(fromfile)
    md_html= md_html_node.to_html()
    print(f"\n\n\n\n**HTML** : \n\n{md_html}")
    page_title = extract_title(fromfile)
    new_template_file = template_file.replace(
        "{{ Title }}",
        page_title).replace(
            "{{ Content }}",
            md_html
            )
    
    with open(dest_path, "w") as f:
        f.write(new_template_file)
        #print(f"wrote file {dest_file} at {dest_path}")

def list_contents(dir_path_content):

    contents_list = []
    #os.listdir(dir_path_content)
    for item in os.listdir(dir_path_content):
        full_path = os.path.join(dir_path_content,item)
        contents_list.append(full_path)
        if os.path.isdir(full_path):
            contents_list.extend(list_contents(full_path))
    

    return contents_list

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    content_list = list_contents(dir_path_content)

    for item in content_list:
        if item.startswith(dir_path_content):
            revised_item_name = item[len(dir_path_content):]
            if revised_item_name.startswith("/"):
                revised_item_name = revised_item_name[1:]
        if revised_item_name.endswith('.md'):
            no_suff = revised_item_name.removesuffix('.md') + ".html"
            full_dest_path = os.path.join(dest_dir_path, no_suff)
            target_dir = os.path.dirname(full_dest_path)
            if os.path.exists(target_dir):
                generate_page(item, template_path, os.path.join(dest_dir_path,no_suff))
            else:
                os.makedirs(target_dir)
                generate_page(item, template_path, os.path.join(dest_dir_path, no_suff))



    


    

def main():
    copy_directory("static/", "public/")
    generate_pages_recursive("./content/", "./template.html", "./public/")


if __name__ == "__main__":
    main()

    