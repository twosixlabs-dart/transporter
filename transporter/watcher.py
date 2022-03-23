from os import path
from typing import List, Callable
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer


class FileCreatedHandler( PatternMatchingEventHandler ):
    def __init__( self, source: str, patterns: List[ str ], action: Callable ):
        super().__init__( patterns = patterns )
        self.source = source
        self.action = action

    def on_created( self, event ):
        print( f'file created: {event.src_path}' )
        raw_doc_path = event.src_path
        _, filename = path.split( raw_doc_path )

        self.action( f'{self.source}/{filename}' )


class FileWatcher:
    def __init__( self, source: str, patterns: List[ str ], action: Callable = None ):
        if action is None:
            action = self.__noop_handler_action__

        patterns = list( map( lambda p: f'*.{p}', patterns ) )

        self.observer = Observer()
        self.handler = FileCreatedHandler( source, patterns, action )
        self.observer.schedule( event_handler = self.handler, path = source, recursive = False )

    def start( self ):
        self.observer.start()

    def stop( self ):
        self.observer.stop()

    def __noop_handler_action__( self, source: str ):
        print( f'source: {source}' )
