import zipfile
import io
from django.core.files.base import ContentFile


def compress_file(file, zip_type="MEDIO"):
    
    tipo_zip = {
        'RAPIDO': zipfile.ZIP_STORED,
        'MEDIO': zipfile.ZIP_DEFLATED, 
        'FORTE': zipfile.ZIP_LZMA
    }
    
    if zip_type not in tipo_zip:
        raise ValueError(f"Tipo incorreto, escolha entre: {tipo_zip.keys()}")
    
    compactar = tipo_zip[zip_type]
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', compactar, allowZip64=True) as zf:
        zf.writestr(file.name, file.read())
    zip_buffer.seek(0)
    return ContentFile(zip_buffer.getvalue(), name=f"{file.name}.zip")