# >> Katsune Source Code <<
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
with open("keys.json", "rb") as file:
    sensitivedata = json.load(file)
bottoken = sensitivedata["bottoken"]
robloxapikey = sensitivedata["robloxapikey"]

# [ variables ]
# --normal--
welcomemessages = ["OOO joined the server! Welcome!", "OOO.Parent = discord.Servers[\"Ghost Hunt (Roblox)\"]", "Another fellow ghost hunter joined us! Welcome OOO!", "OOO joined the asylum, they can never leave!"]
leavemessages = ["We were right, OOO didn't enjoy their stay!", "An unexpected error occurred and OOO needs to quit. We're sorry!", "OOO pressed the leave button on accident", "Shutting down OOO..."]
memberjoinleavechannel = 1125568412882583552

# --other--
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# [ functions ]
# --internal--
def saveData(store, newdata):
    try:
        with open(f"{store}.pkl", "wb") as file:
            pickle.dump(newdata, file)
            return True
    except Exception:
        traceback.print_exc()
        return False

def loadData(store):
    try:
        with open(f"{store}.pkl", "rb") as file:
            return pickle.load(file)
    except Exception:
        traceback.print_exc()
        return ""

def formatUsername(user):
    if user.global_name == None:
        return f"{user.name}"
    else:
        return f"{user.global_name} (@{user.name})"

# --discord--
async def sendwelcome(membermention):
    channel = bot.get_channel(memberjoinleavechannel)
    channel.send(welcomemessages[random.randint(1, len(welcomemessages) - 1)].replace("OOO", membermention))

async def sendbye(membermention):
    channel = bot.get_channel(memberjoinleavechannel)
    channel.send(leavemessages[random.randint(1, len(leavemessages) - 1)].replace("OOO", membermention))

# --roblox--
def getDiscordUserID(robloxid):
    url = f"https://apis.roblox.com/cloud/v2/universes/6869030592/data-stores/DiscordDatastore/entries?id={robloxid}"
    headers = {"x-api-key": robloxapikey}
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if robloxid in data.keys():
            return data[robloxid]
        else:
            return ""
    else:
        print(f"Failed to get Discord ID for Roblox id {robloxid} // {response.json()}")
        return False

def setDiscordUserID(robloxid, discordid):
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
            return False
        olddata[discordid] = {"RobloxID": robloxid, "Verified": False}
        return saveData("linkedrobloxaccounts", olddata)
    else:
        print(f"Failed to link Roblox {robloxid} with {discordid} // {response.json()}")
        return False

def getVerificationStatus(robloxid):
    url = f"https://apis.roblox.com/cloud/v2/universes/6869030592/data-stores/IsVerifiedDatastore/entries?id={robloxid}"
    headers = {"x-api-key": robloxapikey}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return True
    else:
        print(f"Failed to get verification status for {robloxid} // {response.json()}")
        return False

def unlinkUser(discordid, robloxid):
    url = f"https://apis.roblox.com/cloud/v2/universes/6869030592/data-stores/DiscordDatastore/entries/{robloxid}"
    url2 = f"https://apis.roblox.com/cloud/v2/universes/6869030592/data-stores/IsVerifiedDatastore/entries/{robloxid}"
    headers = {"x-api-key": robloxapikey}

    response1 = requests.delete(url=url, headers=headers)
    response2 = requests.delete(url=url2, headers=headers)

    if response1.status_code == 200 or response1.status_code == 404 and response2.status_code == 200 or response2.status_code == 404:
        olddata = loadData("linkedrobloxaccounts")
        if olddata == "":
            return False
        del olddata[discordid]
        return saveData("linkedrobloxaccounts", olddata)
    else:
        print(f"Failed to unlinklink Roblox {robloxid} with {discordid} // Response 1 {response1.json()} // Response 2 {response2.json()}")
        return False

def getRobloxDetails(username: str):
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
    await bot.tree.sync()
    print("Bot is ready!")

