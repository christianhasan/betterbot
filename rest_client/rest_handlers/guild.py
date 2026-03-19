from .endpoints import Endpoints

class Guild:
    def __init__(self, wrapper):
        self.send = wrapper.request

    async def get_guild_info(self, guild_id):
        endpoint = Endpoints.GUILD_INFO(d={"guild_id": guild_id})
        return await self.send(method="get", endpoint=endpoint, identifier=f"guild_info:{guild_id}")

    async def get_guild_members(self, guild_id, limit=1000, after=None):
        endpoint = Endpoints.GUILD_MEMBERS_LIST(d={"guild_id": guild_id}) + (f"?limit={limit}" if after is None else f"limit={limit}&after={after}")
        return await self.send(method="get", endpoint=endpoint, identifier=f"guild_members:{guild_id}")

    async def get_guild_member(self, guild_id, user_id):
        endpoint = Endpoints.GUILD_MEMBER_INFO(d={"guild_id": guild_id, "user_id": user_id})
        return await self.send(method="get", endpoint=endpoint, identifier=f"guild_member:{guild_id}")

    async def get_guild_roles(self, guild_id):
        endpoint = Endpoints.GUILD_ROLES_LIST(d={"guild_id": guild_id})
        return await self.send(method="get", endpoint=endpoint, identifier=f"guild_roles:{guild_id}")

    async def get_guild_role(self, guild_id, role_id):
        endpoint = Endpoints.GUILD_ROLE_INFO(d={"guild_id": guild_id, "role_id": role_id})
        return await self.send(method="get", endpoint=endpoint, identifier=f"guild_role:{guild_id}")

    async def add_member_role(self, guild_id, user_id, role_id):
        endpoint = Endpoints.MEMBER_ROLE_ASSIGN(d={"guild_id": guild_id, "user_id": user_id, "role_id": role_id})
        return await self.send(method="put", endpoint=endpoint, identifier=f"guild_roles_assign:{guild_id}")

    async def remove_member_role(self, guild_id, user_id, role_id):
        endpoint = Endpoints.MEMBER_ROLE_ASSIGN(d={"guild_id": guild_id, "user_id": user_id, "role_id": role_id})
        return await self.send(method="delete", endpoint=endpoint, identifier=f"guild_role_remove:{guild_id}")

    async def member_roles(self, guild, user_id, roles=None):
        payload = {"roles": []}
        if roles: payload["roles"] = roles
        endpoint = Endpoints.MEMBER_ROLE_ASSIGN_JSON(d={"guild_id": guild, "user_id": user_id})
        return await self.send(method="patch", endpoint=endpoint, identifier=f"guild_roles_remove:{guild}", json=payload)

    async def get_guild_bans(self, guild_id):
        endpoint = Endpoints.GUILD_BANS_LIST(d={"guild_id": guild_id})
        return await self.send(method="get", endpoint=endpoint, identifier=f"get:bans:{guild_id}")

    async def get_guild_ban(self, guild_id, user_id):
        endpoint = Endpoints.GUILD_BAN(d={"guild_id": guild_id, "user_id": user_id})
        return await self.send(method="get", endpoint=endpoint, identifier=f"get:ban:{guild_id}")

    async def ban(self, guild_id, user_id):
        endpoint = Endpoints.GUILD_BAN(d={"guild_id": guild_id, "user_id": user_id})
        return await self.send(method="put", endpoint=endpoint, identifier=f"put:ban:{guild_id}")

    async def prune_guild_members(self, guild_id, days=None, compute_prune_count=False):
        payload = {}
        if days is not None: payload["days"] = days
        payload["compute_prune_count"] = compute_prune_count
        endpoint = Endpoints.GUILD_PRUNE_MEMBERS(d={"guild_id": guild_id})
        return await self.send(method="post", endpoint=endpoint, identifier=f"guild_prune:{guild_id}", json=payload)

    async def get_guild_channels(self, guild_id):
        endpoint = Endpoints.GUILD_CHANNELS_LIST(d={"guild_id": guild_id})
        return await self.send(method="get", endpoint=endpoint, identifier=f"guild_channels:{guild_id}")
