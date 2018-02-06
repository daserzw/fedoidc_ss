import logging

from fedoidc_ss.app import init_app

name = 'fedoidc_ss'
app = init_app(name)
logging.basicConfig(level=logging.DEBUG)
app.run(debug=True, host='127.0.0.1', port=5000)
