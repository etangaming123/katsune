print(">> Katsune Alpha v1.00.13 <<") # katsune more like kasane teto or HATSUNE LO
# i hope you like the comments btw
# btw when you startup this bot you get a LOT of print messages saying invalid escape sequence or smth like smth to do with backslashes, ignore those (this only happens if you're using default strings and have not modified them in any way)
# [ modules ]
import discord
from discord.ext import commands
from discord import app_commands
import pickle
import random
import traceback
import requests
import json
import os

# [ set information ]
# basically, since i don't want to share the discord bot token and roblox api keys i put them in a separate json // future etan here, i feel like i should use a .env but im not bothered
with open("keys.json", "rb") as file: # {"bottoken": "Discord Bot Token", "robloxapikey": "Key to access datastores in a Roblox experience"}
    sensitivedata = json.load(file)
bottoken = sensitivedata["bottoken"]
robloxapikey = sensitivedata["robloxapikey"]

# [ data setup ]
# if the .pkl files are not found, katsune will automatically create them
datastores = ["readnotices", "bannedanons", "conversationstarters", "katsuprofiles", "linkedrobloxaccounts", "anonymousmessages"]
for item in datastores:
    if not os.path.exists(f"{item}.pkl"):
        with open(f"{item}.pkl", "wb") as file:
            pickle.dump({}, file)
        print(f"Created new file [{item}.pkl]")

# [ variables ]
# --data--
defaultkatsuprofile = {"AboutMe": "", "DisplayRoblox": False, "DisplaySupporter": False, "DisplayGoodNoodles": False, "Pfp": "Discord", "CustomPFPUrl": "", "DisplayName": "DiscordDisplay", "Name": "DiscordUser"}

# --discord--
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
# OOO is replaced by @user for welcome and leave messages
welcomemessages = ["OOO joined the server! Welcome!", "OOO.Parent = discord.Servers[\"Ghost Hunt (Roblox)\"]", "Another fellow ghost hunter joined us! Welcome OOO!", "OOO joined the asylum, they can never leave!"]
leavemessages = ["We were right, OOO didn't enjoy their stay!", "An unexpected error occurred and OOO needs to quit. We're sorry!", "OOO pressed the leave button on accident", "Shutting down OOO..."]
memberjoinleavechannelid = 1125568412882583552 # channel id to say when a user leaves or joins
verificationchannelid = 1129962618346553450 # channel to send verification confirmation message
anonchannelid = 1128811704726339614 # channel to send anonymous messages
katsunelogid = 1233388519075086366 # channel to send anonymous message reports, etc
verifiedroleid = 1129960240922759218 # the verified role's id
goodnoodleroleid = 1107836361920217118 # the good noodle role's id
adminroleids = [883261775510921256, 883261098059522078] # users with these role ids gain specific permisions
powerusers = [723053854194663456, 627196747676123146] # users with these ids gain even more perms, but do not have the same perms as the above
robloxgameid = 6869030592 # roblox: the game id that has its datastores linked or smth
gamepassids = [] # gamepass ids for katsune supporter
emojilist = ["👻", "💸", "💡", "💥", "🍬", "🤖", "🖥️", "🎮", "🔨"] # supports any string
serverid = 883235310580957234 # the id of the bot's current server
supportergamepassids = [] # enter in the gamepass ids to gain supporter for katsuprofile (the user has to own at least one)
server = None # set to none for now, this will be initialised later

# --other--
pfpdisplays = ["Discord", "Roblox", "Custom"] # the pfps that can be displayed on katsuprofiles
namedisplays = ["DiscordDisplay", "DiscordUser", "RobloxDisplay", "RobloxUser"] # the names and displaynames that can be displayed on katsuprofiles

# [ functions ]
# --internal--
def saveData(store: str, newdata: dict): # Saves data to a specified .pkl file
    print(f"Saving [{store}]...")
    try:
        with open(f"{store}.pkl", "wb") as file:
            pickle.dump(newdata, file)
            return True # Return true if it succeeds
    except Exception:
        traceback.print_exc()
        return False # Otherwise return false

def loadData(store: str): # Gets data from a specified .pkl file
    print(f"Loading [{store}]...")
    try:
        with open(f"{store}.pkl", "rb") as file:
            return pickle.load(file) # Return file data if it succeeds
    except Exception:
        traceback.print_exc()
        return "" # Otherwise return an empty string

def formatUsername(user: discord.User): # Fancy formatting for usernames // displayname (@username)
    if user.global_name == None:
        return f"{user.name}"
    else:
        return f"{user.global_name} (@{user.name})"

# --discord--
async def sendwelcome(membermention): # sends a welcome message
    channel = bot.get_channel(memberjoinleavechannelid)
    await channel.send(welcomemessages[random.randint(1, len(welcomemessages) - 1)].replace("OOO", membermention))

async def sendbye(membermention): # sends a goodbye message
    channel = bot.get_channel(memberjoinleavechannelid)
    await channel.send(leavemessages[random.randint(1, len(leavemessages) - 1)].replace("OOO", membermention))

async def changerpc(newrpc: str): # changes the bot's rpc (playing [game])
    await bot.change_presence(activity=discord.Game(newrpc), status=discord.Status.online)

