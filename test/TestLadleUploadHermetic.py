import unittest
import httpretty
from transporter.ladle import upload_ladle


class LadleUploadHermeticTest( unittest.TestCase ):
    def __init__( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.ladle_host = 'ladle'
        self.ladle_port = 6308
        self.ladle_url = f'https://{self.ladle_host}:{self.ladle_port}/submit/file'

    @httpretty.activate
    def test_upload_success( self ):
        httpretty.enable()
        httpretty.register_uri( httpretty.POST, self.ladle_url, status = 200, body = 'asdf' )

        test_file = 'test/resources/test.pdf.raw'

        result = upload_ladle( test_file, self.ladle_host, self.ladle_port )

        assert result == True

    @httpretty.activate
    def test_upload_failure( self ):
        httpretty.enable()
        httpretty.register_uri( httpretty.POST, self.ladle_url, status = 400, body = 'asdf' )

        test_file = 'test/resources/test.pdf.raw'

        result = upload_ladle( test_file, self.ladle_host, self.ladle_port )

        assert result == False


if __name__ == '__main__':
    unittest.main()