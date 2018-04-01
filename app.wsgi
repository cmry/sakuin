"""Main stuff."""

# Author:       Chris Emmery
# License:      MIT
# pylint:       disable=C0103

import logging
import os
import time
from glob import glob

import bottle
import dateparser
import humanfriendly
import traceback
from beaker.middleware import SessionMiddleware
from cork import Cork

from keys import file_auth

# environ ---------------------------------------------------------------------

logging.basicConfig(format='localhost - - [%(asctime)s] %(message)s',
                    level=logging.DEBUG)
log = logging.getLogger(__name__)
bottle.debug(True)

session_opts = {
   'session.cookie_expires': True,
   'session.encrypt_key': 'kjnfsdJKSFDJKLF023432J32JK32NJK3KFSDFBDKJFDSF',
   'session.httponly': True,
   'session.timeout': 3600 * 24,  # 1 day
   'session.type': 'cookie',
   'session.validate_key': True,
}

app = bottle.app()
aaa = Cork('auth')
app = application = SessionMiddleware(app, session_opts)
args = {'base': '/sakuin/', 'fdir': './_public', 'aaa': aaa}

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

def check_auth(fn):
    if fn in file_auth:
        try:
            if aaa.current_user.username not in file_auth[fn]:
                return False
            else:
                return True
        except:
            return False
    else:
        return True

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

        if check_auth(fn):
            pass
        else:
            continue

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

@bottle.route('/bananen')
def bananas():
    return '<img src="https://admin.mashable.com/wp-content/uploads/2012/10/dancing_banana.gif"/>'


@bottle.post('/auth')
def auth():
  """Authenticate users"""
  username = post_get('username')
  password = post_get('password')
  print(username, password)
  aaa.login(username, password, success_redirect='./', fail_redirect='./bananen')


@bottle.route('/login')
def login():
    return serve('login')

@bottle.route('/logout')
def logout():
    aaa.logout(success_redirect='./')


@bottle.route('/_public/<filename:path>')
def file_serve(filename):
    if not check_auth(filename):
        return bananas()
    return bottle.static_file(filename, root='_public')


@bottle.route('/<handle>')
def dir_serve(handle):
    """Server dir page."""
    if not check_auth(handle):
        return bananas()
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
    print(aaa._beaker_session)
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
