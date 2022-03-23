import pathlib
import shutil


def move_files( filename, target ):
    target = pathlib.Path( target )
    raw_file = pathlib.Path( filename )    
    raw_dst = target / raw_file.with_suffix( '' ).name
    meta_file = raw_file.with_suffix( '' ).with_suffix('.meta')
    meta_dst = target / meta_file.name

    print( f'moving {raw_file} to {raw_dst}' )
    print( f'moving {meta_file} to {meta_dst}' )

    shutil.move( str(raw_file ), raw_dst )
    shutil.move( str(meta_file), meta_dst )
