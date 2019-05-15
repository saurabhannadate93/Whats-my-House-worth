"""
This module contains functions to load the raw data from the source and dump it into the desired location

"""

import logging
import config
 
logger = logging.getLogger(__name__)


def run_loading(args):
    '''Fetches the data from the raw source and dumps it at the location specified
    
    Args:
        args: Argparse args - should include args.where, args.bucket
        
    Returns:
        None
    '''
    print('Hello Doston')
    print(args.where)
    print(args.bucket)


if __name__ == "__name__":
    
    parser = argparse.ArgumentParser(description="Load Data")
    subparsers = parser.add_subparsers()
    
    # Sub-parser for ingesting new data
    sb_ingest = subparsers.add_parser("fetch", description="Fetch the raw data from the source")
    sb_ingest.add_argument("--where", default="Local", help="'Local' or 'AWS'; bucket name needs to be provided in case of AWS")
    sb_ingest.add_argument("--bucket", default="None", help="S3 bucket name")
    sb_ingest.set_defaults(func=run_loading)