async def sendVerificationSystem(): # sends the verify button in the verification channel (ew nested code EW EW EW)
    class ConfirmButtonVerify(discord.ui.View): # verify button !!
        def __init__(self):
            super().__init__(timeout=None) # no button timeout
        @discord.ui.button(label="Verify", style=discord.ButtonStyle.green)
        async def confirmbuttonverify(self, interaction, button):
            if verifiedroleid in [role.id for role in interaction.user.roles]: # check if user is already verified
                await interaction.response.send_message(content="You are already verified!", ephemeral=True)
                return
            usedemojilist = random.sample(emojilist, 5)
            realemoji = random.sample(usedemojilist, 1)[0]

            async def nowayitsabutton(self, interaction, button, number): # function for a button
                if usedemojilist[number] == realemoji: # no way they verified !!!
                    print(f"{formatUsername(interaction.user)} has verified successfully!")
                    await interaction.response.send_message(content="One second, verifying you...", ephemeral=True)
                    try:
                        role = server.get_role(verifiedroleid)
                        await interaction.user.add_roles(role)
                    except Exception:
                        print(f"{formatUsername(interaction.user)} attempted to verify and errored, error logs:")
                        traceback.print_exc()
                        await interaction.edit_original_response(content="Failed to verify! Please report this error to @etangaming123.")
                else:
                    await interaction.response.send_message(content="That doesn't seem to be the right emoji, try again.", ephemeral=True)
                        
            class TheOtherVerifyButtons(discord.ui.View): # select the ghost: [emoji] [emoji] [emoji] idk
                @discord.ui.button(label=usedemojilist[0], style=discord.ButtonStyle.blurple) # literally just copy the buttons 5 times
                async def thefirstbutton(self, interaction, button):
                    await nowayitsabutton(self, interaction, button, 0)
                
                @discord.ui.button(label=usedemojilist[1], style=discord.ButtonStyle.blurple)
                async def thesecondbutton(self, interaction, button):
                    await nowayitsabutton(self, interaction, button, 1)

                @discord.ui.button(label=usedemojilist[2], style=discord.ButtonStyle.blurple)
                async def thethirdbutton(self, interaction, button):
                    await nowayitsabutton(self, interaction, button, 2)

                @discord.ui.button(label=usedemojilist[3], style=discord.ButtonStyle.blurple)
                async def thefourthbutton(self, interaction, button):
                    await nowayitsabutton(self, interaction, button, 3)

                @discord.ui.button(label=usedemojilist[4], style=discord.ButtonStyle.blurple)
                async def thefifthbutton(self, interaction, button):
                    await nowayitsabutton(self, interaction, button, 4)

            await interaction.response.send_message(content=f"Click the [{realemoji}] to verify!", ephemeral=True, view=TheOtherVerifyButtons())
    messages = [message async for message in verificationchannel.history(limit=2)]
    if len(messages) != 0:
        await messages[0].delete() # delete the old verify message 
    await verificationchannel.send(content="Click the verify button to gain access to the server!", view=ConfirmButtonVerify())
        
# --roblox--
def getDiscordUserID(robloxid): # gets the discord user id that is linked to a roblox account
    print(f"Getting Discord ID from Roblox ID [{robloxid}]...")
    url = f"https://apis.roblox.com/cloud/v2/universes/{robloxgameid}/data-stores/DiscordDatastore/entries?id={robloxid}"
    headers = {"x-api-key": robloxapikey}
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if robloxid in data.keys():
            return data[robloxid] # return data if it succeeds
        else:
            return "" # return empty string if nothing exists
    else:
        print(f"Failed to get Discord ID for Roblox id {robloxid} // {response.json()}")
        return False # return false if something fails

