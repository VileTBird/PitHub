'''
Main Entry Point for CLI
'''
import argparse
from pathlib import Path
from storage import Storage

def init_repo(args):
    storage = Storage()
    storage.init_repo()
    print("Initialized empty PitHub repository")

def add_files(args):
    storage = Storage()
    for file in args.files:
        try:
            storage.add_file(file)
            print(f"Added {file} to staging area")
        except FileNotFoundError as e:
            print(f"Error: {e}")

def commit_changes(args):
    storage = Storage()
    try:
        commit_hash = storage.commit(args.message)
        print(f"Created commit {commit_hash}")
    except ValueError as e:
        print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="PitHub Version Control System")
    subparsers = parser.add_subparsers(dest='command')

    # init command
    init_parser = subparsers.add_parser('init', help='Initialize a new repository')
    
    # add command
    add_parser = subparsers.add_parser('add', help='Add file(s) to staging area')
    add_parser.add_argument('files', nargs='+', help='File(s) to add')
    
    # commit command
    commit_parser = subparsers.add_parser('commit', help='Commit staged changes')
    commit_parser.add_argument('-m', '--message', required=True, help='Commit message')

    args = parser.parse_args()

    if args.command == 'init':
        init_repo(args)
    elif args.command == 'add':
        add_files(args)
    elif args.command == 'commit':
        commit_changes(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()