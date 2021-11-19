from flask import Flask, request, render_template
import webcolors

app = Flask(__name__)

import board
import adafruit_dotstar as dotstar

current_color_hex = ''


@app.route("/")
def index():
    f = open('state', 'r')
    hex_color = f.read()
    f.close()
    return render_template('dotstar_control.html', current=hex_color)


@app.route("/", methods=['POST'])
def set_dotstar():
    #red = int(request.form["red"])
    #green = int(request.form["green"])
    #blue = int(request.form["blue"])
    rgb = webcolors.hex_to_rgb(request.form["hex_color"])
    dots = dotstar.DotStar(board.SCK, board.MOSI, 84, brightness=0.2)
    #dots.fill((red, green, blue))
    dots.fill(rgb)
    #    current_color_hex = request.form["hex_color"]
    f = open('state', 'w')
    f.write(request.form["hex_color"])
    f.close()
    return render_template('dotstar_control.html', current=current_color_hex)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

