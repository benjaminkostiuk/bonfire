from tinydb import Query
from tinydb.queries import where

from .exceptions import BonfireNotFound, MultipleBonfiresFound
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

# Find a bonfire by id or nickname
def find_bonfire_by_id(id):
    db = config().db
    try:
        found = db.get(doc_id=int(id))
    except (KeyError, ValueError) as e:
        found = None 
    if not found:
        raise BonfireNotFound('No bonfire with id {} found.')
    return Fire.fromdict(found)

# Find a bonfire by nickname
def find_bonfire_by_nickname(nickname):
    db = config().db
    found = db.search(where('nickname') == nickname) 
    if not found:
        raise BonfireNotFound("No bonfires found for nickname '{}'".format(nickname))
    elif len(found) > 1:
        raise MultipleBonfiresFound("Multiple bonfires with nickname '{}' found.".format(nickname))
    return Fire.fromdict(found[0])

# Delete a bonfire by id
def delete_bonfire(identifiers):
    db = config().db
    try:
        ids = list(map(int, identifiers))
        return db.remove(doc_ids=ids)
    except (KeyError, ValueError) as e:
        return []