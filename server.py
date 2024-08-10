####################################### previous code #########################################
###############################################################################################


# from twisted.cred.checkers import AllowAnonymousAccess
# from twisted.cred.checkers import InMemoryUsernamePasswordDatabaseDontUse
# from twisted.internet import reactor
# from twisted.protocols.ftp import FTPFactory, FTPRealm
# from twisted.cred.portal import Portal


# checker = InMemoryUsernamePasswordDatabaseDontUse()
# checker.addUser("ratul", "123456789")
# checker.addUser("robot", "123456789")

# portal = Portal(FTPRealm("./public", "./users"), [AllowAnonymousAccess(), checker])

# factory = FTPFactory(portal)
# reactor.listenTCP(21, factory)
# reactor.run()





####################################### Improved version of code #############################################
####################################### Improved version of code #############################################
##############################################################################################################

# Though I did not hash password


from twisted.cred.checkers import AllowAnonymousAccess, InMemoryUsernamePasswordDatabaseDontUse
from twisted.internet import reactor
from twisted.protocols.ftp import FTPFactory, FTPRealm
from twisted.cred.portal import Portal
from twisted.python import log
import socket
import sys

# Function to get the IP address of the machine
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Connect to a public server (doesn't have to send actual data)
        s.connect(('8.8.8.8', 1))
        ip_address = s.getsockname()[0]
    except Exception:
        ip_address = '127.0.0.1'
    finally:
        s.close()
    return ip_address

# Function to start the FTP server
def start_ftp_server(users, anonymous_root="./public", user_root="./users", port=21):
    # Enable logging to the console
    log.startLogging(sys.stdout)

    # Create an in-memory database for user authentication
    checker = InMemoryUsernamePasswordDatabaseDontUse()
    for username, password in users.items():
        checker.addUser(username, password)

    # Set up the FTP Realm with directories for anonymous and authenticated users
    ftpRealm = FTPRealm(anonymousRoot=anonymous_root, userHome=user_root)

    # Use a portal to manage authentication and authorization
    portal = Portal(ftpRealm, [AllowAnonymousAccess(), checker])

    # Create the FTP factory, which listens for connections
    factory = FTPFactory(portal)

    # Get the IP address of the server
    ip_address = get_ip_address()

    # Listen on the specified port
    reactor.listenTCP(port, factory)
    print(f"FTP server started on {ip_address}:{port}")
    reactor.run()


# Yo main yoooo 
if __name__ == "__main__":
    # Define user credentials (username: password)
    users = {
        "ratul": "123456789",
        "robot": "123456789"
    }

    # Define directories for anonymous users and authenticated users
    anonymous_root = "./public"
    user_root = "./users"

    # Start the FTP server on port 21
    start_ftp_server(users=users, anonymous_root=anonymous_root, user_root=user_root, port=21)
