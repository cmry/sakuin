# sakuin

![sakuin](https://onyx.uvt.nl/toku/static/sakuin2.png)

>This app only works for :penguin: using :snake: 2 or 3.

## Dependencies

Pip install requirements are `bottle`, `bottle-cork`, `beaker`, `humanfriendly`, and `dateparser`.

## Install

Simply add the `app.wsgi` to your WSGI handler of choice (Apache or Nginx).
Alternatively, you can run the app as a daemon and reverse proxy to its port.
Under `app.wsgi`, change `base` to fit the URL structure (i.e. if you want
it under the main URL it should be changed to `/`. If you want to change the
filedir that `sakuin` monitors, change `fdir` to point *from sakuin* to that
directory.

## Adding New User

To add new users, edit the name and password in `new_user.py` and run the script.
