import os
import json
from pathlib import Path
from pygit2 import Repository
from linguist import analyze_languages
from requirements_parser import parse

def inspect_repo(repo_path):
    repo = Repository(repo_path)

    # Language detection
    languages = analyze_languages(repo_path)

    # Dependency analysis
    dependencies = {}
    req_file = Path(repo_path) / 'requirements.txt'
    if req_file.is_file():
        with open(req_file) as f:
            requirements = parse(f)
            for req in requirements:
                dependencies[req.name] = req.specs[0][1] if req.specs else None

    # Git history analysis
    total_commits = len([commit for commit in repo.walk(repo.head.target)])
    main_contributors = set([commit.author.name for commit in repo.walk(repo.head.target)])
    last_commit_date = repo[repo.head.target].commit_time

    profile = {
        'language': 'Python',
        'language_version': None, # You might need additional logic to extract this
        'framework': 'FastAPI', # You might need additional logic to determine the framework
        'framework_version': dependencies.get('fastapi'),
        'dependencies': dependencies,
        'git_history': {
            'total_commits': total_commits,
            'main_contributors': list(main_contributors),
            'last_commit_date': last_commit_date
        },
        'languages': languages
    }

    return profile

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} <path_to_repo>')
        exit(1)

    repo_path = sys.argv[1]
    profile = inspect_repo(repo_path)

    print(json.dumps(profile, indent=2))

