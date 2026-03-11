
class ExternalDBRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == "prediction_proxy":
            return "prediction_db"
        
        if model._meta.app_label == "service_proxy":
            return "service_db"
        
        return None

    def db_for_write(self, model, **hints):
        return None

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return None
