from .endpoints import Endpoints
from ...gateway_client.event_related.events import Events
from ..error import Types

class Application:
    def __init__(self, wrapper, eventbus):
        self.send = wrapper.request
        self.register = eventbus.register

    # -------------------------
    # GLOBAL COMMANDS
    # -------------------------

    async def get_global_commands(self, application_id):
        endpoint = Endpoints.APPLICATION_GLOBAL_COMMANDS(d={"application_id": application_id})
        return await self.send(method="get", endpoint=endpoint, identifier=f"get_global_commands:{application_id}")

    async def create_global_command(self, application_id, name, description, options=None, cmd_type=1, *handlers):
        payload = {"name": name, "description": description, "type": cmd_type}
        if options: payload["options"] = options
        endpoint = Endpoints.APPLICATION_GLOBAL_COMMANDS(d={"application_id": application_id})
        response = await self.send(method="post", endpoint=endpoint, identifier=f"create_global_command:{application_id}", json=payload)
        
        if response != Types.FAILED and response != Types.CONNECTION_FAILED:
            event = f"{Events.INTERACTION_CREATE}:{name}"
            await self.register(event, *handlers)
        
        return response
    
    async def get_global_command(self, application_id, command_id):
        endpoint = Endpoints.APPLICATION_COMMAND(d={"application_id": application_id, "command_id": command_id})
        return await self.send(method="get", endpoint=endpoint, identifier=f"get_global_command:{application_id}")

    async def update_global_command(self, application_id, command_id, name=None, description=None, options=None):
        payload = {}
        if name: payload["name"] = name
        if description: payload["description"] = description
        if options: payload["options"] = options
        endpoint = Endpoints.APPLICATION_COMMAND(d={"application_id": application_id, "command_id": command_id})
        return await self.send(method="patch", endpoint=endpoint, identifier=f"update_global_command:{application_id}", json=payload)

    async def delete_global_command(self, application_id, command_id):
        endpoint = Endpoints.APPLICATION_COMMAND(d={"application_id": application_id, "command_id": command_id})
        return await self.send(method="delete", endpoint=endpoint, identifier=f"delete_global_command:{application_id}")

    # -------------------------
    # GUILD COMMANDS
    # -------------------------

    async def get_guild_commands(self, application_id, guild_id):
        endpoint = Endpoints.APPLICATION_GUILD_COMMANDS(d={"application_id": application_id, "guild_id": guild_id})
        return await self.send(method="get", endpoint=endpoint, identifier=f"get_guild_commands:{application_id}:{guild_id}")

    async def create_guild_command(self, application_id, guild_id, name, description, options=None, cmd_type=1, *handlers):
        payload = {"name": name, "description": description, "type": cmd_type}
        if options: payload["options"] = options
        endpoint = Endpoints.APPLICATION_GUILD_COMMANDS(d={"application_id": application_id, "guild_id": guild_id})
        response = await self.send(method="post", endpoint=endpoint, identifier=f"create_guild_command:{application_id}:{guild_id}", json=payload)

        if response != Types.FAILED and response != Types.CONNECTION_FAILED:
            event = f"{Events.INTERACTION_CREATE}:{name}:{guild_id}"
            await self.register(event, *handlers)
        
        return response

    async def get_guild_command(self, application_id, guild_id, command_id):
        endpoint = Endpoints.APPLICATION_GUILD_COMMAND(d={"application_id": application_id, "guild_id": guild_id, "command_id": command_id})
        return await self.send(method="get", endpoint=endpoint, identifier=f"get_guild_command:{application_id}:{guild_id}")

    async def update_guild_command(self, application_id, guild_id, command_id, name=None, description=None, options=None):
        payload = {}
        if name: payload["name"] = name
        if description: payload["description"] = description
        if options: payload["options"] = options
        endpoint = Endpoints.APPLICATION_GUILD_COMMAND(d={"application_id": application_id, "guild_id": guild_id, "command_id": command_id})
        return await self.send(method="patch", endpoint=endpoint, identifier=f"update_guild_command:{application_id}:{guild_id}", json=payload)

    async def delete_guild_command(self, application_id, guild_id, command_id):
        endpoint = Endpoints.APPLICATION_GUILD_COMMAND(d={"application_id": application_id, "guild_id": guild_id, "command_id": command_id})
        return await self.send(method="delete", endpoint=endpoint, identifier=f"delete_guild_command:{application_id}:{guild_id}")

    # -------------------------
    # COMMAND PERMISSIONS
    # -------------------------

    async def get_command_permissions(self, application_id, guild_id, command_id):
        endpoint = Endpoints.APPLICATION_COMMAND_PERMISSIONS(d={"application_id": application_id, "guild_id": guild_id, "command_id": command_id})
        return await self.send(method="get", endpoint=endpoint, identifier=f"get_command_permissions:{application_id}:{guild_id}")

    async def update_command_permissions(self, application_id, guild_id, command_id, permissions):
        payload = {"permissions": permissions}
        endpoint = Endpoints.APPLICATION_COMMAND_PERMISSIONS(d={"application_id": application_id, "guild_id": guild_id, "command_id": command_id})
        return await self.send(method="put", endpoint=endpoint, identifier=f"update_command_permissions:{application_id}:{guild_id}", json=payload)