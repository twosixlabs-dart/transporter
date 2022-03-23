import pathlib
import tempfile
import time
import unittest
from transporter.watcher import FileWatcher


class TransporterTest( unittest.TestCase ):
    def __init__( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )

    def test_transporter_detect_file( self ):
        with tempfile.TemporaryDirectory() as source:
            test_file = f'{source}/test.test'

            def action( source, dest ):
                assert source == test_file
                
            watcher = FileWatcher( source, list( "test" ), action )
            watcher.start()
            
            pathlib.Path( test_file ).touch()
            time.sleep( 1 )


if __name__ == '__main__':
    unittest.main()