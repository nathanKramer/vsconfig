# VSConfig

Untested script for storing vscode extensions in version control and re-instating them on other machines.

Usage:

```
code --list-extensions > extensions
git add extension && git commit -m "Store my extensions"

...

git pull
./vsconfig.py install

# or

./vsconfig.py force

# or

./vsconfig.py diff
```
