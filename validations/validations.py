from database.database import db_, os


class Validation:

    @staticmethod
    def check_right_channel(ctx):
        if str(ctx.channel) == os.getenv("DISCORD_CHANNEL_NAME"):
            return True, str(ctx.guild.id), str(ctx.channel.id)
        return False, 0, 0

    @staticmethod
    async def msg_check(ctx):
        right_channel, msg_send, cnl_id = Validation.check_right_channel(ctx)
        if not right_channel:
            await ctx.author.send(
                f"Not Right Channel make sure you create text channel - **{os.getenv('DISCORD_CHANNEL_NAME')}**, and send your commands "
                f"there!")
            return

        channel_data_ = db_.connect_db(cnl_id, msg_check=True).find_one({"Channel Id": cnl_id})
        if not channel_data_:
            db_.save_msg_id(msg_send, cnl_id)

        return cnl_id
