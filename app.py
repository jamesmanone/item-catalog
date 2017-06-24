#!/usr/bin/env python

from blueprints import app

app.secret_key = 'correcthorsebatterystaple'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True,)
