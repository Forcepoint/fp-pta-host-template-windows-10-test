"""
 Author: Jeremy Cornett
   Date: 10/23/2017
Purpose: Populate a file with sensitive data contained in environment variables so said secrets aren't
         committed to source code control. http://jinja.pocoo.org/docs/2.9/api/
"""

import os
from jinja2 import Environment, FileSystemLoader


def main():
    """The main function.
    :return: None
    """
    env = Environment(loader=FileSystemLoader('templates'))
    path_floppy = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "floppy"))

    template = env.get_template("Autounattend.xml")
    with open(os.path.join(path_floppy, "Autounattend.xml"), "w") as file_template:
        file_template.write(template.render(user_password=os.environ["PACKER_WIN_PASSWORD"]))


if __name__ == "__main__":
    main()
