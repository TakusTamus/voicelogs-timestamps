from .nicknamerr import NickNamerr

async def setup(bot):
    await bot.add_cog(NickNamerr(bot))
