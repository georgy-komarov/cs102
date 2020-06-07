import argparse
import os
from pathlib import Path


class MyGit:
    def __init__(self):
        self.args = self.argparse_init()

    def argparse_init(self):
        parser = argparse.ArgumentParser(description='My own git')
        subparsers = parser.add_subparsers(metavar='command')

        parser_init = subparsers.add_parser('init', help='Initialize the .git directory')
        parser_init.add_argument('path', type=Path, default=Path('.'), nargs='?', help='path to git repository')
        parser_init.set_defaults(func=self.init)

        parser_cat_file = subparsers.add_parser('cat-file', help='Read a blob object')
        parser_cat_file.set_defaults(func=self.cat_file)

        parser_hash_object = subparsers.add_parser('hash-object', help='Create a blob object')
        parser_hash_object.set_defaults(func=self.hash_object)

        parser_ls_tree = subparsers.add_parser('ls-tree', help='Read a tree object')
        parser_ls_tree.set_defaults(func=self.ls_tree)

        parser_write_tree = subparsers.add_parser('write-tree', help='Write a tree object')
        parser_write_tree.set_defaults(func=self.write_tree)

        parser_commit_tree = subparsers.add_parser('commit-tree', help='Create a commit')
        parser_commit_tree.set_defaults(func=self.commit_tree)

        parser_clone = subparsers.add_parser('clone', help='Clone a repository')
        parser_clone.set_defaults(func=self.clone)

        return parser.parse_args()

    def init(self):
        path = self.args.path
        os.makedirs(os.path.join(path, '.git'), exist_ok=True)

        for folder in ['objects', 'refs', 'refs/heads']:
            os.makedirs(os.path.join(path, '.git', folder), exist_ok=True)
        with open(os.path.join(path, '.git', 'HEAD'), 'wb') as f:
            f.write(b'ref: refs/heads/master\n')

        print(f'Initialized empty Git repository in {os.path.abspath(os.path.join(path, ".git"))}')

    def cat_file(self):
        raise NotImplementedError

    def hash_object(self):
        raise NotImplementedError

    def ls_tree(self):
        raise NotImplementedError

    def write_tree(self):
        raise NotImplementedError

    def commit_tree(self):
        raise NotImplementedError

    def clone(self):
        raise NotImplementedError


if __name__ == '__main__':
    mygit = MyGit()
    mygit.args.func()
