from fuelapp import app
from flask import request,render_template
import feedparser
import itertools

def generate_url(Product,Region):
    link = []
    for i  in itertools.product(Product,Region):
        gen_url = ("http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?Product={}&Region={}".format(*i))
        link.append(gen_url)
    return (link)

@app.route('/',methods=['GET'])
def index():
     # if request.method == 'GET':
    if request.args :
        print(request.args)
        url,list_data=get_data(request.args['Product'],request.args['metroregion'])
        return render_template('results.html',url = url,list_data = list_data)
    return render_template('search.html')

# (product,brand,region,suburb,surrounding,date):
@app.route('/results/',methods=['GET'])
def get_data(Product,Region):

   # if request.method == 'POST':
   #   Producttype = request.form['Product']
   #   metroRegion = request.form['metroregion']
   #   print(Producttype)
   #   print(metroRegion)

   # Process valid POST
   if request.method == 'GET':
     # Declaring emply dictionary and list to store feed data
     # dic_data={}
     list_data =[]

     #Get the List of URL's to Parse
     #Delcare a list


     url = generate_url([Product],[Region])

     #Parse the url's in list using feedparser
     for i in url:
        list_parse = feedparser.parse(i)

        # channel elements are available in fuel.feed
        # title = list_parse.feed.title

        # item elements are available in x.entries
        for i in list_parse.entries:
            dic_data = {
                        'Price' : i.price,
                        'Location':i.location,
                        'Address':i.address,
                        'Phone':i.phone,
                        'Brand' :i.brand,
                        'Date' : i.date
                       }

            list_data.append(dic_data)
            list_data = sorted(list_data, key=lambda k: k['Price'])
        return url,list_data


# @app.errorhandler(404)
# def page_not_found(e):
#     code = '404'
#     return render_template('error.html', code=code), 404
#
# @app.errorhandler(500)
# def internal_server_error(e):
#     code = '500'
#     return render_template('error.html', code=code), 500
#
# @app.errorhandler(503)
# def service_unavailable(e):
#     code = '503'
#     return render_template('error.html', code=code), 503
