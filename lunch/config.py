import os.path


host = dict(host='127.0.0.1', port=9999)
ROOT = os.path.dirname(os.path.dirname(__file__))
static_dir = ROOT + '/static/'
templates_dir = ROOT + '/templates/'
users_dir = ROOT + '/data/users/'
