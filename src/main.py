from pathlib import Path
import sys
from transfer_util import transfer_contents
from page_util import generate_pages_recursive

def main():
   first_arg = None
   if len(sys.argv) > 1:
      first_arg = sys.argv[1]
   basepath = first_arg or "/"
   print(basepath)
   transfer_contents(
      SOURCE = Path.home() / "workspace/boot-dev/static-site-generator/static",
      DESTINATION = Path.home() / "workspace/boot-dev/static-site-generator/docs"
   ) 
   generate_pages_recursive(
      dir_path_content=Path.home() / "workspace/boot-dev/static-site-generator/content",
      template_path=Path.home() / "workspace/boot-dev/static-site-generator/template.html",
      dest_dir_path=Path.home() / "workspace/boot-dev/static-site-generator/docs",
      basepath=basepath
   )


if __name__ == "__main__":
    main()