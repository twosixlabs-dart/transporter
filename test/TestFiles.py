import pathlib
import shutil
import tempfile
import unittest
from transporter.files import move_files


class FilesTest( unittest.TestCase ):
    def __init__( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.test_raw_file = 'test/resources/test.pdf.raw'
        self.test_meta_file = 'test/resources/test.meta'
    
    def test_move_files( self ):
        with open( self.test_raw_file, mode = 'rb' ) as test_raw_file, open( self.test_meta_file, mode = 'r' ) as test_meta_file:
            with tempfile.TemporaryDirectory() as tempdir_src, tempfile.TemporaryDirectory() as tempdir_dst:
                src = pathlib.Path( tempdir_src )
                dst = pathlib.Path( tempdir_dst )
                raw = src / 'test.pdf.raw'
                meta = src / 'test.meta'
                shutil.copyfile( self.test_raw_file,  str( raw ) )
                shutil.copyfile( self.test_meta_file, str( meta ) )

                move_files(str(raw), tempdir_dst)
                r = pathlib.Path( tempdir_dst ) / 'test.pdf'
                m = pathlib.Path( tempdir_dst ) / 'test.meta'
                assert( r.exists() )
                assert( m.exists() )


if __name__ == '__main__':
    unittest.main()
