import smartpy as sp
from datetime import datetime
from random import randint

Objkt = sp.io.import_script_from_url("file:manager.py")

allTarget = "all"

def init(
    scenario,
    admin, 
    objktMinterAddress=sp.address('KT1EwkWSQHCm8MUfFJXrun3GHFDkboXXSCn7')
  ):

  manager = Objkt.CollectionManager(
    admin, 
    objktMinterAddress,
    metadata = sp.big_map(
      {
        "": sp.utils.bytes_of_string("tezos-storage:content"),
        "content": sp.utils.bytes_of_string('{"name":"minter"}')
      }
    )
  )
  scenario += manager
  return manager 

@sp.add_target(name="Admin", kind=allTarget)
def test():
  scenario = sp.test_scenario()
  admin = sp.address("tz1-admin")
  user1 = sp.address("tz1-user-1")
  user2 = sp.address("tz1-user-2")
  manager = init(scenario, admin)

  scenario += manager.setAdmin(user1).run(sender=user1, valid=False, exception='Only admin can call this entrypoint') 
  scenario += manager.setAdmin(user1).run(sender=admin)
  scenario.verify(manager.data.admin == user1)

  scenario += manager.setCollection(666).run(sender=user1)
  scenario.verify(manager.data.collection == 666)
  

@sp.add_target(name="Create collection", kind=allTarget)
def test():
  scenario = sp.test_scenario()
  admin = sp.address("tz1-admin")
  user1 = sp.address("tz1-user-1")
  user2 = sp.address("tz1-user-2")
  manager = init(scenario, admin)

  scenario += manager.createCollection('ipfs://QmYxrBiyUFRRiHycwCnnBCLcwBCo9jsQsBqeAukAXo65jQ').run(sender=admin)

@sp.add_target(name="Mint", kind=allTarget)
def test():
  scenario = sp.test_scenario()
  admin = sp.address("tz1-admin")
  user1 = sp.address("tz1-user-1")
  user2 = sp.address("tz1-user-2")
  manager = init(scenario, admin)

  scenario += manager.setCollection(123).run(sender=admin)
  scenario += manager.mint(sp.record(
    editions=1,
    metadata='ipfs://QmYxrBiyUFRRiHycwCnnBCLcwBCo9jsQsBqeAukAXo65jQ',
    target=user1
  )).run(sender=admin)

@sp.add_target(name="Collaborators", kind=allTarget)
def test():
  scenario = sp.test_scenario()
  admin = sp.address("tz1-admin")
  user1 = sp.address("tz1-user-1")
  user2 = sp.address("tz1-user-2")
  manager = init(scenario, admin)

  scenario += manager.setCollection(123).run(sender=admin)
  scenario += manager.addCollaborator(user1).run(sender=admin)
  scenario += manager.delCollaborator(user1).run(sender=admin)
