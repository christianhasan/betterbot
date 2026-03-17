import asyncio
import json
import sqlite3
import time
from betterbot import InteractionTypes
from betterbot import Types

class Ban:
    con = sqlite3.connect("database.db", check_same_thread=False)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS banlist(user_id TEXT PRIMARY KEY, roles, duration, time_stamp)")
    lock = asyncio.Lock()

    def __init__(self, mod_roles, rest_client, guild, ban_role):
        self.rest_client = rest_client
        self.mod_roles = mod_roles
        self.guild = guild
        self.ban_role = ban_role

    async def _check_mod(self, roles):
        if any(r in self.mod_roles for r in roles):
            return True
        else:
            return False
        
    async def _respond(self, response, token, interaction_id):
        if response != Types.FAILED and response != Types.CONNECTION_FAILED:
            await self.rest_client.send_interaction_callback(interaction_id, token, InteractionTypes.RESPOND_WITH_MESSAGE, content=f"Successfully completed your requested action.")
            return True
        else:
            await self.rest_client.send_interaction_callback(interaction_id, token, InteractionTypes.RESPOND_WITH_MESSAGE, content=f"Oops something went wrong.")
            return False

    async def ban(self, values, interaction_id, roles, token):
        if await self._check_mod(roles):
            user_to_ban = values[0]
            unit = values[1]
            duration = values[2]
            
            payload = await self.rest_client.get_guild_member(self.guild, user_to_ban)
            check_roles = payload.get("roles")

            if check_roles != self.ban_role:
                response = await self.rest_client.member_roles(self.guild, user_to_ban, roles=self.ban_role)

            all_roles = json.dumps(check_roles)

            if await self._respond(response, token, interaction_id):
                if unit == "days": amount = duration*86400
                if unit == "hours": amount = duration*3600
                if unit == "minutes": amount = duration*60
                
                await self.store_banned(user_to_ban, all_roles, duration=amount)
        else:
            await self.rest_client.send_interaction_callback(interaction_id, token, InteractionTypes.RESPOND_WITH_MESSAGE, content="You do not have permission to use that command!")

    async def store_banned(self, user_id, roles, duration):
        async with Ban.lock:
            current_time = time.time()
            Ban.cur.execute("INSERT OR REPLACE INTO banlist VALUES (?,?,?,?)", (user_id, roles, duration, current_time))
            Ban.con.commit()

    async def unban(self, values, roles, token, interaction_id):
        if await self._check_mod(roles):
            user_to_unban = values[0]
            async with Ban.lock:
                Ban.cur.execute("SELECT roles FROM banlist WHERE user_id = ?", (user_to_unban,))
                fetched = Ban.cur.fetchone()

                if fetched is None:
                    await self.rest_client.send_interaction_callback(interaction_id, token, InteractionTypes.RESPOND_WITH_MESSAGE, content="User is not banned.")
                    return

                user_to_unban_roles = json.loads(fetched[0])
                response = await self.rest_client.member_roles(self.guild, user_to_unban, roles=user_to_unban_roles)
                await self._respond(response, token, interaction_id)
        else:
            await self.rest_client.send_interaction_callback(interaction_id, token, InteractionTypes.RESPOND_WITH_MESSAGE, content="You do not have permission to use that command!")

    async def polling_unban(self):
        while True:
            await asyncio.sleep(60)
            async with Ban.lock:
                Ban.cur.execute("SELECT user_id, roles, duration, time_stamp FROM banlist")
                users = Ban.cur.fetchall()

                for user in users:
                    difference = time.time() - user[3]
                    if difference > user[2]:
                        await self.rest_client.member_roles(self.guild, user[0], roles=json.loads(user[1]))
                        Ban.cur.execute("DELETE FROM banlist WHERE user_id = ?", (user[0],))
                        Ban.con.commit()