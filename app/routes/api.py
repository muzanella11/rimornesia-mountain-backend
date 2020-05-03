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
def provincelistapi():
    return IndonesiaAdministrative(request).get_list('provinces')

@app.route('/province/<value>')
def provincedetailapi(value):
    if value.isnumeric():
        return IndonesiaAdministrative(request).get_detail('provinces', 'id', value)

    return IndonesiaAdministrative(request).get_detail('provinces', 'name', value)

@app.route('/district')
def districtlistapi():
    return IndonesiaAdministrative(request).get_list('districts')

@app.route('/district/<value>')
def districtdetailapi(value):
    if value.isnumeric():
        return IndonesiaAdministrative(request).get_detail('districts', 'id', value)

    return IndonesiaAdministrative(request).get_detail('districts', 'name', value)

@app.route('/regency')
def regencylistapi():
    return IndonesiaAdministrative(request).get_list('regencies')

@app.route('/regency/<value>')
def regencydetailapi(value):
    if value.isnumeric():
        return IndonesiaAdministrative(request).get_detail('regencies', 'id', value)

    return IndonesiaAdministrative(request).get_detail('regencies', 'name', value)

@app.route('/village')
def villagelistapi():
    return IndonesiaAdministrative(request).get_list('villages')

@app.route('/village/<value>')
def villagedetailapi(value):
    if value.isnumeric():
        return IndonesiaAdministrative(request).get_detail('villages', 'id', value)

    return IndonesiaAdministrative(request).get_detail('villages', 'name', value)