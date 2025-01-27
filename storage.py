# storage handler
import os
import hashlib
import zlib
import json
from pathlib import Path

class Storage:
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir)
        self.vcs_dir = self.root_dir / ".vcs"
        self.objects_dir = self.vcs_dir / "objects"
        self.commits_dir = self.vcs_dir / "commits"
        self.index_file = self.vcs_dir / "index"

    def init_repo(self):
        """Initialize repository structure"""
        dirs = [self.vcs_dir, self.objects_dir, self.commits_dir]
        for dir_path in dirs:
            dir_path.mkdir(exist_ok=True, parents=True)
        
        if not self.index_file.exists():
            self._write_index({})

    def hash_content(self, content):
        """Generate SHA-1 hash of content"""
        return hashlib.sha1(content.encode()).hexdigest()

    def store_object(self, content):
        """Store content in objects directory"""
        content_hash = self.hash_content(content)
        compressed = zlib.compress(content.encode())
        
        object_path = self.objects_dir / content_hash
        with open(object_path, 'wb') as f:
            f.write(compressed)
        
        return content_hash

    def get_object(self, content_hash):
        """Retrieve content from objects directory"""
        object_path = self.objects_dir / content_hash
        if not object_path.exists():
            raise ValueError(f"Object {content_hash} not found")
        
        with open(object_path, 'rb') as f:
            compressed = f.read()
        
        return zlib.decompress(compressed).decode()

    def _read_index(self):
        """Read the index file"""
        if not self.index_file.exists():
            return {}
        with open(self.index_file, 'r') as f:
            return json.load(f)

    def _write_index(self, index_data):
        """Write to the index file"""
        with open(self.index_file, 'w') as f:
            json.dump(index_data, f, indent=2)

    def add_file(self, filepath):
        """Add file to staging area"""
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"File {filepath} not found")
        
        with open(filepath, 'r') as f:
            content = f.read()
        
        content_hash = self.store_object(content)
        
        index = self._read_index()
        index[str(filepath)] = {
            'hash': content_hash,
            'timestamp': os.path.getmtime(filepath)
        }
        self._write_index(index)

    def commit(self, message):
        """Create a commit with staged changes"""
        index = self._read_index()
        if not index:
            raise ValueError("Nothing to commit")
        
        commit_data = {
            'message': message,
            'timestamp': os.path.time(),
            'files': index,
            'parent': self._get_latest_commit()
        }
        
        commit_content = json.dumps(commit_data, indent=2)
        commit_hash = self.store_object(commit_content)
        
        commit_ref_path = self.commits_dir / commit_hash
        with open(commit_ref_path, 'w') as f:
            f.write(commit_content)
        
        return commit_hash

    def _get_latest_commit(self):
        """Get the hash of the latest commit"""
        commits = list(self.commits_dir.glob('*'))
        if not commits:
            return None
        return sorted(commits, key=lambda x: os.path.getctime(x))[-1].name