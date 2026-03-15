from sqlitehandler import SQL

class VouchSystem:
    def __init__(self, rest_client, vouch_channel):
        self.rest_client = rest_client
        self.vouch_channel = vouch_channel
        self.sql = SQL()

    async def on_message(self, channel_id, content, message_id, user_id):
        if self.vouch_channel == channel_id:
            splitted = content.split()
            if len(splitted) == 2:
                discord_member = splitted[1][2:-1]

                if discord_member == user_id:
                    return

                if splitted[0].lower() == "vouch" and splitted[1].startswith("<@") and discord_member.isdigit() and len(discord_member) > 16 and len(discord_member) < 22:
                    await self.rest_client.add_reaction(channel_id, message_id, emoji="✅")

                    points = await self.sql.get(table="vouches", columns="points", search_column="user_id", values=(discord_member,))
                    
                    if points:
                        points = points[0][0]
                        points += 1
                    else: points = 1
                    
                    await self.sql.insert(table="vouches", columns="user_id,points", values=(discord_member, points))

    async def vouches_command(self, es, user_id, values):
        response = "You have"
        if values:
            user_id = values[0]
            response = "That person has"

        points = await self.sql.get("vouches", columns="points", search_column="user_id", values=(user_id,))

        if not points: points = 0 
        else: points = points[0][0]

        embed = [{
            "title": "✅ Current Vouches",
            "description": f"{response} **{points}** vouches!",
            "color": 7506394
        }]

        await es.respond_message(embed=embed)