"""
Outputs a file parsed_gunicorn.conf.py, that contains entries for all available
config settings according to the Gunicorn documentation:

https://docs.gunicorn.org/en/stable/settings.html

This file can then be adapted manually.
"""
import sys
from bs4 import BeautifulSoup

with open(sys.argv[1]) as f:
    soup = BeautifulSoup(f.read(), features="html.parser")

settings = soup.find("div", id= "settings")
sections = settings.findAll("div", attrs = {"class": "section"}, recursive = False)
subsections = [s.findAll("div", attrs = {"class": "section"} ,recursive = False) for s in sections]


def find_default(subsection):
    try:
        default_subsection,*_ = [p for p in subsection.findAll("p") if "Default" in p.text]
        return default_subsection.find("code").text
    except (ValueError, AttributeError):
        try:
            return subsection.find("pre").text
        except (ValueError, AttributeError):
            return "\"\""

def hook_fn_name(name):
    return f"""
def {name}(server):
    pass
    """

titles = [div.find("h2").text for div in sections]
subtitles = {title: {div.find("code").text: find_default(div) for div in subsection} for title,subsection in zip(titles,subsections)}


with open("parsed_gunicorn.conf.py","w") as f:
    f.writelines([
        "from environs import Env\n\n",
        "env = Env()\n",
        "env.read_env()\n",
        "\n",
        ])
    for title,subtitles in subtitles.items():
        f.writelines([f"# -- {title[:-1]}\n\n"])
        if "hooks" in title.lower():
            f.writelines([default+"\n" for _,default in subtitles.items()])
        else:
            f.writelines([subtitle + f" = env.str(\"GUNICORN_{subtitle.upper()}\", {default})\n" for subtitle, default in subtitles.items()])
        f.writelines("\n")
