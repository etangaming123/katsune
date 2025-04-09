# Katsune

The Discord bot used in the server [Ghost Hunt](https://discord.gg/CpsCCqSAmq "The invite to the Discord Server")!

This bot's source code is **open source**, so free feel to use this for your own bot, or help with the development of this bot!

> [!NOTE]
> Katsune is still in its early stages of development, so some aspects may be low quality or non functional. If you find an error with usage of the bot in Ghost Hunt's official server, please [create a new issue here.](https://github.com/etangaming123/katsune/issues/new "Issue creation page")

## Roblox Integration

To verify your Roblox account with Discord, run /roblox-link-step-1. You will need to enter your username.

## Katsuprofiles

> [!NOTE]
> Katsuprofiles has not yet been added as of writing this.

## Your own usage

Katsune is free to use in your own Discord server if you wish to!

> [!TIP]
> Test your Discord bot before sending invites!

### Roblox setup

(what you have to do in Roblox)

Copy the [Katsune Verification Place](https://www.roblox.com/games/140030248253073/Katsune-Verification-Place "The Roblox experience used to link Roblox accounts with Discord") and publish it to your own profile/group if you wish to setup Roblox linking with your Discord bot. If you wish, you can change the UI of the "experience" (game) because as of writing this, it's very barebones.

Take note of the ID of your "experience" (game), you'll need it for local setup.

Create a new [API Key](https://create.roblox.com/dashboard/credentials?activeTab=ApiKeysTab "Roblox API key management") and give the key the following permissions for your verification place:

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

> [!WARNING]
> Katsune was not programmed for other usages other than the Ghost Hunt Discord server. Use this script on your own server at your own risk!

Install the [required libraries](requirements.txt "requirements.txt file for pip"), set up the variables in [katsune.py](katsune.py "The Python script used to host the bot, what else?") so that they match your preferred settings:

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
> It's recommended that you change most of the strings, such as the ones where the bot responds to a slash command or button press.

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

Katsune is licensed under the [GNU General Public License v2.0](LICENSE "License") (one of the license templates offered by Github). View it here: [./LICENSE](./LICENSE)
