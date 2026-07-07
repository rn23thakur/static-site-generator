from pathlib import Path
from transfer_util import transfer_contents
from page_util import generate_pages_recursive

def main():
   transfer_contents() 
   generate_pages_recursive(
      dir_path_content=Path.home() / "workspace/boot-dev/static-site-generator/content",
      template_path=Path.home() / "workspace/boot-dev/static-site-generator/template.html",
      dest_dir_path=Path.home() / "workspace/boot-dev/static-site-generator/public"
   )


if __name__ == "__main__":
    main()