from flask import Flask, render_template
from flask_socketio import SocketIO, send
from db_util import *

# Deklarasi variabel
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app, cors_allowed_origins='*')

# Apabila menerima pesan dari user maka simpan pesan tersebut 
# Lalu proses pesan apa yang harus dikeluarkan bot dan kirimkan kembali kedua pesan ini untuk diproses di frontend
@socketio.on('message')
def handleMessage(myMsg):
	if (myMsg =="reset"):
		dell_all_chat()
	else:
		add_new_chat(myMsg)
		botMsg = "Perintah tidak dikenal"
		add_new_chat(botMsg,Bot=1)
		message = [myMsg,botMsg]
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
