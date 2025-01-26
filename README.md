# PitHub

### Main Python Packages in USE/will be USED
```
hashlib → For content hashing.
zlib → For compression.
os & shutil → For file handling.
argparse → For CLI interactions.
json → For metadata storage.
difflib → For diffing files.
```
### File Structure

```
pithub/
│-- main.py (main entry point for CLI)
│-- storage.py (handles file storage)
│-- commands/
│   ├── init.py
│   ├── add.py
│   ├── commit.py
│   ├── log.py
│   ├── checkout.py
│   ├── diff.py
│-- utils.py (hashing, compression helpers)
│-- .vcs/
│   ├── objects/
│   ├── commits/
│   ├── index
```

### Commands (Will be changed to something more intuitive but later)
```
Initialize Repo:
python vcs.py init
Add and Commit Files:
python vcs.py add file.txt  
python vcs.py commit -m "First commit"
View History:
python vcs.py log
Check Differences:
python vcs.py diff
Checkout to Previous State:
python vcs.py checkout <commit_hash>
```