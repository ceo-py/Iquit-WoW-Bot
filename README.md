A little bot that I made, so we can use it with my friends and check our progress, among other useful information about WOW.


You can test the bot functionality [here](https://discord.gg/gCcfWpMCgE)

Commands:

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
![alt text](https://cdn.discordapp.com/attachments/983670671647313930/1058493214610444449/image.png)


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

![alt text](https://cdn.discordapp.com/attachments/983670671647313930/1111980276764123227/image.png)


```code
!rank
```

With that, you'll be able to see every character that you added in the bot with !add ranked and compare to the rest of the characters. If there are characters with 0 RIO they will not show. As an additional option, you have at the bottom to see the top 20 of every role and total.
![alt text](https://cdn.discordapp.com/attachments/983670671647313930/1058492082647474226/image.png)

```code
!check {region} {realm} {character name}
```

![alt text](https://cdn.discordapp.com/attachments/983670671647313930/1058499360758960158/image.png)

With that command, you'll be able to see more detail information about the character you ask for.

```code
!check {nickname} {class}
```

This is a quick check that you don't need to type {region} {realm} {character name} this will only work if you already add that character into the bot by **!add {region} {realm} {character name} {your nickname in discord, wow etc..} {class}**. If the character is not added to the bot, you can simply use then full check by **!check {region} {realm} {character name}**
![alt text](https://preview.redd.it/bcx6f5ybgwl71.png?width=668&format=png&auto=webp&s=11246511f815473c2f1f78454c8d428dd22d4015)



# Global Server Announcement - Rating Updates

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
![alt text](https://cdn.discordapp.com/attachments/983670671647313930/1060516253996945428/image.png)


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
![alt text](https://cdn.discordapp.com/attachments/983670671647313930/1132373752785686538/image.png)


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

![alt text](https://cdn.discordapp.com/attachments/983670671647313930/1132385453887201280/image.png)

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

![alt text](https://cdn.discordapp.com/attachments/983670671647313930/1132392621101289532/image.png)


# Token Command - World of Warcraft Price Information

The `!token` command provides users with valuable information about the current price of World of Warcraft tokens. These tokens can be used in various in-game transactions and hold significant value. The command displays token prices for three different time periods: 1 day, 7 days, and 30 days, including both the lowest and highest prices recorded during each period.

## Command Usage

To use the `!token` command, simply type the following in a Discord text channel:

```
!token [region]
```

Replace `[region]` with one of the available options for the region you wish to check. The available options are:

- US (United States)
- EU (European Union)
- China
- Korea
- Taiwan

## Information Displayed

The `!token` command will provide the following information:

- **1-Day Price Range:**
  The lowest and highest price of the WoW token recorded within the last 24 hours in the specified region.

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

![alt text](https://preview.redd.it/fo0ehrpcgwl71.png?width=681&format=png&auto=webp&s=26d45b61ff1d946585f0ed3bfd81faca756a72fc)


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

![alt text](https://preview.redd.it/vjyah4ndgwl71.png?width=531&format=png&auto=webp&s=5cc256a105183703d35e59edea971efd97c7d461)


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

![alt text](https://preview.redd.it/9yyw3n7fgwl71.png?width=534&format=png&auto=webp&s=74097e31ce9ea73f39cf07387425bf7fe78b3966)


For more information about commands, you can always use !help.
The bot will only respond in **"iquit-bot"** channel.
Installation:
1. From here you can [invite](https://discord.com/api/oauth2/authorize?client_id=859492463918972930&permissions=0&scope=bot) the bot to your discord server
2. After that create text channel iquit-bot

![alt text](https://preview.redd.it/33k6h2fknwl71.png?width=294&format=png&auto=webp&s=0d3510bb3beb37e6476edcb2ebd3297b131bbb0d)

3. **!help** for more information about commands.
That's it, you can enjoy it :)