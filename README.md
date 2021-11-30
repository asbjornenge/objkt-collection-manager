# Objkt Collection Manager

A Collection Manager for the [objkt.com](https://objkt.com) Minting Factory.

This contract can create a collection on objkt.com and mint into it. On top of this you can build a crowdsale or a range minter and get NFTs instantly available on objkt.com :tada:

I am available to build such things. Please [reach out](https://twitter.com/asbjornenge). :wave:

If you use this software, remember to donate some XTZ to tz1UZZnrre9H7KzAufFVm7ubuJh5cCfjGwam so I can afford some salt in my wounds.

## Setup

```
./scipts/init-env.sh
source bin/activate
spy test tests.py output --html
```

## Compile

```
spy compile compile.py compiled
```

## Deploy

```
spy originate-contract --code compiled/randomizer/step_000_cont_0_contract.tz --storage compiled/randomizer/step_000_cont_0_storage.json --rpc https://granadanet.smartpy.io
```

enjoy. 
