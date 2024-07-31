



from flask import Flask, request, Response
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)

tele_parameter = None

def generate_output(tele):
    print(tele)
    cmd = ['sh', '-c', f'cd Piano-PIR-new && go run client_new/client_new.go -ip localhost:50051 -thread 1 -n {tele}']
    print(cmd)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    try:
        for line in iter(p.stdout.readline, ''):
            yield f"data: {line}\n\n"
    finally:
        p.stdout.close()
        p.wait()

@app.route('/execute', methods=['POST'])
def execute():
    global tele_parameter
    # 获取tele参数
    tele = int(request.json.get('tele'))
    if tele:
        tele_parameter = tele
        print(tele_parameter)
        return '', 202
    else:
        return 'Missing tele parameter', 400
    # return '', 202

@app.route('/stream', methods=['GET'])
def stream():
    return Response(generate_output(tele_parameter), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, port=5174)
