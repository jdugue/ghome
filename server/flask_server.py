from flask import Flask, request
app = Flask (__name__)

@app.route("/actionneur", methods=["GET"])
def actionneur():
	if 'id_actionneur' in request.args:
		id_actionneur = request.args.get('id_actionneur','')
		#appeler fonction qui allume/eteint l'actionneur
		return 'Hello id_actionneur: {}'.format(id_actionneur)
	else:
		return 'Pas d\'id actionneur'

if __name__ == '__main__':
    app.run()