import discord
import os
import asyncio
import random
from discord.ext import commands
from datetime import datetime

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

async def status_task():
    while True:
        types = "1", "2", "3", "4"
        choice = random.choice(types)
        if choice == "2":
            await client.change_presence(activity=discord.Activity(type=1, name="Made by PJW#7777", url='https://twitch.tv/twitch'))
        elif choice == "3":
            await client.change_presence(activity=discord.Activity(type=1, name="관리자에게 DM 금지", url='https://twitch.tv/twitch'))
        else:
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="문의 / 신고 DM"))
        await asyncio.sleep(15)

@client.event
async def on_ready():
    print('마대전_로그인 완료')
    print(client.user)
    await client.loop.create_task(status_task())

@client.event
async def on_message(ctx):
    if not ctx.author.bot:
        if ctx.guild == None:
            server = client.get_guild(1014428203219173396)
            
            go = True
            
            for channel in server.channels:
                if channel.name == "문의-" + str(ctx.author.id):
                    await ctx.channel.send("```fix\n추가 메세지가 전송되었습니다.```")
                    try:
                        await channel.send("**추가 메세지 | 내용: " + ctx.content + "**\n사진: " + ctx.attachments[0].url)
                    except IndexError:
                        await channel.send("**추가 메세지 | 내용: " + ctx.content + "**")
                    go = False
                    break

            if go:            
                embed=discord.Embed(title=":grey_question: 문의 종류를 선택해주세요.", description=":one: : 디코 문의\n:two: : 유전 신고\n:three: : 질문\n:four: : 건의\n:five: : 기타\n\n숫자로 작성해주세요.", color=0xf5f5f5)
                msg = await ctx.channel.send(embed=embed)

                def check(m):
                    return m.author == ctx.author

                try:
                    check_text = await client.wait_for('message', timeout=60.0, check=check)
                except asyncio.TimeoutError:
                    embed=discord.Embed(title=":x: 시간 초과", description="응답 시간을 초과하였습니다. 다시 시도해주세요.", color=0xff0a0a)
                else:            
                    
                    if check_text:
                        
                        if check_text.content == "1":
                            category = discord.utils.get(server.categories, name="[디코 문의] 문의")
                        elif check_text.content == "2":
                            category = discord.utils.get(server.categories, name="[유저 신고] 문의")
                        elif check_text.content == "3":
                            category = discord.utils.get(server.categories, name="[질문] 문의")
                        elif check_text.content == "4":
                            category = discord.utils.get(server.categories, name="[건의] 문의")
                        elif check_text.content == "5":
                            category = discord.utils.get(server.categories, name="[기타] 문의")
                        else:
                            await msg.delete()
                            return await ctx.channel.send("```fix\n잘못된 응답입니다.```")
                    
                    await msg.delete()
                            
                    channel = await server.create_text_channel("문의-" + str(ctx.author.id), category=category)

                    embed=discord.Embed(title=":white_check_mark: 문의 사항이 정상적으로 접수되었습니다.", description="관리자가 확인중입니다, 잠시만 기다려주세요.", color=0x42ff4f)
                    embed.set_footer(text="* 욕설, 비방적 내용 등을 포함한 문의는 제재 대상 입니다.")
                    await ctx.channel.send(embed=embed)

                    try:
                        await channel.send("||@here|| **문의 사항이 도착했습니다!**\n*문의자: " + ctx.author.display_name + "(" + str(ctx.author.id) + ")*\n\n내용: **" + ctx.content + "**\n사진: " + ctx.attachments[0].url)
                    except IndexError:
                        await channel.send("||@here|| **문의 사항이 도착했습니다!**\n*문의자: " + ctx.author.display_name + "(" + str(ctx.author.id) + ")*\n\n내용: **" + ctx.content + "**")
                
        else:
            split = ctx.channel.name.split("-")
            if split[0] == "문의":
                user = client.get_user(int(split[1]))
                if user:
                    if ctx.content == "종료":
                        message_log = []
                        async for message in ctx.channel.history():
                            message_log.append(message)
                        message_log.reverse()
                        message_string = ""
                        for m in message_log:
                            message_string = message_string + "\n**" + m.author.display_name + "**: ``" + m.content + "``"
                        log_channel = client.get_channel(1014428204020269075)
                        await log_channel.send("**[" + user.display_name + "님과의 문의 로그]**\n" + message_string)
                        embed=discord.Embed(title=":x: 관리자가 문의를 종료했습니다.", description="만족스러운 답변이 되셨길 바랍니다.", color=0xff4242)
                        embed.set_footer(text="항상 노력하는 마카롱서버가 되겠습니다.")
                        embed.timestamp = datetime.datetime.now(datetime.UTC)
                        await user.send(embed=embed)
                        await ctx.channel.send("* 문의를 종료했습니다.\n* 채널이 5초 뒤 삭제됩니다.")
                        await asyncio.sleep(5)
                        await ctx.channel.delete()
                    else:
                        embed=discord.Embed(title="관리자의 답변이 도착했습니다!", description="< 내용 >```" + ctx.content + "```", color=0x4258ff)
                        embed.set_footer(text="항상 노력하는 마카롱서버가 되겠습니다.")
                        embed.timestamp = datetime.datetime.now(datetime.UTC)
                        try:
                            await user.send("사진: " + ctx.attachments[0].url, embed=embed)
                        except IndexError:
                            await user.send(embed=embed)
                        await ctx.channel.send("* 답변이 전송되었습니다.\n* 문의를 종료하시고 싶으시면 '종료' 라고 입력해주세요!")
                else:
                    pass
            else:
                pass
    else:
        pass 

print("TOKEN:", os.environ.get('DISCORD_BOT_TOKEN'))
client.run(os.environ.get('DISCORD_BOT_TOKEN'))