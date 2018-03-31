"""Main stuff."""

# Author:       Chris Emmery
# License:      MIT
# pylint:       disable=C0103

import os
from glob import glob
import time
import bottle
import humanfriendly
import dateparser
import traceback

# environ ---------------------------------------------------------------------
app = bottle.app()
args = {'base': '/sakuin/', 'fdir': './_public', 'os': os}

# general functionality -------------------------------------------------------

@bottle.route('/static/<filename:path>')
def server_static(filename):
    """Static file includes."""
    return bottle.static_file(filename, root='static')


def postd():
    """Access form data."""
    return bottle.request.forms


def post_get(name, default=''):
    """Retrieve POST data."""
    return bottle.request.POST.getunicode(name, default).strip()


def serve(page, **kwargs):
    """Serve page."""
    return bottle.template('main', content=bottle.template(page, args=args,
                           **kwargs), args=args)

# app specific ----------------------------------------------------------------

def sizeof_fmt(num, suffix=''):
    """Get size of file."""
    for unit in ['b','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Y', suffix)

def collect(fdir):
    """Collect general file info based on fdir."""
    globbar = glob(fdir)
    fils, dirs, finf = [], [], {}
    for f in globbar:
        fn = f.replace(args['fdir'] + '/', '')
        if '.' in f.split('/')[-1]:
            fils.append(fn)
        else:
            dirs.append(fn)
        file_info = os.stat(f)
        finf[fn] = {'size': sizeof_fmt(file_info.st_size),
                    'bsize': file_info.st_size,
                    'ctime': time.ctime(file_info.st_ctime),
                    'date': dateparser.parse(time.ctime(file_info.st_ctime)
                        ).strftime("%d %b %H:%M"),
                    'full': f}

    fsum = {}
    for k, v in finf.items():
        if not fsum.get('bsize'):
            fsum['bsize'] = 0
        fsum['bsize'] += v['bsize']

    fsum['fcount'] = len(fils)
    fsum['dcount'] = len(dirs)
    fsum['size'] = sizeof_fmt(fsum['bsize'])

    return dirs, fils, finf, fsum

# app routes ------------------------------------------------------------------

@bottle.route('/_public/<filename:path>')
def file_serve(filename):
    return bottle.static_file(filename, root='_public')


@bottle.route('/<handle>')
def dir_serve(handle):
    """Server dir page."""
    try:
        if '.' in handle:
            return file_serve(handle)

        dirs, fils, finf, fsum = collect(args['fdir'] + '/' + handle + '/*')

        return serve('index', dirs=dirs, fils=fils, finf=finf, fsum=fsum)
    except:
        return str(traceback.format_exc())


@bottle.route('/')
def root():
    """Mains page."""
    try:
        dirs, fils, finf, fsum = collect(args['fdir'] + '/*')
        return serve('index', dirs=dirs, fils=fils, finf=finf, fsum=fsum)
    except:
        return str(traceback.format_exc())

def main():
    """Boot website."""
    bottle.debug(True)
    bottle.run(app=app, host='0.0.0.0', port=8080, quiet=False, reloader=True)


if __name__ == "__main__":
    main()