def setDiscordUserID(robloxid, discordid): # sets the discord user id for a roblox account
    print(f"Setting Roblox ID {robloxid} to Discord ID {discordid}")
    url = f"https://apis.roblox.com/cloud/v2/universes/{robloxgameid}/data-stores/DiscordDatastore/entries?id={robloxid}"
    headers = {"x-api-key": robloxapikey}
    payload = {
        "value": str(discordid)
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        olddata = loadData("linkedrobloxaccounts")
        if olddata == "":
            return False # return false if this fails
        olddata[discordid] = {"RobloxID": robloxid, "Verified": False, "Supporter": False} # Don't you want me like I want you, baby? (i was bored ok)
        return saveData("linkedrobloxaccounts", olddata) # this function returns true if it succeeds
    else:
        print(f"Failed to link Roblox {robloxid} with {discordid} // {response.json()}")
        return False

def getVerificationStatus(robloxid): # checks if user has entered katsune verification place and hit "verify"
    print(f"Getting verification status for {robloxid}")
    url = f"https://apis.roblox.com/cloud/v2/universes/{robloxgameid}/data-stores/IsVerifiedDatastore/entries?id={robloxid}"
    headers = {"x-api-key": robloxapikey}
    response = requests.get(url, headers=headers)
    if response.status_code == 200: # it doesn't matter what the value is, as long as the value is set (value as in the datastore entry)
        return True
    else:
        print(f"Failed to get verification status for {robloxid} // {response.json()}")
        return False

def unlinkUser(discordid, robloxid): # self explanatory (also returns true if succeeds, false if fails)
    print(f"Unlinking Roblox ID {robloxid} and Discord ID {discordid}")
    url = f"https://apis.roblox.com/cloud/v2/universes/{robloxgameid}/data-stores/DiscordDatastore/entries/{robloxid}"
    url2 = f"https://apis.roblox.com/cloud/v2/universes/{robloxgameid}/data-stores/IsVerifiedDatastore/entries/{robloxid}"
    headers = {"x-api-key": robloxapikey}

    response1 = requests.delete(url=url, headers=headers)
    response2 = requests.delete(url=url2, headers=headers)

    if response1.status_code == 200 or response1.status_code == 404 and response2.status_code == 200 or response2.status_code == 404: # not found requests are ignored, as they are already deleted according to roblox's documentation
        olddata = loadData("linkedrobloxaccounts")
        if olddata == "":
            return False
        del olddata[discordid]
        return saveData("linkedrobloxaccounts", olddata)
    else:
        print(f"Failed to unlinklink Roblox {robloxid} with {discordid} // Response 1 {response1.json()} // Response 2 {response2.json()}")
        return False

def getRobloxDetails(username: str): # gets details of a roblox account
    print(f"Getting Roblox details of Roblox username {username}")
    url = "https://users.roblox.com/v1/usernames/users"
    
    payload = {
        "excludeBannedUsers": False,
        "usernames": [username]
    }
    headers = {
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        jsonload = json.loads(response.text)
        data = jsonload.get("data")
        if data == []:
            print("User does not exist on Roblox.")
            return "NonExistant"
        return {"UserID": data[0]["id"], "Username": data[0]["name"], "DisplayName": data[0]["displayName"]}
    except Exception:
        traceback.print_exc()
        return "Error"

# [ events ]
@bot.event
async def on_ready():
    global server
    global verificationchannel
    print("Syncing commands...")
    await bot.tree.sync() # this syncs slash commands to server
    print("Changing RPC...")
    await changerpc("Roblox [Ghost Hunt]")
    print("Setting up variables...")
    server = await bot.fetch_guild(serverid) # there we go !
    verificationchannel = bot.get_channel(verificationchannelid)
    print("Sending verification system...")
    await sendVerificationSystem()
    print("Bot is ready!")

@bot.event
async def on_member_join(member):
    await sendwelcome(member.mention)

@bot.event
async def on_member_leave(member):
    await sendbye(member.mention)

# [ slash commands + others ]
# --roblox--
@bot.tree.command(name="roblox-link-step-1", description="Verify your Roblox account with Discord! (Step 1)")
@app_commands.describe(username="Your Roblox username")
async def verifystep1(interaction: discord.Interaction, username: str):
    print(f"{formatUsername(interaction.user)} executed /roblox-link-step-1")
    await interaction.response.send_message(content=f"# >> Katsune Verification <<\n\> Getting details...", ephemeral=True)
    try:
        data = loadData("linkedrobloxaccounts")
        if data == "": # if data is empty something went wrong
            await interaction.edit_original_response(content=f"# >> Katsune Verification <<\n\-Getting details...\n\> Failed to read internal data! Please try again.")
            return
        if interaction.user.id in data.keys(): # check if user is already linked
            await interaction.edit_original_response(content=f"# >> Katsune Verification <<\n\-Getting details...\n\> Your account is already linked! Join [this Roblox game](https://www.roblox.com/games/140030248253073/Katsune-Verification-Place) to continue verification, or run /unlink-roblox to change your Roblox user!")
            return
        userinfo = getRobloxDetails(username)
        await interaction.edit_original_response(content=f"# >> Katsune Verification <<\n\-Getting details...\n\> Getting info of {username}...")
        if userinfo == "NonExistant":
            await interaction.edit_original_response(content=f"# >> Katsune Verification <<\n\-Getting details...\n\- Getting info of {username}...\n\> Failed to get details of {username}! Does the user exist?")
            return
        if userinfo == "Error":
            await interaction.edit_original_response(content=f"# >> Katsune Verification <<\n\-Getting details...\n\- Getting info of {username}...\n\> Failed to get details of {username}! Please try again.")
            return
        class ConfirmButtonVerify(discord.ui.View): # literally the verify button
            @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
            async def confirmbuttonverify(self, interaction, button):
                await interaction.response.send_message(content=f"# >> Katsune Verification <<\n\> Linking your account with {userinfo['Username']}...", ephemeral=True)
                if not setDiscordUserID(userinfo["UserID"], interaction.user.id):
                    await interaction.edit_original_response(content=f"# >> Katsune Verification <<\n\- Linking your account with {userinfo['Username']}...\n\> Failed to link your account! Please try again.")
                    return
                await interaction.edit_original_response(content=f"# >> Katsune Verification <<\n\- Linking your account with {userinfo['Username']}...\n\> Successfully linked! Join [this Roblox game](https://www.roblox.com/games/140030248253073/Katsune-Verification-Place) to continue verification, then run /roblox-link-step-2 on Discord to finish verifying!")
        thing = getDiscordUserID(userinfo["UserID"])
        if thing == "": # this is good, we want this
            await interaction.edit_original_response(content=f"# >> Katsune Verification <<\n\-Getting details...\n\- Getting info of {username}...\n\- Details:\n-- UserID: {userinfo['UserID']}\n-- Username: {userinfo['Username']}\n-- Displayname: {userinfo['DisplayName']}\n\> Click the button below if the account is correct.", view=ConfirmButtonVerify())
        elif thing == False: # uh no
            await interaction.edit_original_response(content=f"# >> Katsune Verification <<\n\-Getting details...\n\- Getting info of {username}...\n\> Something went wrong while trying to get verification info.")
        else: # already linked
            await interaction.edit_original_response(content=f"# >> Katsune Verification <<\n\-Getting details...\n\- Getting info of {username}...\n\> Your Roblox user has already been linked to Discord! To change this, run /unlink-roblox and relink your account.")
    except Exception:
        print(f"{formatUsername(interaction.user)} executed /roblox-link-step-1 and errored, error logs:")
        traceback.print_exc()
        await interaction.edit_original_response(content=f"# >> Katsune Verification <<\n[ FATAL ERROR OCCURED ]\nUh oh!\nThis error was not accounted for within Katsune's source code.\n\nPlease screenshot this and report this to etangaming123.")

@bot.tree.command(name="roblox-link-step-2", description="Verify your Roblox account with Discord! (Step 2)")
async def verifystep2(interaction: discord.Interaction):
    print(f"{formatUsername(interaction.user)} executed /roblox-link-step-2")
    await interaction.response.send_message(content="# >> Katsune Verification <<\n\> Confirming verification...", ephemeral=True)
    try:
        data = loadData("linkedrobloxaccounts")
        if data == "": # internal data failed
            await interaction.edit_original_response(content="# >> Katsune Verification <<\n\- Confirming verification...\n\> An error occured while loading internal data.")
            return
        if not interaction.user.id in data.keys(): # user has not ran step 1 verification
            await interaction.edit_original_response(content="# >> Katsune Verification <<\n\- Confirming verification...\n\> Your Roblox user has not been linked! Run /roblox-link-step-1, then rerun this command.")
            return
        if not getVerificationStatus(data[interaction.user.id]): # check if user has joined katsune verification place
            await interaction.edit_original_response(content="# >> Katsune Verification <<\n\- Confirming verification...\n\> An error occured while loading verification data. Have you joined [this Roblox game](https://www.roblox.com/games/140030248253073/Katsune-Verification-Place)?")
            return
        data[interaction.user.id]["Verified"] = True
        if not saveData("linkedrobloxaccounts", data): # uh oh data saving failed
            await interaction.edit_original_response(content="# >> Katsune Verification <<\n\- Confirming verification...\n\> An error occured while saving internal data.")
            return
        await interaction.edit_original_response(content="# >> Katsune Verification <<\n\- Confirming verification...\n\> Successfully confirmed verification! Thank you! :3")
    except Exception:
        print(f"{formatUsername(interaction.user)} executed /roblox-link-step-2 and errored, error logs:")
        traceback.print_exc()
        await interaction.edit_original_response(content=f"# >> Katsune Verification <<\n[ FATAL ERROR OCCURED ]\nUh oh!\nThis error was not accounted for within Katsune's source code.\n\nPlease screenshot this and report this to etangaming123.")

@bot.tree.command(name="unlink-roblox", description="Unlinks your Roblox account with Discord!")
async def unlinkroblox(interaction: discord.Interaction):
    print(f"{formatUsername(interaction.user)} executed /unlink-roblox")
    await interaction.response.send_message(content="# >> Katsune Verification <<\n\> Unlinking your Roblox account...", ephemeral=True)
    try:
        data = loadData("linkedrobloxaccounts")
        if data == "":
            await interaction.edit_original_response(content="# >> Katsune Verification <<\n\- Unlinking your Roblox account...\n\> An error occured while loading internal data.")
        else:
            if interaction.user.id in data.keys():
                if unlinkUser(interaction.user.id, data[interaction.user.id]["RobloxID"]): # this function deletes internal (.pkl) data
                    await interaction.edit_original_response(content="# >> Katsune Verification <<\n\- Unlinking your Roblox account...\n\> Unlinked your Roblox account!")
                else:
                    await interaction.edit_original_response(content="# >> Katsune Verification <<\n\- Unlinking your Roblox account...\n\> An error occured while unlinking your account.")
    except Exception:
        print(f"{formatUsername(interaction.user)} executed /unlink-roblox and errored, error logs:")
        traceback.print_exc()
        await interaction.edit_original_response(content=f"# >> Katsune Verification <<\n[ FATAL ERROR OCCURED ]\nUh oh!\nThis error was not accounted for within Katsune's source code.\n\nPlease screenshot this and report this to etangaming123.")

# --conversation starters--
@bot.tree.command(name="conversation-starter", description="Get a conversation starter!")
async def getConversationStarter(interaction: discord.Interaction):
    print(f"{formatUsername(interaction.user)} executed /conversation-starter")
    await interaction.response.send_message(content="# >> Conversation Starters <<\n\> Getting random conversation starter...")
    try:
        data = loadData("conversationstarters")
        if data == "":
            await interaction.edit_original_response(content="# >> Conversation Starters <<\n\- Getting random conversation starter...\> An error occured while reading internal data.")
            return
        number = random.randint(1, len(data) - 1) # pick random
        await interaction.edit_original_response(content=f"# >> Conversation Starters <<\n\- Getting random conversation starter...\n\> \"{data[str(number)]}\" (ID: {str(number)})")
    except Exception:
        print(f"{formatUsername(interaction.user)} executed /conversation-starter and errored, error logs:")
        traceback.print_exc()
        await interaction.edit_original_response(content=f"# >> Conversation Starters <<\n[ FATAL ERROR OCCURED ]\nUh oh!\nThis error was not accounted for within Katsune's source code.\n\nPlease screenshot this and report this to etangaming123.")

@bot.tree.command(name="add-conversation-starter", description="[ONLY AVALIABLE TO ADMINS AND ABOVE] Adds a conversation starter!")
@app_commands.describe(conversation_starter="The conversation starter to add")
async def addConversationStarter(interaction: discord.Interaction, conversation_starter: str):
    print(f"{formatUsername(interaction.user)} executed /add-conversation-starter")
    haspermissions = False
    for role in interaction.user.roles:
        if role.id in adminroleids:
            haspermissions = True
    if not haspermissions:
        await interaction.response.send_message(content="# >> Conversation Starters <<\n\> You do not have permission to use this command!", ephemeral=True)
        return
    class ConfirmButtonConversationStarter(discord.ui.View):
        @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
        async def confirmbuttonconversationstarter(self, interaction, button):
            await interaction.response.send_message(content=f"# >> Conversation Starters <<\n\> Adding conversation starter \"{conversation_starter}\"...", ephemeral=True)
            try:
                conversationstarterdata = loadData("conversationstarters")
                if conversationstarterdata == "":
                    await interaction.edit_original_response(content=f"# >> Conversation Starters <<\n\- Adding conversation starter \"{conversation_starter}\"...\n\> An internal error occured while getting data.")
                    return
                conversation_starter_id = len(conversationstarterdata) + 1
                conversationstarterdata[str(conversation_starter_id)] = conversation_starter
                if saveData("conversationstarters", conversationstarterdata):
                    await interaction.edit_original_response(content=f"# >> Conversation Starters <<\n\- Adding conversation starter \"{conversation_starter}\"...\n\> Added conversation starter with id {str(conversation_starter_id)}")
                else:
                    await interaction.edit_original_response(content=f"# >> Conversation Starters <<\n\- Adding conversation starter \"{conversation_starter}\"...\n\> An internal error occured while saving data.")
            except Exception:
                print(f"{formatUsername(interaction.user)} clicked button Confirm in /add-conversation-starter and errored, error logs:")
                traceback.print_exc()
                await interaction.edit_original_response(content=f"# >> Conversation Starters <<\n[ FATAL ERROR OCCURED ]\nUh oh!\nThis error was not accounted for within Katsune's source code.\n\nPlease screenshot this and report this to etangaming123.")
    await interaction.response.send_message(content=f"# >> Conversation Starters <<\n\> Are you sure you wish to add the following conversation starter?\n\> \"{conversation_starter}\"", ephemeral=True, view=ConfirmButtonConversationStarter())

@bot.tree.command(name="delete-conversation-starter", description="[ONLY AVALIABLE TO ADMINS AND ABOVE] Deletes a conversation starter!")
@app_commands.describe(conversation_starter_id="The conversation starter to delete (MUST BE AN ID)")
async def addConversationStarter(interaction: discord.Interaction, conversation_starter_id: int):
    print(f"{formatUsername(interaction.user)} executed /delete-conversation-starter")
    haspermissions = False
    for role in interaction.user.roles:
        if role.id in adminroleids:
            haspermissions = True
    if not haspermissions:
        await interaction.response.send_message(content="# >> Conversation Starters <<\n\> You do not have permission to use this command!", ephemeral=True)
        return
    await interaction.response.send_message(content=f"# >> Conversation Starters <<\n\> Finding converstaion starter with ID {conversation_starter_id}", ephemeral=True)
    try:
        conversationstarterdata = loadData("conversationstarters")
        if conversationstarterdata == "":
            await interaction.edit_original_response(content=f"# >> Conversation Starters <<\n\- Finding conversation starter with ID {conversation_starter_id}\n\> Failed to load internal data!")
            return
        if not conversation_starter_id in conversationstarterdata.keys():
            await interaction.edit_original_response(content=f"# >> Conversation Starters <<\n\- Finding conversation starter with ID {conversation_starter_id}\n\> Conversation starter ID {conversation_starter_id} does not exist!")
            return
        conversation_starter = conversationstarterdata[str(conversation_starter_id)]
        class ConfirmButtonDeleteConversationStarter(discord.ui.view):
            @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
            async def confirmbuttonconversationstarter(self, interaction, button):
                await interaction.response.send_message(content=f"# >> Conversation Starters <<\n\> Deleting conversation starter \"{conversation_starter}\"...", ephemeral=True)
                try:
                    conversationstarterdata = loadData("conversationstarters")
                    if conversationstarterdata == "":
                        await interaction.edit_original_response(content=f"# >> Conversation Starters <<\n\- Deleting conversation starter \"{conversation_starter}\"...\n\> An internal error occured while getting data.")
                        return
                    del conversationstarterdata[str(conversation_starter_id)]
                    if saveData("conversationstarters", conversationstarterdata):
                        await interaction.edit_original_response(content=f"# >> Conversation Starters <<\n\- Deleting conversation starter \"{conversation_starter}\"...\n\> Deleted conversation starter with id {str(conversation_starter_id)}")
                    else:
                        await interaction.edit_original_response(content=f"# >> Conversation Starters <<\n\- Deleting conversation starter \"{conversation_starter}\"...\n\> An internal error occured while saving data.")
                except Exception:
                    print(f"{formatUsername(interaction.user)} clicked button Confirm in /add-conversation-starter and errored, error logs:")
                    traceback.print_exc()
                    await interaction.edit_original_response(content=f"# >> Conversation Starters <<\n[ FATAL ERROR OCCURED ]\nUh oh!\nThis error was not accounted for within Katsune's source code.\n\nPlease screenshot this and report this to etangaming123.")
        await interaction.edit_original_response(content=f"# >> Conversation Starters <<\n\- Finding conversation starter with ID {conversation_starter_id}\n\> Are you sure you want to delete the following conversation starter?\n\> \"{conversation_starter}\"", view=ConfirmButtonDeleteConversationStarter())
    except Exception:
        await interaction.edit_original_response(content=f"# >> Conversation Starters <<\n[ FATAL ERROR OCCURED ]\nUh oh!\nThis error was not accounted for within Katsune's source code.\n\nPlease screenshot this and report this to etangaming123.")

# --anonymous messages--
# anon messages do not have print() functions as to maximise well anonymous something
class AnonForm(discord.ui.Modal, title='Anonymous Message Form'): # this isn't a slash command but ok !
    message = discord.ui.TextInput(
        label='Your message',
        style=discord.TextStyle.long,
        placeholder='This message will be sent anonymously.',
        required=True,
        max_length=2000,
    )

    attachment = discord.ui.TextInput(
        label='Attachents',
        placeholder='Add an optional image link here.',
        required=False
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'\> Saving data and posting to channel...', ephemeral=True)
        anonmessages = loadData("anonymousmessages")
        if anonmessages == "":
            await interaction.edit_original_response(content="\- Saving data and posting to channel...\n\> Failed to load anonymous message data! Please report this error to @etangaming123.")
        try:
            anonchannel = await bot.fetch_channel(anonchannelid)
            internalanonid = len(anonmessages) + 1
            message = str(self.message)
            if self.attachment == "" or self.attachment == None:
                anonmessages[internalanonid] = {"UserID": interaction.user.id, "Message": message, "Attachment": ""}
                anonembed = discord.Embed(title="Anonymous message", description=self.message)
            else:
                anonmessages[internalanonid] = {"UserID": interaction.user.id, "Message": message, "Attachment": str(self.attachment)}
                anonembed = discord.Embed(title="Anonymous message", description=message)
                anonembed.set_image(url=str(self.attachment))
            if saveData("anonymousmessages", anonmessages):
                anonembed.set_footer(text=f"If this anonymous message breaks the rules, please run /manage-anon {internalanonid} and click \"report\".")
                message = await anonchannel.send(embed=anonembed)
                anonmessages[internalanonid]["MessageID"] = message.id
                saveData("anonymousmessages", anonmessages)
            else:
                await interaction.edit_original_response(content="\- Saving data and posting to channel...\n\> Failed to save anonymous message data! Please report this error to @etangaming123.")
        except Exception:
            traceback.print_exc()
            await interaction.edit_original_response(content="\- Saving data and posting to channel...\n\> An unaccounted error occured! Please report this error to @etangaming123.")

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('\- Saving data and posting to channel...\n\> Something went wrong whist trying to submit your anonymous message. Please report this error to @etangaming123.', ephemeral=True)
        traceback.print_exception(type(error), error, error.__traceback__)

@bot.tree.command(name="send-anon", description="Sends an anonymous message!")
async def sendanonymousmessage(interaction: discord.Interaction):
    banneduserlist = loadData("bannedanons")
    if banneduserlist == "":
        await interaction.response.send_message("Failed to get banned user list, please try again!", ephemeral=True)
        return
    if interaction.user.id in banneduserlist:
        await interaction.response.send_message("You are banned from using this command, sorry!", ephemeral=True)
        return
    anonmessagedata = loadData("anonymousmessages")
    if anonmessagedata == "":
        await interaction.response.send_message("Something went wrong while trying to load anonymous message data. please try again!", ephemeral=True)
        return
    await interaction.response.send_modal(AnonForm())

@bot.tree.command(name="manage-anon", description="Can be used to report an anonymous message, or deleting if it's your message.")
@app_commands.describe(id="The ID of the anonymous message to manage.")
async def manageanonymousmessage(interaction: discord.Interaction, id: int):
    await interaction.response.send_message("# >> Anon Messaging <<\n\> One second, getting anon message data...", ephemeral=True)
    anonmessagedata = loadData("anonymousmessages")
    if anonmessagedata == "":
        await interaction.edit_original_response(content="# >> Anon Messaging <<\n\- One second, getting anon message data...\n\> Failed to load anon message data! Please report this error to @etangaming123.")
        return
    if not id in anonmessagedata.keys():
        await interaction.edit_original_response(content="# >> Anon Messaging <<\n\- One second, getting anon message data...\n\> That anonymous message does not exist!")
        return
    isyourself = anonmessagedata[id]["UserID"] == interaction.user.id # if the user running the command is the same person as the poster of the message idk 
    isadmin = False
    if not isyourself: # intentional
        for item in interaction.user.roles:
            if item.id in adminroleids:
                isadmin = True
                break
    
    async def reportAnonMessage(interaction, message, id):
        loggingchannel = await bot.fetch_channel(katsunelogid)
        reportEmbed = discord.Embed(title=f"Report by {formatUsername(interaction.user)}", description=f"The user has reported an anonymous message with the following content:\n\n\"{message}\"")
        reportEmbed.set_footer(text=f"The image for this anon message, if any, was removed. If this report is genuine, run /manage-anon {id} and either delete the message or ban the user from making anonymous messages.")
        await loggingchannel.send(embed=reportEmbed)
        await interaction.response.send_message("Report submitted! Thanks for making Ghost Hunt a better place :3", ephemeral=True) # :3

    async def banAnonUser(interaction, anondata):
        bannedusers = loadData("bannedanons")
        if bannedusers == "":
            await interaction.response.send_message("Failed to load banned anons! Please try again.", ephemeral=True)
            return
        bannedusers[anondata["UserID"]] = interaction.user.id # {userthatwasbanned: userthatbannedtheuserthatwasbanned}
        if saveData("bannedanons", bannedusers):
            await interaction.response.send_message("Banned anon user sucessfully!", ephemeral=True)
            return
        await interaction.response.send_message("Failed to save banned anons! Please try again.", ephemeral=True)
        
    async def unbanAnonUser(interaction, anondata):
        bannedusers = loadData("bannedanons")
        if bannedusers == "":
            await interaction.response.send_message("Failed to load banned anons! Please try again.", ephemeral=True)
            return
        if anondata["UserID"] in bannedusers.keys():
            del bannedusers[anondata["UserID"]]
            if saveData("bannedanons", bannedusers):
                await interaction.response.send_message("Unbanned anon user sucessfully!", ephemeral=True)
                return
            await interaction.response.send_message("Failed to save banned anons! Please try again.", ephemeral=True)
        await interaction.response.send_message("This user was never banned in the first place, nothing changed.", ephemeral=True)

    async def deleteAnonMessage(interaction, anonmessageid): 
        anonchannel = await bot.fetch_channel(anonchannelid)
        message = await anonchannel.fetch_message(anonmessageid)
        await bot.delete_message(message)
        await interaction.response.send_message("Deleted that message!", ephemeral=True)

    if isyourself:
        class manageAnonMessageYourself(discord.ui.View):
            @discord.ui.button(label="Delete", style=discord.ButtonStyle.red)
            async def deleteanon(self, interaction, button):
                await deleteAnonMessage(interaction, anonmessagedata[id]["MessageID"])
        await interaction.edit_original_response(content=f"# >> Anon Messaging <<\n\- One second, getting anon message data...\n\> Please select an option below for confession {id}.\n-# Since you're the poster of this anonymous message, you can choose to delete it!", view=manageAnonMessageYourself())
        return

    if isadmin:
        class manageAnonMessageAdmin(discord.ui.View):
            @discord.ui.button(label="Report", style=discord.ButtonStyle.red)
            async def reportanon(self, interaction, button):
                await reportAnonMessage(interaction, anonmessagedata[id]["Message"], id)
            @discord.ui.button(label="Ban from anon messages", style=discord.ButtonStyle.red)
            async def bananon(self, interaction, button): # banananaananananananananananananananaanananananananaananananananananananaan
                await banAnonUser(interaction, anonmessagedata[id])
            @discord.ui.button(label="Unban from anon messages", style=discord.ButtonStyle.green)
            async def unbananon(self, interaction, button):
                await unbanAnonUser(interaction, anonmessagedata[id])
        await interaction.edit_original_response(content=f"# >> Anon Messaging <<\n\- One second, getting anon message data...\n\> Please select an option below for confession {id}.\n-# Since you're an admin, you can ban the user who posted the message from posting more anonymous messages!", view=manageAnonMessageAdmin())
        return

    class manageAnonMessage(discord.ui.View): # one button.
        @discord.ui.button(label="Report", style=discord.ButtonStyle.red)
        async def reportanon(self, interaction, button):
            await reportAnonMessage(interaction, anonmessagedata[id]["Message"], id)
    await interaction.edit_original_response(content=f"# >> Anon Messaging <<\n\- One second, getting anon message data...\n\> Please select an option below for confession {id}.", view=manageAnonMessage())

# --good noodles--
@bot.tree.command(name="my-good-noodles", description="See how many good noodles you have!")
async def getGoodNoodles(interaction: discord.Interaction):
    await interaction.response.send_message("# >> Good Noodles <<\n\> Getting good noodle data...", ephemeral=True)
    goodnoodledata = loadData("goodnoodles")
    if goodnoodledata == "":
        await interaction.edit_original_response(content="# >> Good Noodles <<\n\- Getting good noodle data...\n\> Failed to load good noodle data!")
        return
    if not interaction.user.id in goodnoodledata.keys():
        goodnoodledata[interaction.user.id] = 0
        saveData("goodnoodles", goodnoodledata)
    await interaction.edit_original_response(content=f"# >> Good Noodles <<\n\- Getting good noodle data...\n\> You have {goodnoodledata[interaction.user.id]} good noodles ⭐!")

@bot.tree.command(name="view-good-noodles", description="See how many good noodles a user has!")
@app_commands.describe(user="The user to view good noodles of")
async def viewGoodNoodles(interaction: discord.Interaction, user: discord.User):
    await interaction.response.send_message("# >> Good Noodles <<\n\> Getting good noodle data...", ephemeral=True)
    goodnoodledata = loadData("goodnoodles")
    if goodnoodledata == "":
        await interaction.edit_original_response(content="# >> Good Noodles <<\n\- Getting good noodle data...\n\> Failed to load good noodle data!")
        return
    if not user.id in goodnoodledata.keys():
        goodnoodledata[user.id] = 0
        saveData("goodnoodles", goodnoodledata)
    await interaction.edit_original_response(content=f"# >> Good Noodles <<\n\- Getting good noodle data...\n\> {formatUsername(user)} has {goodnoodledata[user.id]} good noodles ⭐!")

@bot.tree.command(name="good-noodle-leaderboard", description="Shows the good noodle leaderboard! (top 10 users)")
async def goodNoodleLeaderboard(interaction: discord.Interaction):
    await interaction.response.send_message("# >> Good Noodles <<\n\> One second, getting good noodles...", ephemeral=True)
    try:
        goodNoodleData = loadData("goodnoodles")
        if goodNoodleData == "":
            await interaction.edit_original_response(content="# >> Good Noodles <<\n\- One second, getting good noodles...\n\> Failed to load good noodle data!") 
        sorteddata = dict(sorted(goodNoodleData.items(), key=lambda item: item[1], reverse=True)[:10])
        leaderboard = ""
        for item in sorteddata.keys():
            try:
                user = formatUsername(bot.get_user(item))
            except Exception:
                user = f"Unknown User (ID {item})"
            leaderboard += f"\n\> {user} - {str(sorteddata[item])} ⭐"
        await interaction.edit_original_response(content=f"# >> Good Noodles <<\n\- One second, getting good noodles...\n\> Good noodle leaderboard:\n{leaderboard}")
    except Exception:
        print(f"{formatUsername(interaction.user)} executed /good-noodle-leaderboard and errored, error logs:")
        traceback.print_exc()
        await interaction.edit_original_response(content="# >> Good Noodles <<\n[ FATAL ERROR OCCURED ]\nUh oh!\nThis error was not accounted for within Katsune's source code.\n\nPlease screenshot this and report this to etangaming123.")

@bot.tree.command(name="add-good-noodle", description="[ONLY AVALIABLE TO CATULUS] Adds good noodles to a user!")
@app_commands.describe(user="The user to add good noodles to", amount="The amount of good noodles to add (can be negative to subtract)")
async def addGoodNoodle(interaction: discord.Interaction, user: discord.User, amount: int):
    if not interaction.user.id in powerusers:
        await interaction.response.send_message(content="# >> Good Noodles <<\n\> You do not have permission to use this command!", ephemeral=True)
        return
    gaverole = "Nah"
    await interaction.response.send_message(f"# >> Good Noodles <<\n\> Adding {str(amount)} good noodles to {formatUsername(user)}...", ephemeral=True)
    try:
        goodnoodledata = loadData("goodnoodles")
        if goodnoodledata == "":
            await interaction.edit_original_response(content="# >> Good Noodles <<\n\- Adding good noodles...\n\> Failed to load good noodle data!")
            return
        if not user.id in goodnoodledata.keys():
            goodnoodledata[user.id] = 0
        goodnoodledata[user.id] += amount
        if goodnoodledata[user.id] < 0: # if the amount is negative, set it to 0
            goodnoodledata[user.id] = 0
        if goodnoodledata[user.id] > 0: # if the amount is more than 0, give user good noodle role
            try:
                role = server.get_role(goodnoodleroleid)
                await user.add_roles(role)
                gaverole = "Yeah"
            except Exception:
                gaverole = "Errored"
        if saveData("goodnoodles", goodnoodledata):
            if gaverole == "Errored":
                await interaction.edit_original_response(content=f"# >> Good Noodles <<\n\- Adding good noodles...\n\> Added {str(amount)} good noodles to {formatUsername(user)}, they now have {goodnoodledata[user.id]} ⭐!\n\> Failed to give user good noodle role, please do it manually.")
                return
            if gaverole == "Yeah":
                await interaction.edit_original_response(content=f"# >> Good Noodles <<\n\- Adding good noodles...\n\> Added {str(amount)} good noodles to {formatUsername(user)}, they now have {goodnoodledata[user.id]} ⭐!\n\> Gave user good noodle role!")
                return
            await interaction.edit_original_response(content=f"# >> Good Noodles <<\n\- Adding good noodles...\n\> Added {str(amount)} good noodles to {formatUsername(user)}, they now have {goodnoodledata[user.id]} ⭐!")
        else:
            await interaction.edit_original_response(content="# >> Good Noodles <<\n\- Adding good noodles...\n\> Failed to save good noodle data!")
    except Exception:
        print(f"{formatUsername(interaction.user)} executed /add-good-noodle and errored, error logs:")
        traceback.print_exc()
        await interaction.edit_original_response(content=f"# >> Good Noodles <<\n[ FATAL ERROR OCCURED ]\nUh oh!\nThis error was not accounted for within Katsune's source code.\n\nPlease screenshot this and report this to etangaming123.")

# --katsuprofiles--
# TODO: create katsuprofiles :P

# --fun--
@bot.tree.command(name="random-number", description="Picks a random number from 1 to your choice!")
@app_commands.describe(maxnumber="The maximum number the bot can pick")
async def randomNumber(interaction: discord.Interaction, maxnumber: int):
    await interaction.response.send_message(f"Your random number is {str(random.randint(1, maxnumber))}\n-# Number picked from 1 to {str(maxnumber)}")

@bot.tree.command(name="change-status", description="Changes the status of the Katsune bot! Only avaliable to etangaming123 and _catulus.")
@app_commands.describe(state="Playing [state]")
async def changestatus(interaction: discord.Interaction, state: str):
    if interaction.user.id in powerusers:
        print(f"{formatUsername(interaction.user)} executed /change-status")
        try:
            await changerpc(state)
            await interaction.response.send_message(f"Changed status to {state}", ephemeral=True)
        except Exception:
            print(f"{formatUsername(interaction.user)} executed /change-status and errored, error logs:")
            traceback.print_exc()
            await interaction.response.send_message("An error occured while changing bot status. Please report this to etangaming123.", ephemeral=True)
        return
    await interaction.response.send_message("You do not have permission to run this command, sorry!", ephemeral=True)

@bot.tree.command(name="say", description="Make the bot say something!")
@app_commands.describe(message="The message to say")
async def say(interaction: discord.Interaction, message: str):
    if interaction.user.id in powerusers:
        print(f"{formatUsername(interaction.user)} executed /say")
        try:
            await interaction.channel.send(message)
            await interaction.response.send_message("Sent!", ephemeral=True)
        except Exception:
            print(f"{formatUsername(interaction.user)} executed /say and errored, error logs:")
            traceback.print_exc()
            await interaction.response.send_message("An error occured while making the bot say something. Please report this to etangaming123.", ephemeral=True)
        return
    await interaction.response.send_message("You do not have permission to run this command, sorry!", ephemeral=True)

bot.run(bottoken) # run.

# [ other information ]
# --commenting symbols--
# protip: use vscode extention "better comments"
# ! - warning (e.g something doesn't work)
# ? - concern (e.g "you sure bro?")
# * - important info (e.g placeholder code)
# TODO: self explanatory
# anything else without a symbol is just information about the code or other comments