from flask import (Blueprint, render_template)

bp = Blueprint('printers', __name__, url_prefix='/printers')

@bp.route('/')
def print():
    import win32print
    default_printer = win32print.GetDefaultPrinter()
    printers_list = win32print.EnumPrinters(2) # Tuple of tuples with the structure: (flags, description, name, comment)
    # win32print.SetDefaultPrinter(printers_list[0][2]) # Set the default printer with the name of the printer

    # TO PRINT A FILE:
    # import os
    # os.startfile("requirements.txt", "print")

    return render_template('printers/print.html', printers_list=printers_list, default_printer=default_printer)

