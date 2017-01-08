# minions.py
import falcon
import MySQLdb
import json
import sys

class MinionResource(object):
    def on_post(self, req, resp):
        try:
            raw_json = req.stream.read()
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_400,
                'Error',
                ex.message)

        try:
            result_json = json.loads(raw_json, encoding='utf-8')
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400,
                'Malformed JSON',
                'Could not decode the request body. The '
                'JSON was incorrect.')
        try:
            t = result_json['temp']
            my_id = result_json['id']
            print(t, my_id)
            x.execute("INSERT report (t, id) VALUES (%s, %s)", (t, my_id))
            conn.commit()
        except:
            resp.body = ("negative")
            conn.rollback()
            print 'request error', sys.exc_info()[0]
            return


        resp.status = falcon.HTTP_202
        resp.body = json.dumps(result_json, encoding='utf-8')

conn = MySQLdb.connect(host= "localhost",
                  user="root",
                  passwd="root",
                  db="minion")
x = conn.cursor()

# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
minions = MinionResource()

# things will handle all requests to the '/things' URL path
app.add_route('/minions', minions)
