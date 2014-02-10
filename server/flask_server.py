from flask import Flask, request
import requests
app = Flask (__name__)

@app.route("/actionneur", methods=["GET"])
def actionneur():
	if 'id_actionneur' and 'action' in request.args:
		id_actionneur = request.args.get('id_actionneur','')
		action = request.args.get('action','')
		#appeler fonction qui allume/eteint l'actionneur
		return 'Hello id_actionneur: {}, action : {}'.format(id_actionneur,action)
	else:
		return 'Pas d\'id actionneur'

@app.route("/learning", methods=["GET"])
def learning():
	if 'id_actionneur' in request.args:
		id_actionneur = request.args.get('id_actionneur','')
		#appeler fonction qui allume/eteint l'actionneur
		return 'Hello id_actionneur: {}'.format(id_actionneur)
	else:
		return 'Pas d\'id actionneur'

if __name__ == '__main__':
	#on envoie une requete au server pour savoir si on continue
	url = 'http://127.0.0.1:8000/login_client/'
	params = {'user':'1000', 'password': 'coucou'}
	r = requests.post(url, params=params)  
	if r.status_code == requests.codes.ok:
		data = json.loads(r.text)
	app.run(debug=True)
