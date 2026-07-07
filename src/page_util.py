import os
import shutil
from pathlib import Path
from markdown import markdown_to_html_node
from title_util import extract_title

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as markdown_file:
        markdown_text = markdown_file.read()

    with open(template_path, "r") as template_file:
        template_text = template_file.read()
    
    parent_node_object = markdown_to_html_node(markdown=markdown_text)
    html_text = parent_node_object.to_html()

    title = extract_title(markdown_text)

    final_html = template_text.replace("{{ Title }}", title).replace("{{ Content }}", html_text).replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')

    folder_path = os.path.dirname(dest_path)

    if folder_path:
        os.makedirs(folder_path, exist_ok=True)
    # print(f"Final HTML content: {final_html}") 
    # Write to the file
    with open(dest_path, "w", encoding="utf-8") as file:
        print(f"writing html content here: {dest_path}")
        file.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    # Ensure variables are Path objects so / operator works
    dir_path_content = Path(dir_path_content)
    dest_dir_path = Path(dest_dir_path)
    
    for item in dir_path_content.iterdir():
        # Append the current item's name to the destination directory
        dest_item = dest_dir_path / item.name
        
        if item.is_dir():
            # Create the matching directory in destination if it doesn't exist
            dest_item.mkdir(parents=True, exist_ok=True)
            
            # Recurse deeper into the sub-directory
            generate_pages_recursive(item, template_path, dest_item, basepath)
            
        else:
            # Check if the file is a markdown file
            if item.name.endswith('.md'):
                # Call your custom generator function
                dest_html_path = dest_item.with_suffix('.html')
                
                # Calls your generation function with the new HTML path
                generate_page(item, template_path, dest_html_path, basepath)