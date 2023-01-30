import discord
import openai
import config

PREFIX = "/"

class SlashCommandBuilder:
    def __init__(self, command_name, client):
        self.command_name = command_name
        self.client = client
    
    async def handle_message(self, message):
        # Ignore messages sent by the bot
        if message.author == self.client.user:
            return
        # Check if the message starts with the prefix and command name
        if message.content.startswith(f"{PREFIX}{self.command_name}"):
            # Get the question from the user
            question = message.content[len(f"{PREFIX}{self.command_name}"):].strip()
            # Generate an answer using the OpenAI API
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=f"{question}\n",
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5,
            ).choices[0].text
            # Send the answer back to the user
            await message.channel.send(response)

# Initialize the Discord client
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = discord.Client(intents=intents)
# Initialize the OpenAI API
openai.api_key = config.OPENAI_API_KEY

# Declare the custom slash command
globalCommand = SlashCommandBuilder("ask", client)

@client.event
async def on_ready():
    print("Bot is ready to answer questions.")

@client.event
async def on_message(message):
    await globalCommand.handle_message(message)

# Run the Discord client
client.run(config.DISCORD_API_KEY)
