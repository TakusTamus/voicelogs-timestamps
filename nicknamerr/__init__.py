from .nicknamerr import nicknamerr


async def setup(bot):
    await bot.add_cog(nicknamerr(bot))
