import os, json
import flask
from PIL import Image, ImageFont, ImageDraw
from flask_cors import CORS
from io import BytesIO

app = flask.Flask(__name__, template_folder='training')
# CORS(app)

def read_json(f):
    with open(f) as f:
        data = json.load(f)
    return data

# @app.route("/")
# def index():
#     return "Efico Certificate Generate, Navigate to /certificate/<email>, remove everything after @ in the email"


@app.route("/certificate/<email>")
def generate(email):
    certificate = {
        'Image Path': "Path not found, it seems your email is not authorized"
    }
    for data in read_json('detailsList.json'):
        if email.lower() == data['email'].split('@')[0].lower():
            certificate = make_certificate(data['name'])
            break
    return certificate

@app.route('/')
def home():
    return flask.render_template('certificate.html')

@app.errorhandler(404)
def not_found(e):
    msg = flask.jsonify({
        'error': 'Page or endpoint not found'
    })
    return msg, 404

@app.errorhandler(400)
def bad_request(e, message):
    msg = flask.jsonify({
        'error': 'Bad request, might be that you sent an invalid email'
    })
    if message:
        msg['message'] = message
    return msg, 400

@app.errorhandler(500)
def server_error(e):
    msg = flask.jsonify({
        'error': 'Server error',
        'message': 'Something went trong, Our developers have been contacted!'
    })
    return msg, 500

@app.route('/certificate', methods=['POST'])
def post_certificate():
    data = flask.request.get_json()
    email = data['email']
    if email == 'koikibabatunde14@gmail.com':
        # url = ''
        # response = requests.post(url, json={'email': email})
        # if response.status_code == 200:
            # name = response.json()['fullname']
        # else: 
            # flask.abort(400)
        name = 'Babatunde Koiki'
        try:
            certificate = make_certificate(name)
            certificate.headers['Accept']='image/PNG'
        except Exception as e:
            flask.abort(500)
        else: return certificate
    else:
        data = flask.jsonify({
        'error': 'Bad request',
        'message': 'Invalid email address'
    })
        data.status_code = 400
        flask.abort(data)

def make_certificate(name, date=None):
    def draw_text(filename, name, date):
        font_name = "LibreBaskerville-Italic.otf"
        font_date = "static/Raleway-Medium.ttf"
        color = "#3b181d"
        size = 30
        y = 290
        x = 0
        text_name = "{}".format(name).upper()
        raw_img = Image.open(filename)
        img = raw_img.copy()
        draw = ImageDraw.Draw(img)
        W, H = img.size
        date = 'SEPTEMBER 30TH, 2020' if not date else date
        
        # write name
        PIL_font_name = ImageFont.truetype(os.path.join("static/fonts", font_name), size)
        w, h = draw.textsize(text_name, font=PIL_font_name)
        x = 305 + (W - 305 - w)/2 if x == 0 else x
        draw.text((x, y), text_name, fill=color, font=PIL_font_name)

        # write date
        PIL_font_date = ImageFont.truetype(os.path.join("static/fonts", font_date), 10)
        w, h = draw.textsize(date, font=PIL_font_date)
        x = W/3 + 10
        draw.text((x, y+120), date, fill=color, font=PIL_font_date)

        #saving image as byte
        imgbyte = BytesIO()
        img.save(imgbyte, format='PNG')
        return  BytesIO(imgbyte.getvalue())

    imgByte = draw_text('certificate.png', name, date)    
    filename = "{}.png".format(('-').join(name.split(' ')))
    return flask.send_file(imgByte,     
            as_attachment=True,
            attachment_filename=filename)

if __name__ == "__main__":
    app.run(debug=True)