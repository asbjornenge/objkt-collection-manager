import smartpy as sp
import json
import os
from datetime import datetime, timezone
env = os.environ

def UTCTimestamp(datestring):
  dt = datetime.strptime(datestring, '%y-%m-%dT%H:%M')
  dt_utc = dt.replace(tzinfo=timezone.utc)
  return int(dt_utc.timestamp())

Objkt = sp.io.import_script_from_url("file:manager.py")

managerMetadata = {
  "name": "Objkt Collection Manager",
  "version": "1.0.0",
  "authors": ["asbjornenge <asbjorn@tezid.net>"],
  "homepage": "https://twitter.com/asbjornenge",
  "interfaces": ["TZIP-016"]
}

#objktMinterAddress = sp.address('KT1EwkWSQHCm8MUfFJXrun3GHFDkboXXSCn7') <- granadanet, but it's not working properly
objktMinterAddress = sp.address('KT1Aq4wWmVanpQhq4TTfjZXB5AjFpx15iQMM')
asbjorn = sp.address('tz1UZZnrre9H7KzAufFVm7ubuJh5cCfjGwam')

sp.add_compilation_target("manager", Objkt.CollectionManager(
  asbjorn, 
  objktMinterAddress,
  metadata = sp.big_map(
    {
      "": sp.utils.bytes_of_string("tezos-storage:content"),
      "content": sp.utils.bytes_of_string(json.dumps(managerMetadata))
    }
  )
))

