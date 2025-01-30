""">> Katsune Source Code <<"""
# i hope you like the comments btw
# [ modules ]
import discord
from discord.ext import commands
from discord import app_commands
import pickle
import random
import traceback
import requests
import json

# [ set information ]
# basically, since i don't want to share the discord bot token and roblox api keys i put them in a separate json
with open("keys.json", "rb") as file:
    sensitivedata = json.load(file)
bottoken = sensitivedata["bottoken"]
robloxapikey = sensitivedata["robloxapikey"]

# [ variables ]
# --data--
defaultkatsuprofile = {"AboutMe": "", "DisplayRoblox": False, "DisplaySupporter": False, "DisplayGoodNoodles": False, "Pfp": "Discord", "DisplayName": "DiscordDisplay", "Name": "DiscordUser"}

# --discord--
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
# OOO is replaced by @user for welcome and leave messages
welcomemessages = ["OOO joined the server! Welcome!", "OOO.Parent = discord.Servers[\"Ghost Hunt (Roblox)\"]", "Another fellow ghost hunter joined us! Welcome OOO!", "OOO joined the asylum, they can never leave!"]
leavemessages = ["We were right, OOO didn't enjoy their stay!", "An unexpected error occurred and OOO needs to quit. We're sorry!", "OOO pressed the leave button on accident", "Shutting down OOO..."]
memberjoinleavechannelid = 1125568412882583552
verificationchannelid = 1129962618346553450
etanuserid = 723053854194663456
catulususerid = 627196747676123146
verifiedroleid = 1129960240922759218
adminroleids = [883261775510921256, 883261098059522078]
emojilist = ["👻", "💸", "💡", "💥", "🍬", "🤖", "🖥️", "🎮"]
ghosthuntserver = None

# --other--
pfpdisplays = ["Discord", "Roblox", "Custom"] # the pfps that can be displayed on katsuprofiles
namedisplays = ["DiscordDisplay", "DiscordUser", "RobloxDisplay", "RobloxUser"] # the names and displaynames that can be displayed on katsuprofiles

# [ functions ]
# --internal--
def saveData(store: str, newdata: dict): # Saves data to a specified .pkl file
    try:
        with open(f"{store}.pkl", "wb") as file:
            pickle.dump(newdata, file)
            return True # Return true if it succeeds
    except Exception:
        traceback.print_exc()
        return False # Otherwise return false

def loadData(store: str): # Gets data from a specified .pkl file
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
            usedemojilist = random.sample(emojilist, 5)
            realemoji = random.sample(usedemojilist, 1)[0]

            async def nowayitsabutton(self, interaction, button, number): # function for a button
                if usedemojilist[number] == realemoji: # no way they verified !!!
                    await interaction.response.send_message(content="One second, verifying you...", ephemeral=True)
                    try:
                        role = ghosthuntserver.get_role(verifiedroleid)
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
    await verificationchannel.send(content="Click the verify button to gain access to the server!", view=ConfirmButtonVerify())

# --roblox--
def getDiscordUserID(robloxid): # gets the discord user id that is linked to a roblox account
    url = f"https://apis.roblox.com/cloud/v2/universes/6869030592/data-stores/DiscordDatastore/entries?id={robloxid}"
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
    print(discordid)
    url = f"https://apis.roblox.com/cloud/v2/universes/6869030592/data-stores/DiscordDatastore/entries?id={robloxid}"
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
    url = f"https://apis.roblox.com/cloud/v2/universes/6869030592/data-stores/IsVerifiedDatastore/entries?id={robloxid}"
    headers = {"x-api-key": robloxapikey}
    response = requests.get(url, headers=headers)
    if response.status_code == 200: # it doesn't matter what the value is, as long as the value is set (value as in the datastore entry)
        return True
    else:
        print(f"Failed to get verification status for {robloxid} // {response.json()}")
        return False

