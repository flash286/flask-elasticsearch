from flask import current_app
from elasticsearch import Elasticsearch, RequestsHttpConnection


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
        }

        if app.config.get('ELASTICSEARCH_USER', False) and app.config.get('ELASTICSEARCH_PASSWORD', False):
            params.update({
                "http_auth": (app.config['ELASTICSEARCH_USER'], app.config['ELASTICSEARCH_PASSWORD'])
            })
        app.extensions['elasticsearch'] = Elasticsearch(
            [app.config['ELASTICSEARCH_URL']], **params
        )

    def __getattr__(self, item):
        if not 'elasticsearch' in current_app.extensions.keys():
            raise Exception('not initialised, did you forget to call init_app?')
        return getattr(current_app.extensions['elasticsearch'], item)

