from ..endpoints import Endpoints

class Interaction:
    def __init__(self, wrapper):
        self.send = wrapper.request

    async def send_interaction_callback(self, interaction_id, interaction_token, content=None, embed=None, components=None):
        payload = {}
        if content: payload["content"] = content
        if embed: payload["embed"] = embed
        if components: payload["components"] = components
        endpoint = Endpoints.INTERACTION_CALLBACK(d={"interaction_id": interaction_id, "interaction_token": interaction_token})
        return await self.send(method="post", endpoint=endpoint, identifier=f"interaction_callback", json=payload)

    async def send_interaction_followup(self, application_id, interaction_token, content=None, embed=None, components=None):
        payload = {}
        if content: payload["content"] = content
        if embed: payload["embed"] = embed
        if components: payload["components"] = components
        endpoint = Endpoints.INTERACTION_FOLLOWUP(d={"application_id": application_id, "interaction_token": interaction_token})
        return await self.send(method="post", endpoint=endpoint, identifier=f"interaction_followup:{application_id}", json=payload)

    async def get_original_interaction_message(self, application_id, interaction_token):
        endpoint = Endpoints.INTERACTION_ORIGINAL_MESSAGE(d={"application_id": application_id, "interaction_token": interaction_token})
        return await self.send(method="get", endpoint=endpoint, identifier=f"interaction_original_message:{application_id}")

    async def update_interaction_message(self, application_id, interaction_token, content=None, embed=None, components=None, message_id=None):
        payload = {}
        if content: payload["content"] = content
        if embed: payload["embed"] = embed
        if components: payload["components"] = components
        endpoint = Endpoints.INTERACTION_UPDATE_MESSAGE(d={"application_id": application_id, "interaction_token": interaction_token, "message_id": message_id or "@original"})
        return await self.send(method="patch", endpoint=endpoint, identifier=f"interaction_update_message:{application_id}", json=payload)