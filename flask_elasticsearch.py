from flask import current_app
from elasticsearch import Elasticsearch


class ElasticSearch(object):
    """
    A thin wrapper around pyelasticsearch.ElasticSearch()
    """
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('ELASTICSEARCH_URL', 'http://localhost:9200/')

        # using the app factory pattern _app_ctx_stack.top is None so what
        # do we register on? app.extensions looks a little hackish (I don't
        # know flask well enough to be sure), but that's how it's done in
        # flask-pymongo so let's use it for now.
        app.extensions['elasticsearch'] = Elasticsearch(app.config['ELASTICSEARCH_URL'])

    def __getattr__(self, item):
        if not 'elasticsearch' in current_app.extensions.keys():
            raise Exception('not initialised, did you forget to call init_app?')
        return getattr(current_app.extensions['elasticsearch'], item)
