import itertools
import datetime
import logging
import time
import typing as t

import pydantic
import requests
import mongoengine as me
import pymongo as pm

import conf
from server import models


settings = conf.get_settings()
logging.basicConfig(level=logging.INFO)


class BaseModel(pydantic.BaseModel):

    @pydantic.validator('*', pre=True)
    def blank_strings(cls, v):
        """Convert empty strings to None (to save DB space).
        """
        if v == "":
            return None
        return v


class AddsIn(BaseModel):
    str_id: str = pydantic.Field(alias='id')
    categories: dict
    block_reasons: dict
    title: str
    body: t.Optional[str]
    videos: t.Optional[dict]
    price: dict
    republished: datetime.datetime
    delivery: t.Optional[dict]
    views_counter: int
    expire: datetime.datetime
    images: t.Optional[dict]
    offer_type: dict
    posted: datetime.datetime
    autorepublisher: dict
    contacts: dict
    state: str
    location: dict
    features_groups: t.List[dict]
    type: str


def chunker(iterable, n):
    """
    Split iterable into chunks of n items.
    """
    # https://stackoverflow.com/a/29524877/248296
    it = iter(iterable)
    while True:
        chunk_it = itertools.islice(it, n)
        try:
            first_el = next(chunk_it)
        except StopIteration:
            return
        yield list(itertools.chain((first_el,), chunk_it))


def make_request():
    adds = requests.get(f'{settings.API_URL}/adverts',
                        auth=(settings.API_KEY, "")).json()
    incoming_adds = []
    total = int(adds["total"])
    if int(adds["page_size"]) >= int(adds["total"]):
        for add in adds["adverts"]:
            req = requests.get(f'{settings.API_URL}/adverts/{add["id"]}?lang=ru', auth=(settings.API_KEY, ""))
            while req.status_code == 429:
                time.sleep(1)
                logging.warning('Code: 429. Wait. You are very fast.')
                req = requests.get(f'{settings.API_URL}/adverts/{add["id"]}?lang=ru', auth=(settings.API_KEY, ""))
            incoming_adds.append(req.json())

    else:
        new_adds = requests.get(f'{settings.API_URL}/adverts?page=1',
                                auth=(settings.API_KEY, "")).json()
        page = 1
        for add in new_adds["adverts"]:
            req = requests.get(f'{settings.API_URL}/adverts/{add["id"]}?lang=ru', auth=(settings.API_KEY, ""))
            while req.status_code == 429:
                time.sleep(1)
                logging.warning('Code: 429. Wait. You are very fast.')
                req = requests.get(f'{settings.API_URL}/adverts/{add["id"]}?lang=ru', auth=(settings.API_KEY, ""))
            incoming_adds.append(req.json())
        while len(incoming_adds) < total:
            page += 1
            new_adds = requests.get(f'{settings.API_URL}/adverts?page={page}',
                                    auth=(settings.API_KEY, "")).json()
            for add in new_adds["adverts"]:
                req = requests.get(f'{settings.API_URL}/adverts/{add["id"]}?lang=ru', auth=(settings.API_KEY, ""))
                while req.status_code == 429:
                    time.sleep(1)
                    logging.warning('Code: 429. Wait. You are very fast.')
                    req = requests.get(f'{settings.API_URL}/adverts/{add["id"]}?lang=ru', auth=(settings.API_KEY, ""))
                incoming_adds.append(req.json())
    return update_price(incoming_adds)


def gen(
        data_in: t.Iterable[dict],
        model_in: t.Type[pydantic.BaseModel],
        model_db: t.Type[me.Document],
):
    """
    Make a generator of MongoEngine docs to be able to split it and save
    into the database in chunks.
    """
    for data in data_in:
        data = model_in(**data)
        yield model_db(**data.dict())


def save_docs(
        docs: t.Iterable[me.Document],
):
    """
    Save MongoEngine docs to the database and remove stale docs.
    """
    updated_docs = 0
    inserted_docs = 0
    synced_on = datetime.datetime.utcnow()

    for _docs in chunker(docs, 100):
        commands = []
        for doc in _docs:
            doc.synced_on = synced_on
            commands.append(pm.ReplaceOne({'_id': doc['str_id']}, doc.to_mongo(), upsert=True))
        db = models.Adds._get_db()
        collection = db.Adds
        try:
            write_result = collection.bulk_write(commands)
        except me.errors.BulkWriteError as exc:
            write_result = exc.__context__.details['nInserted']
            fail_count = write_result.modified_count + write_result.upserted_count + \
                         updated_docs + inserted_docs
            logging.warning('Failed to insert %s docs')

        updated_docs += write_result.modified_count
        inserted_docs += write_result.upserted_count
        logging.info(f' {datetime.datetime.now()} Updated: {updated_docs}, inserted: {inserted_docs}')
        models.Adds.objects(synced_on__ne=synced_on).delete()


def update_price(incoming_adds):
    import services.bnm_md as bnm
    ratio = float(bnm.get_exchang()['eur'])
    for add in incoming_adds:
        if add['price']['unit'] == 'eur':
            add['price']['unit'] = 'mdl'
            add['price']['value'] = float("{0:.2f}".format(add['price']['value']*ratio))
    return incoming_adds


def update_all():
    logging.info(f' {datetime.datetime.now()} Start Update Db')
    data_in = make_request()
    save_docs(gen(data_in, AddsIn, models.Adds))

