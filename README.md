# Katsune

The Discord bot used in the server [Ghost Hunt](https://discord.gg/CpsCCqSAmq "The invite to the Discord Server")!

This bot's source code is **open source**, so free feel to use this for your own bot, or help with the development of this bot!

> [!NOTE]
> Katsune is still in its early stages of development, so some aspects may be low quality or non functional. If you find an error with usage of the bot in Ghost Hunt's official server, please [create a new issue here.](https://github.com/etangaming123/katsune/issues/new "Issue creation page")

## Roblox Integration

To link your Roblox account with Discord, run /roblox-link-step-1. You will need to enter your username.

After that, join the "experience" (game) that the bot has sent after running /roblox-link-step-1, and follow the instructions from there. After completing those instructions, run /roblox-link-step-2 and you're done! Your Roblox account has been linked with Discord.

## KatsuProfiles

> [!IMPORTANT]
> KatsuProfiles are in early stages of development, use at your own risk!

> [!TIP]
> It's recommended to link your Roblox user with Katsune if you wish to use KatsuProfiles.

KatsuProfiles are "mini-profiles" for each user!

Viewing a profile using /view-profile [user] will show their Katsuprofiles.

KatsuProfiles can be modified to show either a Roblox or Discord username/displayname, a profile picture, and a custom "about me" section using the /edit-katsuprofile and /configure-katsuprofile, as well as your Roblox information and the amount of good noodles you have.

KatsuProfiles also come with a "supporter" tag, which can be brought if a user has at least one of the specified gamepasses. These gamepasses can be modified by adding them to the following list within the script:

```python
gamepassids = [] # gamepass ids for katsune supporter
```

Supporters have more features, such as setting a custom pfp, having a yellow embed background, and a star next to their user/displayname!

Here's an example of a Katsuprofile:

![my katsuprofile in ghost hunt's server](https://raw.githubusercontent.com/etangaming123/katsune/refs/heads/main/docs/katsuprofile.png)

## Other features

### Good Noodles

[haha spunch bob refence](https://www.youtube.com/watch?v=RqkwI-ucNc4)

Good noodles is like a rewards system that owners of servers can use to give out "good noodles" to their server members!

(and yes, there is a leaderboard.)

### /catwoman

![a screenshot](https://raw.githubusercontent.com/etangaming123/katsune/refs/heads/main/docs/thatonescreenshot.png)

### /ship

shipping is literally a random number generator and should not be taken seriously.

### Fancy banning

Ever had a debate with your mod team whether to ban someone on your server or not? Fancybans will fix that!

Fancybans allow server owners (or power users) to make a vote to ban a specific user, and once that number of votes has been reached, they will be able to administer the ban with a simple command.

By default, only staff in your server can vote to ban.

## Your own usage

> [!WARNING]
> Katsune was not programmed for other Discord servers. Use this script on your own server at your own risk!

Katsune is free to use in your own Discord server if you wish to! Please note, issues that occur during your own usage cannot be reported as bugs.

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

Install the [required libraries](requirements.txt "requirements.txt file for pip"), and set up the variables in [katsune.py](katsune.py "The Python script used to host the bot, what else?") so that they match your preferred settings:

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

## Contributing

You can report issues with Katsune [here](https://github.com/etangaming123/katsune/issues/new). Please note that issues can only be created if you find a bug in the official Katsune bot (in the Ghost Hunt server.)

You can also create a new [pull request](https://github.com/etangaming123/katsune/pulls) if there's code that can be improved.

Please note that I may not be able to respond to your issue or pull request immediately. Pull requests cannot be new features, please post that as a suggestion in the Ghost Hunt server.

## Licensing

Katsune is licensed under the [GNU General Public License v2.0](LICENSE "License") (one of the license templates offered by Github). View it here: [./LICENSE](./LICENSE)
