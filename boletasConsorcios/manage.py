#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "boletasConsorcios.settings")
    os.environ['MUNI_ID'] = '220'
    os.environ['MUNI_DB'] = 'grupogua_aires'
    os.environ['MUNI_DIR'] = 'aires'
    # os.environ['MUNI_ID'] = '000'
    # os.environ['MUNI_DB'] = 'gg_prueba'
    # os.environ['MUNI_DIR'] = 'prueba'
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
