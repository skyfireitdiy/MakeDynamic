import os
from werkzeug.utils import _windows_device_files


def my_secure_filename(filename):
    # if isinstance(filename, text_type):
    #     from unicodedata import normalize
    #     filename = normalize('NFKD', filename).encode('ascii', 'ignore')
    #     if not PY2:
    #         filename = filename.decode('ascii')
    for sep in os.path.sep, os.path.altsep:
        if sep:
            filename = filename.replace(sep, ' ')
    # filename = str(_filename_ascii_strip_re.sub('', '_'.join(
    #     filename.split()))).strip('._')
    if os.name == 'nt' and filename and \
            filename.split('.')[0].upper() in _windows_device_files:
        filename = '_' + filename
    return filename


def valid_image_ext(file_name: str):
    ext = [".jpg", ".jpeg", ".png", ".gif"]
    return os.path.splitext(file_name)[-1] in ext
