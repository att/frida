# Copyright (c) 2019 AT&T Intellectual Property. All rights reserved.

"""
Helper functions for frida
"""
import datetime

def get_unique_filename(*args, delim='_', ext='', datetimed=True, ms=False) -> str:
    """
    Returns filenames unique-ified by the args, delimited by delim (default underscore
    to make splitting the name from the datetime easier), ending with ext, 
    and default including the current ISO datetime, optionally with millisecond precision
    """
    base = delim.join(map(str, args))
    if datetimed:
        base = delim.join([base, '{iso_datetime}'])
        iso_now = datetime.datetime.now().isoformat()
        if not ms:
            # Drop milliseconds - only 1 period in ISODT-6
            iso_now, __ , __ = iso_now.partition('.')

        base = base.format(iso_datetime=iso_now)

    return base + ext