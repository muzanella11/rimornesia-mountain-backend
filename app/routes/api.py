from flask import request
from app import app
from app.controllers.health_indicator import HealthIndicator
from app.controllers.indonesia_administrative import IndonesiaAdministrative

@app.route('/api')
def helloapi():
    return "Hello World!"

@app.route('/health')
def health_indicator():
    return HealthIndicator().run()

@app.route('/province')
def provinceapi():
    return IndonesiaAdministrative(request).province()

@app.route('/province/<param>')
def provincebyparamapi(param):
    if param.isnumeric():
        return IndonesiaAdministrative(request).province_by_id(param)

    return IndonesiaAdministrative(request).province_by_name(param)