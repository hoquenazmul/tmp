class DefaultDatabaseRouter:
    def db_for_read(self, model, **hints):
        return None

    def db_for_write(self, model, **hints):
        return None

    def db_for_migrate(self, db, app_label, model_name=None, **hints):
        return 'default'

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == 'default'
