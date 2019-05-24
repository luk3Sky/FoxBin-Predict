from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

from foxbinary.consumers import BinaryConsumer

application = ProtocolTypeRouter({
    # WebSocket handler
    "websocket": AllowedHostsOriginValidator(
    	AuthMiddlewareStack(
	        URLRouter(
	        	[
		            url(r"^ml/", BinaryConsumer)
	        	]
	       	)
	    )
    )
})
