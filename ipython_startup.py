import math
import pathlib
import subprocess

from math import pi

from explor import explore as ex
from explor import explore_signature as exs
from explor import explore_object as exo

from astropy import units
from astropy import constants

import IPython
IPython.core.oinspect.Inspector.pinfo = lambda self, obj, *args, **kwargs: ex(obj)

import pyperclip

pycopy = pyperclip.copy
pypaste = pyperclip.paste

ipy = get_ipython()

#ipy.magic("%alias_magic %h %history")
ipy.run_line_magic("alias_magic", "%h %history")
#ipy.magic("%autocall 1") # kann auch /ex benutzen
ipy.run_line_magic("autocall", "1")

print("copypaste: pycopy() / pypaste()")
# print("Included: wex, units, constants, pIncluded: wex, units, constants, pii")

p = print
def wex(path=None):
    """open the Windows EXplorer"""
    if path is None:
        subprocess.Popen(["explorer.exe", "."])
    elif isinstance(path, pathlib.Path):
        subprocess.Popen(["explorer.exe", str(path.resolve())])
    else:
        subprocess.Popen(["explorer.exe", path])


underscored = lambda val: "{:_}".format(val)
console_formatter = ipy.display_formatter.formatters['text/plain']
console_formatter.for_type(float, lambda val, p, c: p.text(underscored(val)))
console_formatter.for_type(int, lambda val, p, c: p.text(underscored(val)))
console_formatter.for_type(units.Quantity, lambda val, p, c: p.text(show_si(val)))

def show_si(val):
    if 0 * val == 0 * val.si:
        return f"{underscored(val)}   ---   ({underscored(val.si)})"



units.Quantity.inv = property(lambda x: 1/x)
units.UnitBase.inv = property(lambda x: (1/x).unit)
