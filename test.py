import discord
from discord.ext import commands, tasks
from discord import app_commands
import main

TOKEN = 'MTMwMTE2MTM0Njg0MjIzNDk1Mw.GYCPc1.7wXYgp3VsC5wV2wWLLAymg7V_A4xWp-RWowUbo'
GUILD_ID = 1300841680416538635
CATALOG_CHANNEL_ID = 1300861513086799993
READ_CHANNEL_ID = 1300841680965996596
TOS_ID = 1300858485868859424
PAY_ID = 1300859905296695427
FAQ_ID = 1301219045357654077

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Sample product catalog descriptions
product_catalog = {
    "Nitro": """> **:money_with_wings:  Nitro Price Lists**
> 
> Nitro Boost 1 month >> **6.5 USD**
> Nitro Boost 1 year >> **22 USD (best deal)**""",
    
    "Server Boost": """> **:money_with_wings:  Server Boost Price Lists**
> 
> x14 Server Boost 1 month >>** 3 USD**
> x14 Server Boost 3 month >> **6.5 USD**""",
    
    "Decorations": """Flexible pricing depends on what you chose, create a ticket to get the price!""",
    
    "Robux": """> **Robux Price List**
> 
> R$1000 >> **7.5 USD**
> R$10000  >>** 65 USD**""",
    
    "VPNs": """> **VPN Price Lists**
> 
> NordVPN 3 month >> **5 USD**
> IPVanish 1 year >> **10 USD (best deal)**""",
    
    "Streaming": """> **Streaming Services Price Lists**
> 
> Spotify 1 month >>** 1.5 USD**
> Netflix 1 month >> **2.5 USD**
> Netflix 3 month >>** 6.5 USD**"""
}

catalog_text = (
    """**Product Catalogue**
> *If you are interested in purchasing a specific item or want to check the current price list, please click below.
> This way you will be able to see the selected product and familiarize yourself with available offers.
> There this is only a relative price; it may change slightly depending on when you purchase them.
> For Vietnam customers, you may benefit from local pricing, applicable only via bank/Momo transfer.*"""
)

# Custom dropdown view for selecting a product
class ProductDropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label=product_name, description="Select to view details")
            for product_name in product_catalog
        ]
        super().__init__(placeholder="Choose a product...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        selected_product = self.values[0]
        product_details = product_catalog[selected_product]
        
        await interaction.response.send_message(f"**{selected_product}**\n{product_details}", ephemeral=True)

class ProductDropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(ProductDropdown())

# Function to send messages only if the channel is empty
async def send_if_empty(channel, content, view=None):
    async for message in channel.history(limit=1):
        if message.author == bot.user:
            return  # Message already sent by the bot, do nothing
    await channel.send(content, view=view)  # Send the message if channel is empty


# Initialize the bot and sync commands
@bot.event
async def on_ready():
    # Send "Hello" to the specified channel if it's empty
    hello_channel = bot.get_channel(READ_CHANNEL_ID)
    if hello_channel:
        await send_if_empty(hello_channel, f"""> Discover the best Services at **DPS Store**
> ***Tired of overpaying*** for streaming services? Look no further! We're revolutionizing the industry by offering top-notch services at unbeatable prices. From ***Nitro Boost to Spotify and beyond***, we've got you covered!
> Why choose us?
> ***Unmatched Affordability***: Save more without sacrificing quality.
> ***Extensive Selection***: Find the perfect service to suit most of your needs.
> ***Reliable Warranty***: Enjoy peace of mind with our customer satisfaction guarantee.
> Ready to experience the difference? **Visit our store today and explore our exciting offerings!**""")
    
    tos = bot.get_channel(TOS_ID)
    if tos:
        await send_if_empty(tos, f"""> ***PLEASE READ THIS BEFORE PROCEEDING TO PURCHASE ANYTHING FROM US!***
> 
> **Support & Delivery:**
> We aim to respond to support inquiries within 12 hours, with a maximum of 48 hours in rare cases.
> We prioritize timely delivery, but unforeseen technical issues may cause delays.
> We use secure payment methods like Bank Transfer (VN) or Crypto and many others ([click for more details](https://discord.com/channels/1300841680416538635/1300859905296695427) ).
> Your personal information is kept confidential and only for legal purposes.
> Our products are legal and safe to use without risking account bans.
> 
> **Refund Policy:**
> We offer refunds for issues caused by our services.
> Refunds are not available for features restricted by your location or use of prohibited tools.
> We cannot be held responsible for Discord account bans or (revoke) reversals.
> 
> **Payment & Verification:**
> Unauthorized chargebacks without contacting support may lead to account restrictions.
> We cannot replace revoked Discord boosts.
> Payments may be temporarily held for verification purposes.
> We reserve the right to decline payments if legitimacy is questionable.
> Refunds are not issued after successful product delivery.
> Payment limits and additional verification may apply, especially for PayPal transactions.""")
        
    pay = bot.get_channel(PAY_ID)
    if pay:
        await send_if_empty(pay, f"""> :money_with_wings: Payment methods:
> Crypto (ETH/LTC)
> Paypal (***F&F only, plus 18% fee***)
> MoMo (**Viet Nam only**)
> Bank Transfer (**Viet Nam only**)
> 
> **Note: If you pay with cryptocurrencies/Momo/bank transfer, ask about the possibility of receiving a discount, which is available in most offers.**""")
        
        
    faq = bot.get_channel(FAQ_ID)
    if faq:
        await send_if_empty(faq, f"""> **How will I receive my product after payment?**
> Once your payment is completed, the product details will be sent to you straight in the your ticket or DM.
> 
> **What is the delivery time?**
> Most products are delivered instantly, although some may take a little longer. Our goal is to deliver within one to two hours, but it could take up to 48 hours. Keep in mind that our working hours are from 17:00 to 23:00 UTC +7 on weekdays, and we are available all day on weekends.
> 
> **What if my product doesnt function as expected?**
> We offer a full refund if your product does not work as intended. However, if you use any of the designated tools, we cannot guarantee listings for them. Additionally, regarding Server Boosts, if your Discord account gets banned, we will not be able to assist you as that situation is beyond our control.""")
    
    # Reset the product catalog only if the channel is empty
    channel = bot.get_channel(CATALOG_CHANNEL_ID)
    if channel:
        await send_if_empty(channel, catalog_text, view=ProductDropdownView())  # Reset the catalog on startup

    await bot.tree.sync()  # Sync commands globally
    print(f"{bot.user} is now running!")

# Run the bot
bot.run(TOKEN)
