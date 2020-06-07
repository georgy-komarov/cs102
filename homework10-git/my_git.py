import argparse
import hashlib
import os
import zlib
from pathlib import Path


class MyGit:
    def __init__(self):
        self.git_folder = '.mygit'
        self.args = self.argparse_init()

    def argparse_init(self):
        parser = argparse.ArgumentParser(description='My own git')
        subparsers = parser.add_subparsers(metavar='command')

        parser_init = subparsers.add_parser('init', help='Initialize the .git directory')
        parser_init.add_argument('path', type=Path, default=Path('.'), nargs='?', help='path to git repository')
        parser_init.set_defaults(func=self.init)

        parser_cat_file = subparsers.add_parser('cat-file', help='Read a blob object')
        parser_cat_file.add_argument('hash', help='object\'s hash')
        parser_cat_file.add_argument('-p', dest='pretty_print', action='store_true',
                                     help='pretty-print object\'s content')
        parser_cat_file.set_defaults(func=self.cat_file)

        parser_hash_object = subparsers.add_parser('hash-object', help='Create a blob object')
        parser_hash_object.add_argument('filepath', help='file to hash')
        parser_hash_object.add_argument('-w', dest='write', action='store_true',
                                        help='write the object into the object database')
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
        os.makedirs(os.path.join(path, self.git_folder), exist_ok=True)

        for folder in ['objects', 'refs', 'refs/heads']:
            os.makedirs(os.path.join(path, self.git_folder, folder), exist_ok=True)
        with open(os.path.join(path, self.git_folder, 'HEAD'), 'wb') as f:
            f.write(b'ref: refs/heads/master\n')

        print(f'Initialized empty Git repository in {os.path.abspath(os.path.join(path, self.git_folder))}')

    def cat_file(self):
        sha1_prefix = self.args.hash
        pretty_print = self.args.pretty_print
        if len(sha1_prefix) < 2:
            raise ValueError('Hash should be at least 2 characters')
        if pretty_print:
            subfolder, sha1_rest = sha1_prefix[:2], sha1_prefix[2:]
            obj_dir = os.path.join(self.git_folder, 'objects', subfolder)

            # Allow to search with part of hash
            try:
                objects = [name for name in os.listdir(obj_dir) if name.startswith(sha1_rest)]
            except FileNotFoundError:  # if subfolder does not exist
                objects = []

            if not objects:
                raise ValueError(f'object {sha1_prefix} not found')
            if len(objects) >= 2:
                raise ValueError(f'multiple objects ({len(objects)}) found with prefix {sha1_prefix}')

            obj_path = os.path.join(obj_dir, objects[0])
            with open(obj_path, 'rb') as f:
                data = zlib.decompress(f.read())
                blob, content = map(bytes.decode, data.split(b'\x00', maxsplit=1))

            print(blob, content, sep='\n\n')
        else:
            print('no action supplied')

    def hash_object(self):
        file_path = self.args.filepath
        write = self.args.write

        with open(file_path, 'rb') as f:
            content = f.read()

        header = f'blob {len(content)}'.encode()
        data = header + b'\x00' + content
        compressed_data = zlib.compress(data)

        sha1_hash = hashlib.sha1(data).hexdigest()
        if write:
            subfolder, sha1_rest = sha1_hash[:2], sha1_hash[2:]
            obj_path = os.path.join(self.git_folder, 'objects', subfolder, sha1_rest)
            os.makedirs(os.path.dirname(obj_path), exist_ok=True)

            with open(obj_path, 'wb') as f:
                f.write(compressed_data)

            print(f'file {file_path} written as {obj_path}')
        else:
            print('no action supplied')

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
