import logging
import asyncio
from websockets import ConnectionClosed, InvalidHandshake, ConnectionClosedError
from socket import gaierror
from ssl import SSLError

class InvalidTokenError(Exception): pass
class MaxRetriesAttempted(Exception): pass
class InvalidIntentsError(Exception): pass
class DisallowedIntentsError(Exception): pass

class HandleGatewayErrors:
    def __init__(self):
        self.reset_counter = 0
        self.logger = logging.getLogger(__name__)

    async def handle_gateway_errors(self, ws, e):
        if isinstance(e, (OSError, ConnectionClosedError, ConnectionClosed, gaierror, InvalidHandshake, SSLError)):
            pass
        else:
            raise e
        
        if hasattr(ws, "close_code") and ws.close_code is not None:
            if ws.close_code == 1000:
                self.logger.warning("Discord closed for maintainence or related. Close code 1000.")

            elif ws.close_code == 4001:
                self.logger.error("Please report this. Unknown opcode was sent. Code 4001")

            elif ws.close_code == 4003:
                self.logger.error("Discord responded with NOT_AUTHENTICATED code 4003. This should be impossible. Report this please.")

            elif ws.close_code == 4004:
                raise InvalidTokenError("Token is invalid. Code 4004")

            elif ws.close_code == 4005:
                self.logger.error("Discord responded with ALREADY_AUTHENTICATED. This shouldn't happen. Code 4005")

            elif ws.close_code == 4008:
                self.logger.warning("Discord is ratelimiting gateway connect attempts. Sleeping for ten seconds before retry. Code 4008")
                await asyncio.sleep(10)

            elif ws.close_code == 4013:
                raise InvalidIntentsError("Invalid Intents. Code 4013")

            elif ws.close_code == 4014:
                raise DisallowedIntentsError("You must open discord developer portal and enable intents. Code 4014.")

        if hasattr(ws, "close_code") and ws.close_code is None:
            self.logger.debug("Attempting to close connection")
            await ws.close() 

        self.reset_counter += 1

        if self.reset_counter == 100:
            raise MaxRetriesAttempted("Multiple retries attempted and failed.")
        else:
            await asyncio.sleep(self.reset_counter * 2)