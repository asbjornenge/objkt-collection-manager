import smartpy as sp

class CollectionManager(sp.Contract):
  def __init__(
    self,
    admin,
    objktMinterAddress,
    metadata
  ):

    self.init(
      admin=admin,
      objktMinterAddress=objktMinterAddress,
      metadata=metadata,
      collection=0,
    ) 

  ## Helper functions
  #

  def bytes_of_string(self, s):
      b = sp.pack(s)
      return sp.slice(b, 6, sp.as_nat(sp.len(b) - 6)).open_some("Could not get bytes of string")

  def checkAdmin(self):
    sp.verify(sp.sender == self.data.admin, 'Only admin can call this entrypoint')

  def checkCollection(self):
    sp.verify(self.data.collection != 0, 'Collection id not set')

  ## Admin
  #

  @sp.entry_point
  def setAdmin(self, admin):
    self.checkAdmin()
    self.data.admin = admin

  @sp.entry_point
  def setCollection(self, collection):
    self.checkAdmin()
    self.data.collection = collection 

  ## Collection
  #

  @sp.entry_point
  def createCollection(self, metadata):
    self.checkAdmin()
    sp.set_type(metadata, sp.TString)
    entrypoint = sp.contract(
      sp.TBytes, 
      self.data.objktMinterAddress,
      entry_point='create_artist_collection').open_some('No such entrypoint')
    sp.transfer(self.bytes_of_string(metadata), sp.mutez(0), entrypoint)

  ## Mint
  #

  @sp.entry_point
  def mint(self, editions, metadata, target):
    self.checkAdmin()
    self.checkCollection()
    sp.set_type(metadata, sp.TString)
    arg = sp.record(
      collection=self.data.collection,
      editions=editions,
      metadata_cid=self.bytes_of_string(metadata),
      target=target
    )
    entrypoint = sp.contract(
      sp.TRecord(collection=sp.TNat, editions=sp.TNat, metadata_cid=sp.TBytes, target=sp.TAddress), 
      self.data.objktMinterAddress,
      entry_point='mint_artist').open_some('No such entrypoint')
    sp.transfer(arg, sp.mutez(0), entrypoint)

  ## Collab
  #

  @sp.entry_point
  def addCollaborator(self, collaborator):
    self.checkAdmin()
    self.checkCollection()
    entrypoint = sp.contract(
      sp.TRecord(collaborator=sp.TAddress, collection_id=sp.TNat),
      self.data.objktMinterAddress,
      entry_point='invite_collaborator').open_some('No such entrypoint')
    arg = sp.record(
      collaborator=collaborator,
      collection_id=self.data.collection,
    )
    sp.transfer(arg, sp.mutez(0), entrypoint)

  @sp.entry_point
  def delCollaborator(self, collaborator):
    self.checkAdmin()
    self.checkCollection()
    entrypoint = sp.contract(
      sp.TRecord(collaborator=sp.TAddress, collection_id=sp.TNat),
      self.data.objktMinterAddress,
      entry_point='remove_collaborator').open_some('No such entrypoint')
    arg = sp.record(
      collaborator=collaborator,
      collection_id=self.data.collection,
    )
    sp.transfer(arg, sp.mutez(0), entrypoint)
