from flask import request, send_from_directory
from app import app
from app.controllers.eticket import ETicket

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/json')
def main():
    return "json"

@app.route('/eticket/<ticket_code>')
def eticketdetailapi(ticket_code):
    return ETicket(request).get_detail('code', ticket_code.upper())