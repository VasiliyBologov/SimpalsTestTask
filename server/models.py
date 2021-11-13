import mongoengine as me


class BaseModel(me.Document):
    meta = {
        'abstract': True,
    }

    @classmethod
    def _get_db(cls):
        import conf

        # Get settings to register mongodb connections, set up logging, etc.
        conf.get_settings()

        return super()._get_db()

    def to_dict(self):
        return self.to_mongo(use_db_field=False).to_dict()

    def __repr__(self):
        return f'{self.__class__.__str__}{self.to_dict()}'


class SyncedModel(BaseModel):
    synced_on = me.DateTimeField()

    meta = {
        'abstract': True,
    }


class Adds(SyncedModel):
    str_id = me.StringField(primary_key=True)
    categories = me.DictField()
    block_reasons = me.DictField()
    title = me.StringField()
    body = me.StringField(blank=True, null=True)
    videos = me.DictField(blank=True, null=True)
    price = me.DictField()
    republished = me.DateTimeField()
    delivery = me.DictField(blank=True, null=True)
    views_counter = me.IntField()
    expire = me.DateTimeField()
    images = me.DictField(blank=True, null=True)
    offer_type = me.DictField()
    posted = me.DateTimeField()
    autorepublisher = me.DictField()
    contacts = me.DictField()
    state = me.StringField()
    location = me.DictField()
    features_groups = me.ListField()
    type = me.StringField()

    meta = {
        'collection': 'Adds',
    }

    def __str__(self):
        return self.title
