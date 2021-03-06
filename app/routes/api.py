from flask import request, send_from_directory
from app import app
from app.libraries.slug_validate import SlugValidate
from app.controllers.health_indicator import HealthIndicator
from app.controllers.indonesia_administrative import IndonesiaAdministrative
from app.controllers.mountains import Mountains
from app.controllers.climbing_post import ClimbingPost
from app.controllers.stories import Stories
from app.controllers.stories_content import StoriesContent
from app.controllers.uploads import Uploads
from app.controllers.booking import Booking

@app.route('/api')
def helloapi():
    return "Hello World!"

## Health Check ##
@app.route('/health')
def health_indicator():
    return HealthIndicator().run()
##################

## Indonesia Administrative ##
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
##################

## Mountain ##
@app.route('/mountain')
def mountainlistapi():
    return Mountains(request).get_list('')

@app.route('/mountain/<value>')
def mountaindetailapi(value):
    if value.isnumeric():
        return Mountains(request).get_detail('id', value)

    if SlugValidate().run(value):
        return Mountains(request).get_detail('error', value)

    return Mountains(request).get_detail('name', value)
##################

## Climbing Post ##
@app.route('/climbing-post')
def climbingpostlistapi():
    return ClimbingPost(request).get_list()

@app.route('/climbing-post/<value>')
def climbingpostdetailapi(value):
    if value.isnumeric():
        return ClimbingPost(request).get_detail('id', value)

    if SlugValidate().run(value):
        return ClimbingPost(request).get_detail('error', value)

    return ClimbingPost(request).get_detail('name', value)

@app.route('/climbing-post', methods=['POST'])
def climbingpostcreateapi():
    return ClimbingPost(request).create_data()

@app.route('/climbing-post/<id>', methods=['PUT'])
def climbingpostupdateapi(id):
    return ClimbingPost(request).update_data(id)

@app.route('/climbing-post/<id>', methods=['DELETE'])
def climbingpostdeleteapi(id):
    return ClimbingPost(request).delete_data(id)
##################

## Stories ##
@app.route('/stories')
def storieslistapi():
    return Stories(request).get_list()

@app.route('/stories/<value>')
def storiesdetailapi(value):
    if value.isnumeric():
        return Stories(request).get_detail('id', value)

    return Stories(request).get_detail('error', value)

@app.route('/stories', methods=['POST'])
def storiescreateapi():
    return Stories(request).create_data()

@app.route('/stories/<id>', methods=['PUT'])
def storiesupdateapi(id):
    return Stories(request).update_data(id)

@app.route('/stories/<id>', methods=['DELETE'])
def storiesdeleteapi(id):
    return Stories(request).delete_data(id)
##################

## Stories Content ##
@app.route('/stories-content')
def storiescontentlistapi():
    return StoriesContent(request).get_list()

@app.route('/stories-content/<value>')
def storiescontentdetailapi(value):
    if value.isnumeric():
        return StoriesContent(request).get_detail('id', value)

    return StoriesContent(request).get_detail('error', value)

@app.route('/stories-content', methods=['POST'])
def storiescontentcreateapi():
    return StoriesContent(request).create_data()

@app.route('/stories-content/<id>', methods=['PUT'])
def storiescontentupdateapi(id):
    return StoriesContent(request).update_data(id)

@app.route('/stories-content/<id>', methods=['DELETE'])
def storiescontentdeleteapi(id):
    return StoriesContent(request).delete_data(id)
##################

## Booking ##
@app.route('/booking/code')
def bookingcodeapi():
    return Booking(request).get_booking_code()

@app.route('/booking/code/<value>', methods=['POST'])
def bookingcodeavailabilityapi(value):
    return Booking(request).get_availability_code(value.upper())

@app.route('/booking')
def bookinglistapi():
    return Booking(request).get_list()

@app.route('/booking/<booking_code>')
def bookingdetailapi(booking_code):
    return Booking(request).get_detail('code', booking_code.upper())

@app.route('/booking', methods=['POST'])
def bookingcreateapi():
    return Booking(request).create_data()

@app.route('/booking/<booking_code>', methods=['PUT'])
def bookingupdateapi(booking_code):
    return Booking(request).update_data(booking_code.upper())
##################

## Uploads ##
@app.route('/uploads/<path:path>')
def uploadgetfile(path):
    return Uploads(request).get_detail(path)

@app.route('/uploads', methods=['POST'])
def uploadcreateapi():
    return Uploads(request).create_data()

@app.route('/uploads/delete/<path:path>', methods=['DELETE'])
def uploaddeletefile(path):
    return Uploads(request).delete_data(path)
##################