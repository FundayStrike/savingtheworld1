from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
  global c
  exist, name, block, block_png, floor, classnum, addinfo, error_msg = False, None, None, None, None, None, None, None
  if request.method == "POST":
    name = request.form["location"].title()
    connection = sqlite3.connect("loc_database.db", check_same_thread=False)
    c = connection.cursor()
    if get_location_details(name) == []:
      error_msg = "Location is not found."
    else:
      exist=True
      location_details = get_location_details(name)
      name, block, classnum, addinfo = location_details[0][0], location_details[0][1], location_details[0][3], location_details[0][4]
      block_png = get_block(block)
      if name == "Easter Egg":
        block_png = "easter-egg.png"
      floor = str(location_details[0][2])
      if len(location_details) > 1:
        for i in range(1, len(location_details)):
          floor += f'/{location_details[i][2]}'
    connection.close()
  return render_template("index.html", exist=exist, name=name, block=block, block_png=block_png, floor=floor, classnum=classnum, addinfo=addinfo, error_msg=error_msg)

def get_location_details(name):
  get_location = "SELECT * FROM location WHERE Name=@0 OR AltName1=@0 OR AltName2=@0"
  c.execute(get_location, [name])
  location = c.fetchall()
  return location

def get_block(block):
  block_list = ['block1.png', 'block2.png', 'block3.png','', 'block5.png', 'block6.png', 'block7.png', 'block8.png', 'block9.png', 'block10.png', 'block11.png', 'block12.png', 'block13.png']
  if block != None:
    return block_list[block-1]

app.run(host='0.0.0.0', port=81)
