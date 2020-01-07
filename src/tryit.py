from vsconfig import installed_extensions, index_extension_metadata

# This file isn't important, it's just a placeholder for glorified REPL testing
idx = index_extension_metadata(
    installed_extensions(), '/Users/nathankramer/.vscode/extensions')

print(idx)
