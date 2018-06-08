class MultiDBRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'girlstatue':
            return 'girlstatue_db'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'girlstatue':
            return 'girlstatue_db'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'girlstatue' or \
           obj2._meta.app_label == 'girlstatue':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'girlstatue_db':
            return app_label == 'girlstatue'
        elif app_label == 'girlstatue':
            return False
        return None
