import praw
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

# Authenticate with Reddit
reddit = praw.Reddit(
    client_id='',
    client_secret='',
    user_agent='Bunkertip Alpha 0.1 by /u/IdotMaster1',
    username='bunkertip',
    password=''
)

reddit.validate_on_submit = True

# Print the username of the bot
print(reddit.user.me())

# Define RPC connection details
RPC_USER = 'user'
RPC_PASSWORD = 'pass'
RPC_HOST = '127.0.0.1'
RPC_PORT = 22225

# RPC connection function
def get_rpc_connection():
    return AuthServiceProxy(f"http://{RPC_USER}:{RPC_PASSWORD}@{RPC_HOST}:{RPC_PORT}")

# Define the bot's response to a comment
def get_balance(user):
    rpc_connection = get_rpc_connection()
    get_balance = rpc_connection.getbalance(user)
    return get_balance

def withdraw(sender, address, amount):
    rpc_connection = get_rpc_connection()
    withdraw = rpc_connection.sendfrom(sender, address, amount)
    return withdraw

def getnewaddress(user):
    rpc_connection = get_rpc_connection()
    getnewaddress = rpc_connection.getnewaddress(user)
    return getnewaddress

def getaddress(user):
    rpc_connection = get_rpc_connection()
    getaccountaddress = rpc_connection.getaccountaddress(user)
    return getaccountaddress

# Commands
for item in reddit.inbox.unread(limit=None):
    if item.body.startswith('+help'):
        item.reply("+bal - Check your balance.\n+withdraw - Withdraw your balance. Usage: +withdraw ADDRESS AMOUNT\n+makeaccount - Make an account. PS: Do not run this multiple times!.\n Important: I am not responsible for any loss of funds.")
        item.mark_read()

    elif item.body.startswith("+withdraw"):
        print(item.author.name + " requested a withdrawal")
        command = item.body
        command_splitted = command.split(" ")
        address = command_splitted[1]
        amount = command_splitted[2]
        print(address, amount)
        sender = item.author.name
        withdraw(sender, address, amount)
        item.reply("Withdrawal of " + amount + " BKC to " + address + " successful. \n Important: I am not responsible for any loss of funds.")
        print("Withdrew " + amount + " to " + address)
        item.mark_read()

    elif item.body.startswith("+makeaccount"):
        print(item.author.name + " requested a new account")
        user = item.author.name
        new_address = getnewaddress(user)
        item.reply("It's dangerous to go alone, take this! Your new address is " + new_address + " \n Important: I am not responsible for any loss of funds.")
        print("Created account for " + user)
        item.mark_read()

    elif item.body.startswith("+bal"):
        print(item.author.name + " requested balance")
        user = item.author.name
        balance = get_balance(user)
        item.reply("Your balance is " + str(balance) + " BKC \n Important: I am not responsible for any loss of funds.")
        item.mark_read()

    elif item.body.startswith("+dep"):
        print(item.author.name + " requested deposit address")
        user = item.author.name
        deposit_address = getaddress(user)
        item.reply("Your address is " + deposit_address + " \n Important: I am not responsible for any loss of funds.")
        item.mark_read()

    elif item.body.startswith("+tip"):
        print(item.author.name + " requested a tip")
        sender = item.author.name
        command = item.body
        command_splitted = command.split(" ")
        recipient = command_splitted[1]
        amount = command_splitted[2]
        withdraw(sender, recipient, amount)
        item.reply("Tip of " + amount + " BKC to " + recipient + " successful. \n Important: I am not responsible for any loss of funds.")
        item.mark_read()
