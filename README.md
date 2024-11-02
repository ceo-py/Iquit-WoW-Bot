# WoW Mythic+ Discord Bot

A Discord bot for World of Warcraft (WoW) players, designed specifically for Mythic Plus (M+) players and enthusiasts. This bot allows users to check character progress, ranks, gear, and real-time WoW token prices via easy-to-use slash commands. It helps you stay on top of your performance and compare yourself with other players in your Discord server.

## Key Features

- **Track Mythic Plus Performance**: Add your characters to the server and track their Mythic Plus rank and progression.
- **Automated Character Progression Updates**: Every 15 minutes, the bot checks all characters added to the server for any rating changes. If a character's progression improves, an announcement will be made with details on the rating change, dungeon performance, and current rank.
- **Check Character Information**: View detailed character data such as item level, raid progression, last Mythic dungeon completed, and links for selected character to Raidbots, Wowhead, Wowprogress and Archon.
- **View WoW Token Prices**: Stay up to date with WoW token prices for your region.
- **Interactive Gear Guide**: Access gear guides and gear progression tips, all with just one command.
- **Mythic Plus Dungeon Records**: On use it will display a character's best record for each Mythic Plus dungeon, including affixes, key level, time, and score.

## Commands

### `/rank`
Displays a ranking of all characters added to the Discord server, sorted by roles (Tank, DPS, Healer) and by total performance.

- **Usage**: `/rank`
- **Output**: A leaderboard that sorts players by their role and Mythic Plus performance.

## Automated Progression Announcements

The bot automatically checks all characters in the server every 15 minutes for any Mythic Plus rating changes. If a character shows progression, an announcement will be posted in the Discord channel with the following information:

- **Character name and new rating**: Includes the role icon and rating change.
- **Rank position**: Shows the character's new rank or if they remain in the same position.
- **Dungeon details**: Displays the completed dungeons with time remaining, score, and level.
![alt text](https://github.com/ceo-py/Iquit-WoW-Bot/blob/main/pictures/announcement_example.png)

### `/mplus`
Displays information about a character's Mythic Plus dungeon records for the current season.

- **Usage**: `/mplus`
- **Parameters**:
  - `region`: The player's region (e.g., `eu`, `us`, `kr`, `tw`).
  - `realm`: The player's server.
  - `character name`: The character's name.

- **Output**: Shows detailed information for each Mythic Plus dungeon completed by the character, including:
  - Dungeon name
  - Key level
  - Affixes
  - Dungeon score
  - Un/Completion time

### `/check`
Displays detailed character information after you provide the character's region, realm, and name.

- **Usage**: `/check`
- **Parameters**: 
  - `region`: The player's region (e.g., `eu`, `us`, `kr`, `tw`).
  - `realm`: The player's server.
  - `character name`: The character's name.
- **Output**: Shows the character's item level, raid progression, last completed Mythic Plus dungeon, and links to:
  - WoW Logs for detailed performance metrics.
  - Raidbots for simulation results.
  - Archon for simulation results.
  - World of Warcraft for character information.

### `/token`
Shows the up-to-date price of the WoW token for your region.

- **Usage**: `/token [region]`
- **Parameters**: 
  - `region`: The region for which you want the token price (e.g., `eu`, `us`, `kr`, `tw`).
- **Output**: The current token price for the specified region.

### `/add`
Add a character to the server's list for tracking and ranking in Mythic Plus.

- **Usage**: `/add`
- **Parameters**:
  - `region`: The player's region (e.g., `eu`, `us`, `kr`, `tw`).
  - `realm`: The player's server.
  - `character name`: The character's name.

- **Output**: Character added to server tracking. Will appear in `/rank` and receive announcements for rating updates.

### `/remove`
Remove a character from the server's tracking list.

- **Usage**: `/remove`
- **Parameters**:
  - `region`: The player's region.
  - `realm`: The player's server.
  - `character name`: The character's name.
- **Output**: The character is removed from the server, and their data will no longer be included in `/rank` and announcements.

### `/gear`
Provides a link to a gear guide and a picture showing gear progression for your character.

- **Usage**: `/gear`
- **Output**: A link to a comprehensive gear guide and a visual representation of gear progression.

## Getting Started

1. **Invite the Bot**: Use the bot's invite link to add it to your Discord server create channel with name "iquit-bot" the bot will answer only in that channel.
2. **Set Up Your Character**: Use `/add` to start tracking your characters' Mythic Plus performance and see them on the rank leaderboard.
3. **Stay Updated**: Use `/check` to view up-to-date information about your characters or `/token` to check the current WoW token price.


---

Enjoy tracking your Mythic Plus progress and stay competitive with your friends and guildmates!

## To use Discord emojis when you self host the bot

1. Upload emoji images from 'icons' folder to your Discord server
2. Copy emoji IDs from Discord
3. Update emoji IDs in database using the provided JSON fileExample
4. Create all emojis into the database using the provided json file (json file name is equal to the table name inside the database). MAKE SURE YOU CHANGE THE IDS IN THE JSON FILE WITH THE ONE YOU GOT FROM DISCORD

[More Information](https://github.com/ceo-py/Iquit-WoW-Bot/issues/2#issuecomment-2453038059)

THE WAY YOU COPY DISCORD EMOJIS IDS RIGHT CLICK ON THE EMOJIS AND **COPY TEXT**
`<:arak:1267431668071792701>`


