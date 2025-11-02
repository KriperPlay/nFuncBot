

#╭╮╱╱╱╱╱╭━━━╮╱╱╱╭━╮╭━╮
#┃┃╱╱╱╱╱┃╭━╮┃╱╱╱┃╭╯┃╭╯
#┃╰━┳╮╱╭┫╰━╯┣━━┳╯╰┳╯╰╮
#┃╭╮┃┃╱┃┣━━╮┃╭╮┣╮╭┻╮╭╯
#┃╰╯┃╰━╯┣━━╯┃╰╯┃┃┃╱┃┃
#╰━━┻━╮╭┻━━━┻━━╯╰╯╱╰╯
#╱╱╱╭━╯┃
#╱╱╱╰━━╯

import telebot
import numpy as np
import matplotlib.pyplot as plt
import io

import config

bot = telebot.TeleBot(config.API_TOKEN)

plt.switch_backend('Agg')

x = np.linspace(config.XMIN, config.XMAX, config.POINTS)
y1 = 0*x

safe_dict = {
	'x': x,
	'np': np,
	'sin': np.sin,
	'cos': np.cos,
	'tan': np.tan,
	'exp': np.exp,
	'log': np.log,
	'log10': np.log10,
	'sqrt': np.sqrt,
	'abs': np.abs,
	'pi': np.pi,
	'e': np.e
}

def graph(func: str):
	try:
		y = eval(func, {"__builtins__": {}},safe_dict)
		
		plt.plot(x, y,color='black')
		plt.plot(x,y1,color='red')
		plt.axvline(x=0,color='red')
		plt.xlabel('x')
		plt.ylabel('y') 
		plt.title(f'y={func}') 
		plt.grid()
		
		buf = io.BytesIO()
		plt.savefig(buf,format='png')
		buf.seek(0)
		plt.close()
		
		return buf
		
	except Exception as e:
		print(e)


@bot.message_handler(commands=['start'])
def start(message):
	if config.WHITE_LIST:
		if str(message.from_user.id) in config.ID_USERS:
			bot.reply_to(message, config.HELP_TEXT)
		else:
			bot.reply_to(message, config.HELP_TEXT + "\nP.S. You are not in the white list, u cant to use this bot :(")
	else:
		bot.reply_to(message, config.HELP_TEXT)

@bot.message_handler(func=lambda message: True)
def send_graph(message):
	if config.WHITE_LIST:
		if str(message.from_user.id) in config.ID_USERS:
			func_str = message.text.strip()
			image_buffer = graph(func_str)
			
			bot.send_photo(message.chat.id, image_buffer, caption=f"y = {func_str}")
		else:
			bot.reply_to(message,"You are not in the white list")
	else:
		func_str = message.text.strip()
		image_buffer = graph(func_str)
		
		bot.send_photo(message.chat.id, image_buffer, caption=f"y = {func_str}")
	

if __name__ == '__main__':
	bot.infinity_polling()
	