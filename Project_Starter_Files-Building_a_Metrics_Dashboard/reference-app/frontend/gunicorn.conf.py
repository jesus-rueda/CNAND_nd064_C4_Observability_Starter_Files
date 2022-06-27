from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics
print("CONFIGURATION READ")

def child_exit(server, worker):
    GunicornInternalPrometheusMetrics.mark_process_dead_on_child_exit(worker.pid)