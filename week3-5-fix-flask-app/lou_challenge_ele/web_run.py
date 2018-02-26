from flask import Flask, request, render_template
from ele import ele_red_packet

app = Flask(__name__)


@app.route('/')
def form():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def phone_number_form():
    phone_number = request.form['phone']
    get_red_packet = ele_red_packet(phone_number)
    return render_template('index.html', phone_number=get_red_packet)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
