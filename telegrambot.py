from pyrogram import Client, Filters
from pyrogram import ForceReply, InputMediaPhoto
from virustotal import virus
import time, os
import math
msgdic={}


app = Client("hey",123456,"client_secret within"" ",  bot_token="add_your_bot_token within"" ")


def progress(client, current, total, message_id, chat_id, start):
	now = time.time()
	diff = now - start
	if round(diff % 5.00) == 0 or current == total:
		percentage = current * 100 / total
		speed = current / diff
		elapsed_time = round(diff) * 1000
		time_to_completion = round((total - current) / speed) * 1000
		estimated_total_time = elapsed_time + time_to_completion
		elapsed_time = TimeFormatter(milliseconds=elapsed_time)
		estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)
		progress = "[{0}{1}] \nPercentage: {2}%\n".format(
			''.join(["█" for i in range(math.floor(percentage / 5))]),
			''.join(["░" for i in range(20 - math.floor(percentage / 5))]),
			round(percentage, 2)
		)
		tmp = progress + "{0} of {1}\nSpeed: {2}/s\nETA: {3}\n".format(
			humanbytes(current),
			humanbytes(total),
			humanbytes(speed),
			estimated_total_time if estimated_total_time != '' else "0 s"
		)
		try:
			client.edit_message_text(
				chat_id,
				message_id,
				text="Downloading...\n {}".format(tmp)
			)
		except:
			pass

def humanbytes(size):
	if not size:
		return ""
	power = 2**10
	n = 0
	Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
	while size > power:
		size /= power
		n += 1
	return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'

def TimeFormatter(milliseconds: int) -> str:
	seconds, milliseconds = divmod(int(milliseconds), 1000)
	minutes, seconds = divmod(seconds, 60)
	hours, minutes = divmod(minutes, 60)
	days, hours = divmod(hours, 24)
	tmp = ((str(days) + "d, ") if days else "") + \
		((str(hours) + "h, ") if hours else "") + \
		((str(minutes) + "m, ") if minutes else "") + \
		((str(seconds) + "s, ") if seconds else "") + \
		((str(milliseconds) + "ms, ") if milliseconds else "")
	return tmp[:-2]

@app.on_message(Filters.document)
def download_telegram_media(client, message):

    msg = client.send_message(
      chat_id=message.chat.id,
      text='Download is being started...\nPlease Wait !'
    )
    start_time = time.time()
    download_location = client.download_media(
      message=message,
      file_name='./',
      progress=progress,
      progress_args=(
        msg.message_id,
        message.chat.id,
        start_time
      )
    )
    userid=message.from_user.id
    client.delete_messages(userid,msg.message_id)
    print('a')
    check_size(download_location,userid)
    print('b')

def send_msg(user,txt):
  app.send_message(user,txt,parse_mode="markdown")
  


def check_size(path,userid):
	viruslist = []
	reasons=[]
	b=os.path.getsize(path)
	print('file size is',b)
	obj=virus(str(path))
	if b>32*1024*1024:
		send_msg(userid,'Sorry This file is larger than 32Mb')
		return
		obj.large_files()
	else:
		obj.smallfiles()
	if obj.res==False:
		send_msg(userid,'Error')
	send_msg(userid,obj.verbose)
	time.sleep(7)
	obj.get_report()
	for i in obj.report:
		
		if obj.report[i]['detected']==True:
			viruslist.append(i)
			reasons.append('➤ '+obj.report[i]['result'])
	if len(viruslist) > 0:
		names=' , '.join(viruslist)
		reason='\n'.join(reasons)
		send_msg(userid,'\n☣ --Threats have been detected !-- ☣\n\n**{}** \n\n\n**Description**\n\n`{}`\n\n[Detailed Report]({})'.format(names,reason,obj.link))
	else:
		send_msg(userid,'✔️ File is clean ')

app.run()