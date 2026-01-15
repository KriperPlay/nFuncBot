

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
	func = func.replace('^', '**')
	print(func)
	try:
		if ';' in func:
			__func = func.split(';')
			for _func in __func:
				y = eval(_func, {"__builtins__": {}},safe_dict)
				plt.plot(x, y,label=f"{_func.strip()}")
		else:
			y = eval(func, {"__builtins__": {}},safe_dict)
			plt.plot(x, y,color='black',label=f"{func}")

		plt.plot(x,y1,color='red')
		plt.axvline(x=0,color='red')
		plt.xlabel('x')
		plt.ylabel('y') 
		plt.title(f'{func.replace(';',' ')}') 
		plt.legend()
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
			image_buffer = graph(message.text.strip())
			
			bot.send_photo(message.chat.id, image_buffer)
		else:
			bot.reply_to(message,"You are not in the white list")
	else:
		image_buffer = graph(message.text.strip())
		
		bot.send_photo(message.chat.id, image_buffer)
	

if __name__ == '__main__':
	bot.infinity_polling()
	