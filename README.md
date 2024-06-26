A little bot that I made, so we can use it with my friends and check our progress, among other useful information about WOW.


You can test the bot functionality [here](https://discord.gg/gCcfWpMCgE).

Your Feedback Matters: Help Shape the Future of Iquit Bot
We're always looking for ways to improve our bot and make it even more helpful and engaging for our users. 
That's why we're inviting you to share your feedback and suggestions. [here](https://github.com/ceo-py/Iquit-WoW-Bot/discussions).
## Bot Command Navigation

1. [!add  - Add Characters to the Database](#add-command)
2. [!delete_character - Remove Characters from the Database](#delete-character-command)
3. [!rank - World of Warcraft Rating Details](#rank-command-world-of-warcraft-rating-details)
4. [!check - Detailed Character Information](#check-command-detailed-character-information)
5. [!check - Quick Character Information](#check-command-quick-character-information)
6. [Global Server Announcement - Rating Updates](#global-server-announcement-rating-updates)
7. [/rankglobalsetting - Rank Global Setting](#rank-global-setting-command)
8. [/ranksimple - RankSimple Global](#ranksimple-global-command)
9. [!token - World of Warcraft Price Information](#token-command-world-of-warcraft-price-information)
10. [!weather - Real-Time Weather Information](#weather-command)
11. [!ask - Ask Questions and Get Answers](#ask-command)
12. [Bot Information and Installation](#bot-information-and-installation)



# Add Command

The `!add` command allows users to add their characters to the bot's database for comparison with other characters within the Discord server. This command triggers a pop-up with five fields that must be filled out correctly to successfully add the character. The required fields are:

1. **Region Name:** Enter the region where the character is located (e.g., "US," "EU," "KR," etc.).

2. **Realm Name:** Provide the name of the realm where the character exists.

3. **Character Name:** Input the full name of the character.

4. **Nickname:** Add an optional nickname for the character.

5. **Character Class:** Specify the class or profession of the character (e.g., "Warrior," "Mage," "Rogue," etc.).

## Command Usage

To use the `!add` command, simply type the following in a Discord text channel:

```
!add
```

Upon executing this command, a pop-up will appear, prompting users to enter the required information.

## Instructions

1. **Complete All Fields:** Ensure that all five fields are filled out with accurate and valid information.

2. **Valid Region Names:** Use standard abbreviations for region names, such as "US," "EU," "KR," etc.

3. **Realm Name Accuracy:** Double-check the realm name for accuracy.

4. **Correct Character Name:** Enter the character's full name correctly.

5. **Optional Nickname:** Add a nickname if desired.

6. **Character Class Selection:** Select the appropriate character class from the provided options.

By following the provided instructions and completing all fields accurately, users can seamlessly add their characters to the database using the `!add` command, making them eligible for comparison with other characters in the Discord community.
![alt text](https://github.com/ceo-py/Project-Pictures/blob/main/Iquit/add_character_modal.png?raw=true)


# Delete Character Command

The `!delete_character` command allows users to remove a character from the bot's database. By providing the character name as a parameter, the command will check if the character name exists in the database. If the character name is found, the character will be deleted from the database.

## Command Usage

To use the `!delete_character` command, enter the following in a Discord text channel:

```
!delete_character [character_name]
```

Replace `[character_name]` with the full name of the character that you wish to delete.

## Functionality

1. **Character Deletion:**
   When executing the command with the specific character name, the bot will verify if the character exists in the database. If the character name is found, the character will be removed from the database.

2. **Data Validation:**
   The `!delete_character` command ensures data accuracy by checking if the provided character name matches an existing character in the database before proceeding with the deletion.

## Note

1. **Correct Character Name:**
   Make sure to enter the full and correct name of the character that you wish to delete. Only exact matches will result in the character's removal from the database.

2. **Irreversible Action:**
   Deleting a character from the database is an irreversible action. Exercise caution and verify the character name before executing the command.

By using the `!delete_character` command with the appropriate character name parameter, users can effectively remove characters from the bot's database, ensuring that the database remains up-to-date and accurate for future comparisons.

![alt text](https://github.com/ceo-py/Project-Pictures/blob/main/Iquit/delete_command_example.png?raw=true)


# Rank Command World of Warcraft Rating Details

The `!rank` command provides embedded information about World of Warcraft rating cutoffs for top 0.1%, top 1%, and top 10% players. It displays a leaderboard of the top 9 characters in the Discord server based on their character ratings. Additionally, it showcases the top 3 players for DPS, healers, and tanks, all ranked by character rating.

## Command Usage

To use the `!rank` command, simply type the following in a Discord text channel:

```
!rank
```

## Information Displayed

The `!rank` command will provide the following details:

- **Rating Cutoffs:**
  World of Warcraft rating cutoffs for top 0.1%, top 1%, and top 10% players.

- **Top 9 Characters:**
  A leaderboard of the top 9 characters in the Discord server, ranked by their character ratings.

- **Top 3 for DPS, Healers, and Tanks:**
  The top 3 players for DPS, healers, and tanks, all ranked by character rating.

- **Current Week Affixes:**
  Information about the affixes active in the current week.

- **World Ranks for Every Class and Role:**
  Links to view the current world ranks for every class and role.

## Note

1. **Real-Time Data:**
   The command fetches real-time rating data, ensuring the latest and most accurate information.

2. **Server-Specific Leaderboard:**
   The leaderboard displays characters within the Discord server where the command is used.

3. **Class and Role Rankings:**
   The command provides links to view the current world ranks for every class and role.

By using the `!rank` command, players can easily access comprehensive ranking information, stay competitive, and track their character's performance in World of Warcraft.

![alt text](https://github.com/ceo-py/Project-Pictures/blob/main/Iquit/rank_command_example.png?raw=true)

# Check Command Detailed Character Information

The `!check` command allows users to retrieve comprehensive details about a World of Warcraft character through an embedded view. It requires three mandatory parameters:

1. **Region:** Enter the region of the character (e.g., EU, US, etc.).
2. **Realm:** Provide the name of the realm where the character exists.
3. **Character Name:** Input the full name of the character.

## Command Usage

To use the `!check` command, type the following in a Discord text channel:

```
!check [region] [realm] [character_name]
```

## Information Displayed

The `!check` command will provide the following information about the character:

- **Character Class:** The class or profession of the character.
- **Item Level:** The character's gear item level.
- **Covenant:** The Covenant chosen by the character.
- **Character Link:** Quick links to view the character on WoW Armory, Raidbots, and Warcraft Logs.
- **Raid Progression:** The character's current raid progression on Normal, Heroic, and Mythic difficulties.
- **Dungeon Key:** The last finished dungeon key level, upgrade information, and points obtained for that dungeon.

## Note

1. **Real-Time Data:** The command fetches real-time character information, ensuring the latest and most accurate details.
2. **Character Customization:** The information displayed pertains specifically to the entered character on the provided region and realm.
3. **External Links:** Quick access to WoW Armory, Raidbots, and Warcraft Logs for more in-depth character analysis.

By using the `!check` command with the appropriate parameters, players can gain valuable insights into a character's attributes, progression, and performance, aiding in strategic gameplay and improvement.

![alt text](https://github.com/ceo-py/Project-Pictures/blob/main/Iquit/check_command_example.png?raw=true)

With that command, you'll be able to see more detail information about the character you ask for.

# Check Command Quick Character Information

The `!check` command provides a swift way to access essential information about a World of Warcraft character within the Discord server. With just two parameters required:

1. **Nickname:** Enter the character's nickname within the server.
2. **Class:** Specify the character's class or profession.

## Command Usage

To use the `!check` command for quick character info, type the following in a Discord text channel:

```
!check [nickname] [class]
```

## Information Displayed

The `!check` command will promptly display the following character details:

- **Character Class:** The class or profession of the character.
- **Item Level:** The character's gear item level.
- **Covenant:** The Covenant chosen by the character.
- **Character Link:** Quick link to view the character on WoW Armory, Raidbots, and Warcraft Logs.

## Note

1. **Server-Based:** The command fetches character data specifically from the Discord server, ensuring easy access to relevant information.
2. **Simplified Query:** By providing just the nickname and class, users can swiftly retrieve essential character details without the need for additional information.
3. **External Links:** Quick access to WoW Armory, Raidbots, and Warcraft Logs for further character exploration.

The `!check` command streamlines the process of obtaining essential character information within the server, enabling users to make informed decisions and foster a cohesive World of Warcraft community.
![alt text](https://github.com/ceo-py/Project-Pictures/blob/main/Iquit/check_quick_command_example.png?raw=true)


# Global Server Announcement Rating Updates

The Global Server Announcement is a periodic notification system that occurs every 2 hours within the Discord server. This automated process is designed to provide real-time updates on character rating progress.

## Functionality

1. **Real-Time Updates:** The Global Server Announcement runs every 2 hours, fetching the latest data from Raider.io to identify characters that have gained rating within that time frame.

2. **Channel Customization:** Users have the flexibility to choose the specific Discord channel in which they wish to receive the rating updates.

## Command Usage

1. **Enabling Notifications:** To subscribe to the Global Server Announcement, users need to set up the desired Discord channel to receive the updates, default one is 'iquit-bot''.

2. **Character Progress Tracking:** Once the system is activated, the bot will automatically detect any character that gains rating and promptly notify the specified Discord channel.

## Note

1. **Continuous Monitoring:** The Global Server Announcement continually monitors character achievements, allowing for immediate updates on any rating gains.

2. **Data Accuracy:** The system ensures accurate and up-to-date character data from the Raider.io database.

By utilizing the Global Server Announcement, players can stay informed about their character's progression and gain insights into other players' achievements in real-time, fostering a competitive and engaging community within the Discord server.
![alt text](https://github.com/ceo-py/Project-Pictures/blob/main/Iquit/global_server_announcment_example.png?raw=true)


# Rank Global Setting Command

The `rankglobalsetting` command enables users to add or remove a single custom channel to the bot's database, allowing them to receive global server rank notifications every 2 hours. This custom channel will serve as the destination for the notifications, replacing the default channel 'iquit-bot'. Please note that only one active custom channel is allowed per server at any given time.

## Command Usage

To use the `rankglobalsetting` command, type the following in a server text channel:

```
/rankglobalsetting [option]
```

Replace `[option]` with either "Add" or "Remove" to perform the desired action.

## Options

1. `Add`: Use this option to add the current channel as the custom channel for global rank notifications.

2. `Remove`: Use this option to remove the custom channel from the bot's database, restoring the default channel 'iquit-bot' for notifications.

## Functionality

1. **Adding a Custom Channel:**
   When using the "Add" option, the command will add the current channel as the custom channel for global rank notifications. Subsequently, all global server rank notifications will be sent to this custom channel every 2 hours, replacing the default channel.

2. **Removing a Custom Channel:**
   If you choose the "Remove" option, the command will remove the custom channel from the bot's database. This action will revert the notifications back to the default channel 'iquit-bot'.

## Note

1. **One Custom Channel Limit:**
   Only one custom channel is allowed per server. If you add a new custom channel, the previous one will be replaced, and global rank notifications will be sent to the newly added custom channel.

2. **Maintaining Custom Channel:**
   To maintain the custom channel and continue receiving global rank notifications, use the "Add" option.

3. **Reverting to Default Channel:**
   To revert to the default channel 'iquit-bot' for global rank notifications, use the "Remove" option.

4. **Permissions:**
   Ensure that you have the necessary permissions to interact with the bot and manage channels in the server.

By utilizing the `rankglobalsetting` command with the appropriate options, users can seamlessly manage their custom channel preferences for global rank notifications and tailor the bot's behavior to their preferences in the Discord server.
![alt text](https://github.com/ceo-py/Project-Pictures/blob/main/Iquit/global_server_announcment_adding_custom_channel_example.png?raw=true)


# RankSimple Global Command

The `/ranksimple` command is a powerful tool designed to display the top-rated players for a specific role within the Discord server. By providing two mandatory parameters, namely the role (All, DPS, Heal, or Tank) and the desired number of top players to show (from 1 to 10), users can obtain valuable rating information effortlessly.

## Command Usage

To use the `/ranksimple` command, type the following in a Discord text channel:

```
/ranksimple [role] [top]
```

Replace `[role]` with one of the available options: All, DPS, Heal, or Tank. Additionally, set `[top]` to the desired number of top-rated players to display (ranging from 1 to 10).

## Displayed Information

The `/ranksimple` command will present the following information:

- **Top-Rated Players:** The command will retrieve the highest-rated players for the specified role within the Discord server's character database.

- **Rating Information:** The displayed list will show the players' ratings in descending order, showcasing the highest-rated player at the top.

## Note

1. **Server-Specific Data:** The `/ranksimple` command accesses the character database specific to the Discord server it is used in, ensuring that the ranking information remains relevant and tailored to the server's characters.

2. **Accurate and Up-to-Date:** The command provides real-time rating data, ensuring the latest and most accurate information for the ranked players.

3. **Limitation on Displayed Players:** The maximum number of players shown is based on the `[top]` parameter. Setting `[top]` to 5, for example, will display the top 5 highest-rated players for the chosen role.

The `/ranksimple` command streamlines the process of accessing rating information for specific roles in the Discord server's character database. It serves as a valuable resource for users to identify top-rated players within their server effortlessly.

![alt text](https://github.com/ceo-py/Project-Pictures/blob/main/Iquit/rank_simple_example.png?raw=true)

# RankSimpleLoop Global Command

The `/ranksimpleloop` command offers a convenient way to set up and automate daily rank leaderboard notifications for specific roles in a Discord server's character database. By providing four essential parameters - `hour`, `minute`, `role` (ALL, DPS, Heal, or Tank), and `top` (number of players to display), users can configure the command to trigger daily and display ranking information based on their chosen criteria.

## Command Usage

To use the `/ranksimpleloop` command, enter the following in a Discord text channel:

```
/ranksimpleloop [hour] [minute] [role] [top]
```

1. **`[hour]` and `[minute]`:** Set the specific time (in UTC Zone) when you want the command to trigger and display the daily rank leaderboard.

2. **`[role]`:** Choose one of the available options - ALL, DPS, Heal, or Tank - to filter the ranking based on the desired role.

3. **`[top]`:** Specify the number of top-rated players to show in the leaderboard for the selected role (ranging from 1 to 10).

## Automate Daily Rank Leaderboard

The `/ranksimpleloop` command allows you to automate daily rank leaderboard notifications. Once you set the desired time, the command will display the ranking information based on your criteria every day at the scheduled UTC time. It is crucial to note that the server time is in UTC, so ensure you convert your local time zone to UTC when setting the hour and minute.

## Note

1. **Server-Specific Data:** The `/ranksimpleloop` command accesses the character database specific to the Discord server it is used in, ensuring that the leaderboard displays relevant information for the server's characters.

2. **Accurate and Up-to-Date:** The command provides real-time rating data, ensuring the latest and most accurate information for the ranked players.

3. **Daily Automation:** The command runs daily based on the time you set, ensuring regular updates on character rankings.

The `/ranksimpleloop` command streamlines the process of obtaining daily rank leaderboard information for specific roles in the Discord server. By scheduling the command to trigger at your preferred time, you can effortlessly keep track of top-rated players and their rankings for the chosen role on a daily basis.

![alt text](https://github.com/ceo-py/Project-Pictures/blob/main/Iquit/rank_simple_loop_example.png?raw=true)


# Token Command World of Warcraft Price Information

The `!token` command provides users with valuable information about the current price of World of Warcraft tokens. These tokens can be used in various in-game transactions and hold significant value. The command displays token prices for three different time periods: 1 day, 7 days, and 30 days, including both the lowest and highest prices recorded during each period.

## Command Usage

To use the `!token` command, simply type the following in a Discord text channel:

```
!token [region]
```

Replace `[region]` with one of the available options for the region you wish to check. The available options are:

- US (United States)
- EU (European Union)
- Korea
- Taiwan

## Information Displayed

The `!token` command will provide the following information:

- **3-Day Price Range:**
  The lowest and highest price of the WoW token recorded within the last 3 days in the specified region.

- **7-Day Price Range:**
  The lowest and highest price of the WoW token recorded within the last 7 days in the specified region.

- **30-Day Price Range:**
  The lowest and highest price of the WoW token recorded within the last 30 days in the specified region.

## Note

1. **Real-Time Data:**
   The command fetches real-time data on token prices, providing the latest and most accurate information.

2. **Currency Information:**
   The prices are displayed in the in-game currency of World of Warcraft.

3. **Region Selection:**
   Choose the appropriate region option to view token prices specific to that region.

By using the `!token` command with the desired region parameter, players can stay informed about the fluctuating prices of World of Warcraft tokens, helping them make informed decisions in the in-game economy.

![alt text](https://github.com/ceo-py/Project-Pictures/blob/main/Iquit/toke_price_example.png?raw=true)


# Weather Command

The `!weather` command allows users to obtain real-time weather information about a specific city. By providing the city name as a parameter, the command will fetch and display various weather details, including the current temperature, "feels like" temperature, and the minimum and maximum temperatures for the day.

## Command Usage

To use the `!weather` command, simply enter the following in a Discord text channel:

```
!weather [city_name]
```

Replace `[city_name]` with the name of the city for which you want to retrieve the weather information.

## Information Displayed

The `!weather` command will provide the following weather details:

- **Current Temperature:** The current temperature in degrees Celsius.

- **"Feels Like" Temperature:** The perceived temperature, which factors in other weather elements like humidity and wind, giving a sense of how the weather actually feels.

- **Minimum Temperature:** The lowest temperature expected during the day.

- **Maximum Temperature:** The highest temperature expected during the day.

## Note

1. **Real-Time Data:**
   The command fetches real-time weather data, ensuring that the information provided is up-to-date and accurate.

2. **City Selection:**
   Make sure to enter the correct name of the city to obtain weather information for that specific location.

3. **Temperature Units:**
   The temperature will be displayed in either Celsius, depending on the region's standard unit.


By using the `!weather` command with the desired city name, users can quickly access essential weather information for any location, helping them plan and prepare for their activities accordingly.

![alt text](https://github.com/ceo-py/Project-Pictures/blob/main/Iquit/weather_example.png?raw=true)


# Ask Command

The `!ask` command allows users to ask a wide range of questions and receive answers directly from the bot. The command is designed to handle both simple inquiries, such as basic calculations like "2 + 2," and more specific questions like "When is the next game for a particular sports team?"

## Command Usage

To use the `!ask` command, enter the following in a Discord text channel:

```
!ask [question]
```

Replace `[question]` with your specific question, and the bot will attempt to provide a relevant answer.

## Supported Questions

The `!ask` command is flexible and can handle various types of questions, including:

1. **Simple Calculations:** You can ask the bot to perform basic arithmetic calculations, such as addition, subtraction, multiplication, and division.

2. **Sports Team Information:** The command can also answer questions about sports teams, such as their next game schedule or recent match results.

3. **General Knowledge:** Feel free to inquire about general knowledge topics or seek answers to factual questions.

## Note

1. **Precision of Answers:**
   While the `!ask` command can provide answers to various questions, it may not be capable of answering extremely complex or highly specialized inquiries.

2. **Clear and Concise Questions:**
   To ensure accurate responses, it is recommended to frame your questions clearly and concisely.

3. **Limited Predictive Abilities:**
   The bot may not have predictive capabilities, so questions about future events might be based on available data up to the current time.

The `!ask` command serves as a versatile tool for obtaining quick answers to a wide array of questions, making it a valuable feature for users seeking prompt information or engaging in enjoyable interactions with the bot.

![alt text](https://github.com/ceo-py/Project-Pictures/blob/main/Iquit/ask_command_example.png?raw=true)

# Bot Information and Installation

To explore more commands and features, use `!help` for comprehensive details. The bot exclusively responds in the designated "iquit-bot" channel.

## Installation:

1. [invite](https://discord.com/api/oauth2/authorize?client_id=859492463918972930&permissions=0&scope=bot) the bot to your Discord server.
2. Create a text channel that include the name "iquit-bot" for seamless interaction.

Enjoy the bot's functionalities and make the most of its features to enhance your World of Warcraft experience! 🎮🤖
For more information about commands, you can always use !help.
The bot will only respond in **"iquit-bot"** or if you add custom channel.
