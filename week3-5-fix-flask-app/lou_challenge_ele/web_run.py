from flask import Flask, render_template, request
from ele import ele_red_packet

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('index.html')

@app.route('/', methods=['post'])
def phone_number_form():
    phone_number = request.form['phone']
    get_red_packet = ele_red_packet(phone_number)
    return render_template('index.html', phone_number=get_red_packet)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
