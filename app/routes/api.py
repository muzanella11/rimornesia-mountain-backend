from app import app
from app.controllers.health_indicator import HealthIndicator

@app.route('/api')
def helloapi():
    return "Hello World!"

@app.route('/health')
def health_indicator():
    return HealthIndicator().run()