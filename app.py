import logging
import time
import yaml
import os

from flask import Flask, render_template, Response, request

app = Flask(__name__)
logging.basicConfig(filename='access.log', filemode='w', level=logging.INFO)

class Config(dict):
    def __init__(self, config_path='config.yaml'):
        self.config_path = config_path
        self.file_hash = os.path.getmtime(config_path)
        super(Config, self).__init__(yaml.load(open(config_path)))
        logging.info("CONFIG: " + str(self))

    def _file_changed(self):
        new_hash = os.path.getmtime(self.config_path)
        change = self.file_hash != new_hash
        self.file_hash = new_hash
        return change

    def _reload(self):
        if not self._file_changed():
            return

        # reload variables everytime so you don't have to restart server
        # goal is also not to crash on bad config
        try:
            new_config = yaml.load(open(self.config_path))
            super(Config, self).__init__(new_config)
            logging.debug("CONFIG: " + str(self))
        except yaml.parser.ParserError:
            logging.error('Configuration File Parse Error. Still using previous file')

    def __repr__(self):
        self._reload()
        return dict.__repr__(self)

    def __getitem__(self, key):
        self._reload()
        # Capitalize since Yaml looks better with caps and python better in lower case.
        return super(Config, self).__getitem__(key.capitalize())

    def __setitem__(self, key, val):
        raise NotImplementedError


config = Config()
door_timeout = 0

@app.route('/call', methods=['GET'])
def play_tone():
    global door_timeout

    if door_timeout > time.time() or config['party']:
        door_timeout = 0
        logging.info("Call. Letting someone in.")
        response = render_template('call-success.xml')
    else:
        logging.info("Call. Redirecting.")
        response = render_template('call-failure.xml', number=config['admin'])

    return Response(response, mimetype='text/xml')


@app.route('/sms', methods=['POST'])
def get_number():
    global door_timeout

    number, body = request.form['From'], request.form['Body']

    if int(number[1:]) in config['users'] or (config['password'] and body == config['password']):
        door_timeout = time.time() + config['timeout'] * 60
        logging.info("SMS. Good. Number: " + number)
        response = render_template('sms-success.xml')
    else:
        logging.info("SMS. Bad. Number: " + number)
        response = render_template('sms-failure.xml')

    return Response(response, mimetype='text/xml')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
