from flask import Flask, render_template
from flask_socketio import SocketIO, send
from util import *
from chat_process import *

# Deklarasi variabel
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app, cors_allowed_origins='*')

# Apabila menerima pesan dari user maka simpan pesan tersebut 
# Lalu proses pesan apa yang harus dikeluarkan bot dan kirimkan kembali kedua pesan ini untuk diproses di frontend
@socketio.on('message')
def handleMessage(myMsg):
	formatMsg = myMsg.replace('\n', '<br> ')
	if (not("--resetChat" in myMsg)):
		add_new_chat(formatMsg)
	botMsg = process_user_chat(myMsg.replace('\n', ''))
	if ("--resetChat" in myMsg):
		send(["--resetChat","--resetChat"], broadcast=True)
	if (botMsg != ""):
		add_new_chat(botMsg,Bot=1)
		message = [formatMsg,botMsg]
		send(message, broadcast=True)
		
		
		
	
# Route untuk aplikasi yang dibuat
@app.route("/")
def index():
	# Merender halaman utama
	messages = get_all_chat()
	return render_template('index.html', messages=messages)

# Menjalankan socketio
if __name__ == '__main__':
	socketio.run(app,debug=True)
