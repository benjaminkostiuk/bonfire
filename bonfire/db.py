from tinydb import Query
from tinydb.queries import where
from .config import config
from .fire import Fire

# Save a bonfire to the database
def save_bonfire(bonfire):
    db = config().db
    db.insert(dict(bonfire))

# Rename a bonfire
def rename_bonfire(bonfire, nickname):
    db = config().db
    return db.update({ 'nickname': nickname }, doc_ids=[bonfire.id])

# List all bonfires stored in the database
def list_bonfires():
    return list(map(Fire.fromdict, config().db.all()))

# Find a bonfire by id
def find_bonfire(identifier):
    db = config().db
    try:
        found = db.get(doc_id=int(identifier))
        return Fire.fromdict(found) if found else None
    except ValueError as e:
        return None

# Delete a bonfire by id
def delete_bonfire(identifiers):
    db = config().db
    try:
        ids = list(map(int, identifiers))
        return db.remove(doc_ids=ids)
    except (KeyError, ValueError) as e:
        return []