def unlinkUser(discordid, robloxid): # self explanatory (also returns true if succeeds, false if fails)
    url = f"https://apis.roblox.com/cloud/v2/universes/6869030592/data-stores/DiscordDatastore/entries/{robloxid}"
    url2 = f"https://apis.roblox.com/cloud/v2/universes/6869030592/data-stores/IsVerifiedDatastore/entries/{robloxid}"
    headers = {"x-api-key": robloxapikey}

    response1 = requests.delete(url=url, headers=headers)
    response2 = requests.delete(url=url2, headers=headers)

    if response1.status_code == 200 or response1.status_code == 404 and response2.status_code == 200 or response2.status_code == 404: # not found requests are ignored idk how to explain it
        olddata = loadData("linkedrobloxaccounts")
        if olddata == "":
            return False
        del olddata[discordid]
        return saveData("linkedrobloxaccounts", olddata)
    else:
        print(f"Failed to unlinklink Roblox {robloxid} with {discordid} // Response 1 {response1.json()} // Response 2 {response2.json()}")
        return False

def getRobloxDetails(username: str): # gets details of a roblox account
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
    global ghosthuntserver
    global verificationchannel
    print("Syncing commands...")
    await bot.tree.sync() # this syncs slash commands to server
    print("Changing RPC...")
    await changerpc("Roblox [Ghost Hunt]")
    print("Setting up variables...")
    ghosthuntserver = await bot.fetch_guild(883235310580957234)
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

# [ slash commands ]
# --roblox--
@bot.tree.command(name="verify-step-1", description="Verify your Roblox account with Discord! (Step 1)")
@app_commands.describe(username="Your Roblox username")
async def verifystep1(interaction: discord.Interaction, username: str):
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
                await interaction.response.send_message(content=f"# >> Katsune Verification <<\n\> Linking your account with {userinfo["Username"]}...", ephemeral=True)
                if not setDiscordUserID(userinfo["UserID"], interaction.user.id):
                    await interaction.edit_original_response(content=f"# >> Katsune Verification <<\n\- Linking your account with {userinfo["Username"]}...\n\> Failed to link your account! Please try again.")
                    return
                await interaction.edit_original_response(content=f"# >> Katsune Verification <<\n\- Linking your account with {userinfo["Username"]}...\n\> Successfully linked! Join [this Roblox game](https://www.roblox.com/games/140030248253073/Katsune-Verification-Place) to continue verification, then run /verify-step-2 on Discord to finish verifying!")
        thing = getDiscordUserID(userinfo["UserID"])
        if thing == "": # this is good, we want this
            await interaction.edit_original_response(content=f"# >> Katsune Verification <<\n\-Getting details...\n\- Getting info of {username}...\n\- Details:\n-- UserID: {userinfo["UserID"]}\n-- Username: {userinfo["Username"]}\n-- Displayname: {userinfo["DisplayName"]}\n\> Click the button below if the account is correct.", view=ConfirmButtonVerify())
        elif thing == False: # uh no
            await interaction.edit_original_response(content=f"# >> Katsune Verification <<\n\-Getting details...\n\- Getting info of {username}...\n\> Something went wrong while trying to get verification info.")
        else: # already linked
            await interaction.edit_original_response(content=f"# >> Katsune Verification <<\n\-Getting details...\n\- Getting info of {username}...\n\> Your Roblox user has already been linked to Discord! To change this, run /unlink-roblox and relink your account.")
    except Exception:
        print(f"{formatUsername(interaction.user)} executed /verify-step-1 and errored, error logs:")
        traceback.print_exc()
        await interaction.edit_original_response(content=f"# >> Katsune Verification <<\n[ FATAL ERROR OCCURED ]\nUh oh!\nThis error was not accounted for within Katsune's source code.\n\nPlease screenshot this and report this to etangaming123.")

