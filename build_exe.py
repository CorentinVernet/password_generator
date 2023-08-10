from py2exe import *

if __name__ == "__main__":
    adjectives_path = ".\\assets\\common_adjectives.json"
    verbs_path = ".\\assets\\common_verbs.json"
    nouns_path = ".\\assets\\common_nouns.json"
    freeze(windows=[{"script": ".\\generate_password.py"}], 
           data_files=[("assets", [verbs_path, adjectives_path, nouns_path])],
           zipfile=None,
           options={"py2exe": {"packages": ["pattern"], "includes": ["pattern"]}})