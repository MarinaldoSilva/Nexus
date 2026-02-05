import zipfile
import io
from django.core.files.base import ContentFile


def compress_file_lzma(file):
    
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_LZMA, allowZip64=True) as zf:
        zf.writestr(file.name, file.read())
    zip_buffer.seek(0)
    return ContentFile(zip_buffer.getvalue(), name=f"{file.name}.zip")