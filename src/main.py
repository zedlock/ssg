import shared
import os
import shutil
import sys

def main():
    global BASEPATH
    if len(sys.argv) < 2:
        BASEPATH = '/'
    else:
        BASEPATH = sys.argv[1]
    cwd = os.getcwd()
    if os.path.exists(f"{cwd}/docs"):
        shutil.rmtree(f"{cwd}/docs")

    copy_static(cwd)

    generate_page_recursive(
        f"{cwd}/content",
        f"{cwd}/docs",
        f"{cwd}/template.html",
    )

def copy_static(cwd):
    copy(f"{cwd}/static", f"{cwd}/docs")

def copy(src, dst):
    if os.path.isfile(src):
        shutil.copy(
            src,
            dst
        )
    else:
        os.mkdir(dst)
        for file in os.listdir(src):
            copy(f"{src}/{file}", f"{dst}/{file}")

def generate_page_recursive(src, dst, template):
    if os.path.isfile(src):
        file_parts = dst.split(".")
        file_parts[-1] = "html"
        dst = ".".join(file_parts)
        generate_page(src, dst, template)
    else:
        if not os.path.exists(dst):
            os.mkdir(dst)
        for file in os.listdir(src):
            generate_page_recursive(f"{src}/{file}", f"{dst}/{file}", template)

def generate_page(src, dst, template):
    print(f"Generating page from \"{src}\" to \"{dst}\" using \"{template}\"")
    with open(src) as f:
        md_file = f.read()
    with open(template) as f:
        template = f.read()

    title = shared.extract_title(md_file)
    content = shared.markdown_to_html_node(md_file).to_html()

    page = template.replace("{{ Title }}", title).replace("{{ Content }}", content)
    page = page.replace("href=\"", title).replace(f"href=\"{BASEPATH}", content)
    page = page.replace("src=\"", title).replace(f"src=\"{BASEPATH}", content)

    with open(dst, "x") as f:
        f.write(page)




main()