@bot.tree.command(name="verify-step-2", description="Verify your Roblox account with Discord! (Step 2)")
async def verifystep2(interaction: discord.Interaction):
    await interaction.response.send_message(content="# >> Katsune Verification <<\n\> Confirming verification...", ephemeral=True)
    try:
        data = loadData("linkedrobloxaccounts")
        if data == "": # internal data failed
            await interaction.edit_original_response(content="# >> Katsune Verification <<\n\- Confirming verification...\n\> An error occured while loading internal data.")
            return
        if not interaction.user.id in data.keys(): # user has not ran step 1 verification
            await interaction.edit_original_response(content="# >> Katsune Verification <<\n\- Confirming verification...\n\> Your Roblox user has not been linked! Run /verify-step-1, then rerun this command.")
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
        print(f"{formatUsername(interaction.user)} executed /verify-step-2 and errored, error logs:")
        traceback.print_exc()
        await interaction.edit_original_response(content=f"# >> Katsune Verification <<\n[ FATAL ERROR OCCURED ]\nUh oh!\nThis error was not accounted for within Katsune's source code.\n\nPlease screenshot this and report this to etangaming123.")

@bot.tree.command(name="unlink-roblox", description="Unlinks your Roblox account with Discord!")
async def unlinkroblox(interaction: discord.Interaction):
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
    await interaction.response.send_message(content="# >> Conversation Starters <<\n\> Getting random conversation starter...")
    try:
        data = loadData("conversationstarters")
        if data == "":
            await interaction.edit_original_response(content="# >> Conversation Starters <<\n\- Getting random conversation starter...\> An error occured while reading internal data.")
            return
        number = random(0, len(data) - 1)
        await interaction.edit_original_response(content=f"# >> Conversation Starters <<\n\- Getting random conversation starter...\n\> \"{data[str(number)]}\" (ID: {str(number)})")
    except Exception:
        print(f"{formatUsername(interaction.user)} executed /conversation-starter and errored, error logs:")
        traceback.print_exc()
        await interaction.edit_original_response(content=f"# >> Conversation Starters <<\n[ FATAL ERROR OCCURED ]\nUh oh!\nThis error was not accounted for within Katsune's source code.\n\nPlease screenshot this and report this to etangaming123.")

@bot.tree.command(name="add-conversation-starter", description="[ONLY AVALIABLE TO ADMINS AND ABOVE] Adds a conversation starter!")
@app_commands.describe(conversation_starter="The conversation starter to add")
async def addConversationStarter(interaction: discord.Interaction, conversation_starter: str):
    haspermissions = False
    for role in interaction.user.roles:
        if role.id in adminroleids:
            haspermissions = True
    if not haspermissions:
        await interaction.response.send_message(content="# >> Conversation Starters <<\n\> You do not have permission to use this command!", ephemeral=True)
        return
    class ConfirmButtonConversationStarter(discord.ui.view):
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

# --fun--
@bot.tree.command(name="random-number", description="Picks a random number from 1 to your choice!")
@app_commands.describe(maxnumber="The maximum number the bot can pick")
async def randomNumber(interaction: discord.Interaction, maxnumber: int):
    await interaction.response.send_message(f"Your random number is {str(random.randint(1, maxnumber))}\n-# Number picked from 1 to {str(maxnumber)}")

@bot.tree.command(name="change-status", description="Changes the status of the Katsune bot! Only avaliable to etangaming123 and _catulus.")
@app_commands.describe(state="Playing [state]")
async def changestatus(interaction: discord.Interaction, state: str):
    try:
        await changerpc(state)
        await interaction.response.send_message(f"Changed status to {state}!!", ephemeral=True)
    except Exception:
        print(f"{formatUsername(interaction.user)} executed /change-status and errored, error logs:")
        traceback.print_exc()
        await interaction.response.send_message("An error occured while changing bot status. Please report this to etangaming123.", ephemeral=True)

bot.run(bottoken)

# other information
# ! - warning (e.g something doesn't work)
# ? - concern (e.g "you sure bro?")
# * - important info (e.g placeholder code)
# TODO: self explanatory
# anything else without a symbol is just information about the code or other comments