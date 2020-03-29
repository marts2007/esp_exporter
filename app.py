import socket

import json
from flask import Flask, escape, request, g

app = Flask(__name__)
cache = {}



@app.route('/temp/data.php')
def claymore():
    ready = True
    if not 'humidity' in cache:
        cache['humidity']=None
        ready=False
    if not 'temp_in' in cache:
        cache['temp_in']=None
        ready=False
    if not 'temp_out'  in cache:
        cache['temp_out']=None
        ready=False
    if not 'pressure' in cache:
        cache['pressure']=None
        ready=False

    t=request.args.get('temp',default=None, type=float)
    if t:
        cache['temp_out']=t
    t=request.args.get('tempin',default=None, type=float)
    if t:
        cache['temp_in']=t
    h=request.args.get('tempin',default=None, type=float)
    if h:
        cache['humidity']=h
    p=request.args.get('pressure',default=None, type=float)
    if p:
        cache['pressure']=p
    if ready:
        metrics = 'esp_humidity{sensor="inside"} %(h)s\n' % dict(h=cache['humidity'])
        metrics = metrics + 'esp_tempreture{sensor="inside"} %(t)s\n' % dict(t=cache['temp_in'])
        metrics = metrics + 'esp_tempreture{sensor="outside"} %(t)s\n' % dict(t=cache['temp_out'])
        metrics = metrics + 'esp_pressure %(p)s\n' % dict(p=cache['pressure'])
        return metrics
    return ''

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')



