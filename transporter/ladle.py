import pathlib
import time
import requests


def upload_ladle( filename, host, port ) -> bool:
    raw_filepath = pathlib.Path( filename )
    metadata_filepath = raw_filepath.with_suffix( '' ).with_suffix( '.meta' )

    for _ in range( 5 ):
        if raw_filepath.exists() and metadata_filepath.exists():
            break
        print( f'waiting for {raw_filepath} and {metadata_filepath} to become available' )
        time.sleep( 1 )
    else:
        raise RuntimeError( f'could not find both {raw_filepath} and {metadata_filepath}' )

    with __resolve_file__( raw_filepath ) as raw_file:
        with open( metadata_filepath ) as meta_file:
            meta_json = meta_file.read()
        post_files = { "file": ( raw_filepath.with_suffix( '' ).name, raw_file ), "metadata": ( None, meta_json, 'application/json' ) }
        try:
            ladle_path = 'factiva' if 'factiva' in filename else 'file'
            endpoint = f'http://{host}:{port}/submit/{ladle_path}'
            response = requests.post( endpoint, files = post_files )
            if response.status_code == 200:
                return True
            else:
                print( f'failed to invoke the ladle service {response.status_code}, {response.text}' )
                return False
        except Exception as e:
            print( e )
            return False


def __resolve_file__( filename: str, mode: str = 'r' ):
    try:
        with open( filename, mode = mode ) as f:
            f.read()
        return open( filename, mode = mode )
    except UnicodeDecodeError as e:
        return __resolve_file__( filename, 'rb' )
