from asyncio.log import logger
from flask import Flask, jsonify
from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics
import logging
from jaeger_client import Config


app = Flask(__name__)
metrics = GunicornInternalPrometheusMetrics(app)


def init_tracer(service):
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name=service,
    )

    # this call also sets opentracing.tracer
    return config.initialize_tracer()

tracer = init_tracer('backend')


@app.route("/")
def homepage():
    return "Hello World"

@app.route("/fail")
def going_to_fail():
    raise Exception("Something is wrong")

@app.route("/api")
def my_api():
    with tracer.start_span('backend-span') as span:
        span.set_tag('http.url', '/api')        
        span.set_tag('http.method', "GET")

        answer = "something"
        response = jsonify(repsonse=answer)
        span.set_tag('http.status_code', 200)
        logging.info("api requests")
        return response


if __name__ == "__main__":
    app.run()
