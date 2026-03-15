import asyncio
import json
import time
from sqlitehandler import SQL
from betterbot import ResponseTypes

class Ban:
    def __init__(self, mod_roles, rest_client, guild, ban_role):
        self.rest_client = rest_client
        self.mod_roles = mod_roles
        self.guild = guild
        self.ban_role = ban_role
        self.sql = SQL()

    async def _check_mod(self, roles):
        if any(r in self.mod_roles for r in roles):
            return True
        else:
            return False
        
    async def _respond(self, response, es):
        if response != ResponseTypes.FAILED and response != ResponseTypes.CONNECTION_FAILED:
            await es.respond_message(content=f"Successfully completed your requested action.")
            return True
        else:
            await es.respond_message(content=f"Oops something went wrong.")
            return False

    async def ban(self, values, es, roles):
        if await self._check_mod(roles):
            user_to_ban = values[0]
            unit = values[1]
            duration = values[2]
            
            payload = await self.rest_client.get_guild_member(self.guild, user_to_ban)
            check_roles = payload.get("roles")

            if check_roles != self.ban_role:
                response = await self.rest_client.member_roles(self.guild, user_to_ban, roles=self.ban_role)

            all_roles = json.dumps(check_roles)

            if await self._respond(response, es):
                if unit == "days": amount = duration*86400
                if unit == "hours": amount = duration*3600
                if unit == "minutes": amount = duration*60
                
                await self.sql.insert(table="banlist", columns="user_id,roles,duration,time_stamp", values=(user_to_ban, all_roles, amount, time.time()))
        else:
            await es.respond_message(content="You do not have permission to use that command!", ephemeral=True)

    async def unban(self, values, roles, es):
        if await self._check_mod(roles):
            user_to_unban = values[0]

            fetched = await self.sql.get(table="banlist", columns="roles", search_column="user_id", values=(user_to_unban,))

            if fetched is None:
                await es.respond_message(content="User is not banned.")
                return

            user_to_unban_roles = json.loads(fetched[0][0])
            response = await self.rest_client.member_roles(self.guild, user_to_unban, roles=user_to_unban_roles)
            
            await self.sql.delete(table="banlist", search_column="user_id", values=(user_to_unban,))
            
            await self._respond(response, es)
        else:
            await es.respond_message(content="You do not have permission to use that command!", ephemeral=True)

    async def polling_unban(self):
        while True:
            users = await self.sql.get(table="banlist", columns="user_id,roles,duration,time_stamp")
            
            for user in users:
                difference = time.time() - user[3]
                if difference > user[2]:
                    await self.rest_client.member_roles(self.guild, user[0], roles=json.loads(user[1]))
                    await self.sql.delete(table="banlist", search_column="user_id", values=(user[0],))

            await asyncio.sleep(60)
