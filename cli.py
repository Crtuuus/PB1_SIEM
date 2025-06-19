# cli.py
import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Asset

# 1) Poveže se na SQLite bazo
engine = create_engine('sqlite:///siem.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

# 2) Definicija funkcije za ukaz list-assets
def list_assets(args):
    assets = session.query(Asset).all()
    print(f"{'ID':<3} {'Hostname':<10} {'IP Address':<15} {'Type':<10} {'Location'}")
    print("-"*50)
    for a in assets:
        print(f"{a.asset_id:<3} {a.hostname:<10} {a.ip_address:<15} {a.device_type:<10} {a.location}")

# 3) Main parser in subparser za ukaze
def main():
    parser = argparse.ArgumentParser(prog='siem-cli', description='SIEM CLI tool')
    subparsers = parser.add_subparsers()

    # list-assets
    p_list = subparsers.add_parser('list-assets', help='List all assets')
    p_list.set_defaults(func=list_assets)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
