# Katsune

The Discord bot used in the server [Ghost Hunt](https://discord.gg/CpsCCqSAmq "The invite to the Discord Server")!

This bot's source code is **open source**, so free feel to use this for your own bot, or help with the development of this bot!

>  [!NOTE]
> Katsune is still in its early stages of development, so some aspects may be low quality or non functional. If you find an error with usage of the bot in Ghost Hunt's official server, please [create a new issue here.](https://github.com/etangaming123/katsune/issues/new)

## Features

Katsune has many features, including:

* Roblox integration
* Anonymous messaging
* Conversation starters

And there are more features to come:

* Katsuprofiles
* [Good noodle](https://www.youtube.com/watch?v=RqkwI-ucNc4) leaderboard

## Your own usage

Katsune is free to use in your own Discord server if you wish to!

> [!TIP]
> Test your Discord bot before sending invites!

### Roblox setup

(what you have to do in Roblox)

Copy the [Katsune Verification Place](https://www.roblox.com/games/140030248253073/Katsune-Verification-Place) and publish it to your own profile/group if you wish to setup Roblox linking with your Discord bot. If you wish, you can change the UI of the "experience" (game) because as of writing this, it's very barebones.

Take note of the ID of your "experience" (game), you'll need it for local setup.

Create a new [API Key](https://create.roblox.com/dashboard/credentials?activeTab=ApiKeysTab) and give the key the following permissions for your verification place:

* universe-datastores:
  * universe-datastores.objects:create
  * universe-datastores.objects:delete
  * universe-datastores.objects:update
  * universe-datastores.objects:read
  * universe-datastores.control:create
* ordered-data-stores:
  * universe.ordered-data-store.scope.entry:read
  * universe.ordered-data-store.scope.entry:write

Save your API key somewhere safe, you'll also need that for local setup.

### Local Setup

(what you have to do on the device running katsune.py)

Install the [required libraries](requirements.txt), set up the variables in [katsune.py](katsune.py) so that they match your preferred settings:

```python
memberjoinleavechannelid = 1125568412882583552 # channel id to say when a user leaves or joins
verificationchannelid = 1129962618346553450 # channel to send verification confirmation message
anonchannelid = 1128811704726339614 # channel to send anonymous messages
katsunelogid = 1233388519075086366 # channel to send anonymous message reports, etc
verifiedroleid = 1129960240922759218 # the verified role's id
adminroleids = [883261775510921256, 883261098059522078] # users with these role ids gain specific permisions
powerusers = [723053854194663456, 627196747676123146] # users with these ids gain even more perms, but do not have the same perms as the above
robloxgameid = 6869030592 # roblox: the game id that has its datastores linked or smth
emojilist = ["👻", "💸", "💡", "💥", "🍬", "🤖", "🖥️", "🎮", "🔨"] # supports any string
ghosthuntserverid = 883235310580957234 # the id of the bot's current server
```

> [!TIP]
> It's recommended that you change most of the strings, specifically the ones where the bot responds to a slash command or button press.

Create a new file named keys.json in the same directory as katsune.py:

```json
{
    "robloxapikey": "A Roblox API key that can access your datastores in Roblox",
    "bottoken": "The token for the Discord bot"
}
```

Once you've setup the variables, run katsune.py! It will automatically create the data files (.pkl).

And now you have Katsune in your own server!

## Licensing

Katsune is licensed under the [GNU General Public License v2.0](LICENSE) (one of the license templates offered by Github). 

### Summary of license (directly from Github's license template selection)

Allowed:

* **Commercial use**
  * The licensed material and derivatives may be used for commercial purposes.
* **Modification**
  * The licensed material may be modified.
* **Distribution**
  * The licensed material may be distributed.
* **Private use**
  * The licensed material may be used and modified in private.

Limitations:

* **Liability**
  * This license includes a limitation of liability.
* **Warranty**
  * This license explicitly states that it does NOT provide any warranty.

Conditions:

* **License and copyright notice**
  * A copy of the license and copyright notice must be included with the licensed material.
* **State changes**
  * Changes made to the licensed material must be documented.
* **Disclose source**
  * Source code must be made available when the licensed material is distributed.
* **Same license**
  * Modifications must be released under the same license when distributing the licensed material. In some cases a similar or related license may be used.
