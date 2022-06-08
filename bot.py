import praw
from contextlib import suppress
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

# TODO: Collect this data
#def getinboxdata(inboxdata):
# for item in reddit.inbox.all(limit=None):
#    print(repr(item))


# Define the bot's response to a comment
def get_balance(user):
    rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:22225" % ('user', 'pass'))
    get_balance = rpc_connection.getbalance(user)
    return get_balance # This will print the balance

def withdraw(sender, address, amount):
    rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:22225" % ('user', 'pass'))
    withdraw = rpc_connection.sendfrom(sender, address, amount)
    return withdraw

def getnewaddress(user):
    rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:22225" % ('user', 'pass'))
    getnewaddress = rpc_connection.getnewaddress(user)
    return getnewaddress

def getaddress(user):
    rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:22225" % ('user', 'pass'))
    getaccountaddress = rpc_connection.getaccountaddress(user)
    return getaccountaddress

def tip(sender, reciever, amount):
    rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:22225" % ('user', 'pass'))
    tip = rpc_connection.sendfrom(sender, reciever, amount)
    return tip

# Commands
for item in reddit.inbox.unread(limit=None):

     if item.body.startswith('+help'): 
        item.reply("+bal - Check your balance.\n+withdraw - Withdraw your balance. Usage: +withdraw ADDRESS AMMOUNT\n+makeaccount - Make an account. PS: Do not run this multiple times!.\n Important: I am not responsible for any loss of funds.")
        item.mark_read()

     if item.body.startswith("+withdraw"):
          print(item.author.name + " requested a withdraw")
          command=item.body
          command_splitted = command.split(" ")
          address = command_splitted[1]
          amount = command_splitted[2]
          print(address, amount)
          sender = item.author.name
          withdraw(sender, address, amount)
          item.reply("Withdrawal of " + amount + " BKC to " + address + " successful. \n Important: I am not responsible for any loss of funds.")
          print("Withdrew " + amount + " to " + address)
          item.mark_read()

     if item.body.startswith("+makeaccount"):
            print("bruh")
            print(item.author.name + " requested a new account")
            user = item.author.name
            withdraw(user)
            item.reply("It's dangerous to go alone, take this! PS: Please dont run this command multiple times, its gonna fuck up your account... \n Important: I am not responsible for any loss of funds.")
            print("Created account for " + user)
            item.mark_read()

     if item.body.startswith("+bal"):
         print("worke")
         user = item.author.name
         item.reply("Your balance is " + str(get_balance(user)) + " BKC \n Important: I am not responsible for any loss of funds.")
         item.mark_read()

     if item.body.startswith("+dep"):
         print("worke")
         user = item.author.name
         json_data = getaddress(user)
         element_one = json_data[0]
         item.reply("Your address is " + element_one + " \n Important: I am not responsible for any loss of funds.")
         item.mark_read()

     if item.body.startswith("+tip"):
         print("bruh")
         sender = item.author.name
         command = item.body
         command_splitted = command.split(" ")
         myballs = command_splitted[2]
         reciever = getaddress(myballs)
         print(reciever)
         amount = command_splitted[3]
         withdraw(sender, reciever, amount)
         item.reply("Tip of " + amount + " BKC to " + reciever + " successful. \n Important: I am not responsible for any loss of funds.")
         item.mark_read()
