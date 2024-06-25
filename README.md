# Launching the solution

To spin up the project, simply install Docker Desktop and then run the following commands:

```
git clone https://github.com/alexben16/TaskBen
cd TaskBen
docker compose up -d 
```

 # Tearing it down
 
When you're done, simply remove the containers by running the following command:

```
docker compose down
```

# Using the Discord bot

Learn the actual token and update TOKEN in bot.py

- First method:

  - Send the `!start` command to the TaskBen#3563 bot

- Second method:

  - Create a Discord server
   
  - Invite the Bot to your server at the following link: https://discord.com/oauth2/authorize?client_id=1254711882518888582&permissions=3072&integration_type=0&scope=bot
   
  - Send the `!start` command to the channel
