from flask import current_app
from elasticsearch import Elasticsearch, Urllib3HttpConnection


class ElasticSearch(object):
    """
    A thin wrapper around pyelasticsearch.ElasticSearch()
    """
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('ELASTICSEARCH_URL', 'http://localhost:9200/')

        params = {
            "host": app.config['ELASTICSEARCH_URL']
        }

        if 'ELASTICSEARCH_USER' in app.config.keys() and 'ELASTICSEARCH_PASSWORD' in app.config.keys():
            params.update({
                "http_auth": (app.config['ELASTICSEARCH_USER'], app.config['ELASTICSEARCH_PASSWORD'])
            })
        app.extensions['elasticsearch'] = Elasticsearch(transport_class=Urllib3HttpConnection, **params)

    def __getattr__(self, item):
        if not 'elasticsearch' in current_app.extensions.keys():
            raise Exception('not initialised, did you forget to call init_app?')
        return getattr(current_app.extensions['elasticsearch'], item)
