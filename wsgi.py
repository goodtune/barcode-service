import json
import os
import StringIO
import sys

import magic
import zbar
from PIL import Image

ALLOWED_MIME_TYPES = {
    'image/jpeg',
    'image/png',
}


def extract_barcodes(data):
    """
    Given image data, attempt to identify any barcodes present in the image.

    :param data: binary data
    :return: iterable of :class:`dict`
    """
    scanner = zbar.ImageScanner()
    scanner.parse_config('enable')

    pil = Image.open(StringIO.StringIO(data)).convert('L')
    width, height = pil.size
    raw = pil.tobytes()

    image = zbar.Image(width, height, 'Y800', raw)
    scanner.scan(image)

    for symbol in image:
        yield {
            'symbol': unicode(symbol.type),
            'value': symbol.data,
        }


def application(environ, start_response):

    data = environ['wsgi.input'].read()
    mime = magic.from_buffer(data, mime=True)

    if mime in ALLOWED_MIME_TYPES:
        start_response('200 OK', [('Context-Type', 'application/json')])
        yield json.dumps([each for each in extract_barcodes(data)])

    else:
        start_response('400 Bad Request', [('Context-Type', 'application/json')])
        yield json.dumps({'error': 'mime type "%s" not allowed' % mime})
