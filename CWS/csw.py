#https://geopython.github.io/OWSLib/index.html
#https://docs.pycsw.org/en/latest/index.html
#https://live.osgeo.org/en/quickstart/pycsw_quickstart.html

#pip3 install pycsw
#sudo apt-get install libgeos-dev

from flask import Flask, request, Response

from pycsw import __version__ as pycsw_version
from pycsw.server import Csw

application = Flask(__name__)

@application.route('/csw')
def csw_wrapper():
    """CSW wrapper"""

    print('Running pycsw %s', pycsw_version)

    pycsw_config = ""#some_dict  # really comes from somewhere

    # initialize pycsw
    # pycsw_config: either a ConfigParser object or a dict of
    # the pycsw configuration
    #
    # env: dict of (HTTP) environment (defaults to os.environ)
    #
    # version: defaults to '3.0.0'
    my_csw = Csw(pycsw_config, request.environ, version='2.0.2')

    # dispatch the request
    http_status_code, response = my_csw.dispatch_wsgi()

    print('Status Code %s',http_status_code)
    print('Response %s',response)

    return response, http_status_code, {'Content-type': pycsw_version}

    #return Response({'Content-type': csw.contenttype})

if __name__ == '__main__':
    application.run(host='172.17.0.3', port=8006)#, debug=True)