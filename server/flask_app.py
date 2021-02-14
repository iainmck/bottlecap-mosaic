from flask import Flask, request, jsonify, send_file
from Errors import *
from main import makeCapMosaic

app = Flask(__name__)

@app.route('/')
def index():
    return 'Cap server 1.0'

@app.route('/process', methods=['POST'])
def process():
    postData = request.get_json()
    print "/process POST PARAMS"
    print request.get_json()

    if 'caps_list' not in postData.keys() or \
     'image_url' not in postData.keys() or \
     'caps_wide' not in postData.keys():
        raise RequestError('Missing request params "caps_list" or "image_url" or "caps_wide".', 400)

    try:
        if 'starting_bin_width' in postData.keys():
            capMosaic = makeCapMosaic(postData['caps_list'], postData['image_url'], int(postData['caps_wide']),
                          startingBinWidth=int(postData['starting_bin_width']))
        else:
            capMosaic = makeCapMosaic(postData['caps_list'], postData['image_url'], int(postData['caps_wide']))

        return send_file(capMosaic, mimetype='image/png')

    except BadImageLinkError:
        raise RequestError('Image could not be found at specified url.', 400)
    except BadImageFiletypeError:
        raise RequestError('Image must be of filetype .jpg or .png.', 400)
    except FilesizeError:
        raise RequestError('Maximum filesize of 2 Megabytes surpassed.', 400)
    except BadImageError:
        raise RequestError('Image could not be processed, please try another image (Check that image does not have transparent background).', 400)

@app.errorhandler(RequestError)
def handleRequestError(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

if __name__ == "__main__":
    app.run()