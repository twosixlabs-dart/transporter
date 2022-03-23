import argparse
import time

from transporter.files import move_files
from transporter.ladle import upload_ladle
from transporter.watcher import FileWatcher


def parse_inputs():
    parser = argparse.ArgumentParser( description = 'transporter' )
    parser.add_argument( '--source', required = True, type = str )
    parser.add_argument( '--target', required = True, type = str )
    parser.add_argument( '--patterns', required = True, type = str )
    parser.add_argument( '--host', required = True, type = str )
    parser.add_argument( '--port', required = True, type = int )
    return parser.parse_args()


def main():
    args = parse_inputs()
    def upload_action( source_file: str, target_dir: str = args.target, host = args.host, port = args.port ):
        if upload_ladle( source_file, host, port ):
            print( f'successfully processed file {source_file} -> {target_dir}' )
            move_files( source_file, target_dir )
        else:
            print( f'error processing file {source_file}' )

    print( f'starting file watcher on {args.source} for patterns ${args.patterns.strip().split( "," )}' )

    document_watcher = FileWatcher( args.source, args.patterns.strip().split( ',' ), upload_action )
    document_watcher.start()

    try:
        while True:
            time.sleep( 1 )
    except KeyboardInterrupt:
        document_watcher.stop()


if __name__ == "__main__":
    main()
