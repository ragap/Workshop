#import urllib.request
import feedparser
import webbrowser

#def get_fuel_watch_xml(product,brand,region,suburb,surrounding,date):

def generate_url():

    # Declaring an empty list
    link = ["http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?Product=2&Region=26",
            "http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?Product=2&Region=26&Day=tomorrow",
            "http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?Product=2&Region=25",
            "http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?Product=2&Region=25&Day=tomorrow"
            ]
    
    return(link)

def get_data():

    # Declaring emply dictionary and list to store feed data
    dic_data={}
    list_data =[]

    #Get the List of URL's to Parse
    list = generate_url()
    print (list)


    #Parse the url's in list using feedparser
    for url in list:
        list_parse = feedparser.parse(url)

        # channel elements are available in fuel.feed
        title = list_parse.feed.title
        print (title)
        print (list_parse.feed.link)
        print (list_parse.feed.description)


        # item elements are available in x.entries
        for i in list_parse.entries:
            dic_data = {
                        'Price' : i.price ,
                        'Location':i.location,
                        'Address':i.address,
                        'phone':i.phone,
                        'brand' :i.brand,
                        'date' : i.date
                       }

            list_data.append(dic_data)
            list_data = sorted(list_data, key=lambda k: k['Price'])

        # Declare a string to hold table row data
        Table_body = ''

        for i in list_data:
            table_row ="<tr><td>{Price}</td><td>{Location}</td><td>{Address}</td><td>{phone}</td><td>{brand}</td><td>{date}</td></tr>".format(**i)
            #%(i['Price'],i['Location'],i['Address'],i['phone'],i['brand'],i['date'])
            Table_body += table_row


        # Create Template to hold HTML Data
        template = """<html>
                              <head>
                              </head>
                              <body>
                                <h2>"Fuel Prices For all metro regions" </h2>
                                <table border = "1">
                                   <thead>
                                      <tr>
                                         <th>Price</th>
                                         <th>Location</th>
                                         <th>Address</th>
                                         <th>Phone</th>
                                         <th>Brand</th>
                                         <th>Date</th>
                                       </tr>
                                 </thead>
                          <tbody> {}
                          </tbody>
                       </table>
                          </body>
                          </html>""".format(Table_body)




    #Open File to write HTML Data
    # using "With"  statement , no need to close the file explictly
    with open('fuelwatch.html','w') as f:
        f.write(template)

#Change path to reflect file location
filename = "E:\Material\Django\Fuelwatch\fuelwatch.html" 
webbrowser.open_new_tab(filename)

get_data()