@bot.event
async def on_member_join(member):
    await sendwelcome(member.mention)

@bot.event
async def on_member_leave(member):
    await sendbye(member.mention)

# [ commands // roblox verification ]
@bot.tree.command(name="verify-step-1", description="Verify your Roblox account with Discord! (Step 1)")
@app_commands.describe(username="Your Roblox username")
async def verifystep1(interaction: discord.Interaction, username: str):
    await interaction.response.send_message(content=f"# >> Katsune Verification <<\n\> Getting details...", ephemeral=True)
    try:
        data = loadData("linkedrobloxaccounts")
        if data == "":
            await interaction.edit_original_response(content=f"# >> Katsune Verification <<\n\-Getting details...\n\> Failed to read internal data! Please try again.")
            return
        if interaction.user.id in data.keys():
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
        class ConfirmButton(discord.ui.View):
            @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
            async def confirmbutton(self, interaction, button):
                await interaction.response.send_message(content=f"# >> Katsune Verification <<\n\> Linking your account with {userinfo["Username"]}...", ephemeral=True)
                if not setDiscordUserID(userinfo["UserID"], interaction.user.id):
                    await interaction.edit_original_response(content=f"# >> Katsune Verification <<\n\- Linking your account with {userinfo["Username"]}...\n\> Failed to link your account! Please try again.")
                    return
                await interaction.edit_original_response(content=f"# >> Katsune Verification <<\n\- Linking your account with {userinfo["Username"]}...\n\> Successfully linked! Join [this Roblox game](https://www.roblox.com/games/140030248253073/Katsune-Verification-Place) to continue verification, then run /verify-step-2 on Discord to finish verifying!")
        thing = getDiscordUserID(userinfo["UserID"])
        if thing == "":
            await interaction.edit_original_response(content=f"# >> Katsune Verification <<\n\-Getting details...\n\- Getting info of {username}...\n\- Details:\n-- UserID: {userinfo["UserID"]}\n-- Username: {userinfo["Username"]}\n-- Displayname: {userinfo["DisplayName"]}\n\> Click the button below if the account is correct.", view=ConfirmButton())
        elif thing == False:
            await interaction.edit_original_response(content=f"# >> Katsune Verification <<\n\-Getting details...\n\- Getting info of {username}...\n\> Something went wrong while trying to get verification info.")
        else:
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
        if data == "":
            await interaction.edit_original_response(content="# >> Katsune Verification <<\n\- Confirming verification...\n\> An error occured while loading internal data.")
            return
        if not interaction.user.id in data.keys():
            await interaction.edit_original_response(content="# >> Katsune Verification <<\n\- Confirming verification...\n\> An error occured while loading internal data.")
            return
        if not getVerificationStatus(data[interaction.user.id]):
            await interaction.edit_original_response(content="# >> Katsune Verification <<\n\- Confirming verification...\n\> An error occured while loading verification data. Have you joined [this Roblox game](https://www.roblox.com/games/140030248253073/Katsune-Verification-Place)?")
            return
        data[interaction.user.id]["Verified"] = True
        if not saveData("linkedrobloxaccounts", data):
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
                if unlinkUser(interaction.user.id, data[interaction.user.id]["RobloxID"]):
                    await interaction.edit_original_response(content="# >> Katsune Verification <<\n\- Unlinking your Roblox account...\n\> Unlinked your Roblox account!")
                else:
                    await interaction.edit_original_response(content="# >> Katsune Verification <<\n\- Unlinking your Roblox account...\n\> An error occured while unlinking your account.")
    except Exception:
        print(f"{formatUsername(interaction.user)} executed /unlink-roblox and errored, error logs:")
        traceback.print_exc()
        await interaction.edit_original_response(content=f"# >> Katsune Verification <<\n[ FATAL ERROR OCCURED ]\nUh oh!\nThis error was not accounted for within Katsune's source code.\n\nPlease screenshot this and report this to etangaming123.")

bot.run(bottoken)
