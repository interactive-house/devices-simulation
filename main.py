from threading import Thread
import testClient
import testServer

client = Thread(target=testClient.main)
client.start()
server = Thread(target=testServer.main)
server.start()



