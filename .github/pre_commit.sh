#!/bin/sh

# Define an array of file extensions to check
file_extensions=(*.*)

# Define a function to check for secret files with the given extension
check_secret_files() {
  for file in "$@"; do
    if git diff --cached --name-only "$file" | grep -E ".*\.$extension$" | grep -vE '^(security/.*)$' | xargs git diff --cached --name-only -s | grep -E '^(A|M)$'; then
      echo "Error: Secret files with extension.$extension detected in $file"
      exit 1
    fi
  done
}

# Loop through each file extension
for extension in "${file_extensions[@]}"; do
  # Check for changes to files with the current extension
  if git diff --cached --name-only | grep -E ".*\.$extension$" | xargs git diff --cached --name-only -s | grep -E '^(A|M)$'; then
    # Check for secret files with the current extension
    check_secret_files $(git diff --cached --name-only | grep -E ".*\.$extension$" | grep -vE '^(security/.*)$')

    # Check for textual secret codes in files with the current extension
    while read file; do
      if git diff --cached --name-only "$file" | grep -E ".*\.$extension$" | xargs git diff --cached --word-diff=color | grep -E '[-+][^-+ ]+'; then
        # Get the line number and character index range of the location of the secret
        line_number=$(git diff --cached --name-only "$file" | grep -E ".*\.$extension$" | xargs git diff --cached --word-diff=color | grep -nE '[-+][^-+ ]+' | cut -d':' -f1)
        character_index_range=$(git diff --cached --name-only "$file" | grep -E ".*\.$extension$" | xargs git diff --cached --word-diff=color | grep -nE '[-+][^-+ ]+' | cut -d':' -f2-3 | tr -d ')
        # Get the name of the file and the location of the secret
        file_name=$(basename "$file")
        secret_location=$(sed -n "$line_number"p "$file")
        # Raise an exception with the file name, line number, character index range, and location of the secret
        echo "Error: Textual secret codes detected in $file_name at line $line_number: $character_index_range: $secret_location"
        exit 1
      fi
    done < <(git diff --cached --name-only | grep -E ".*\.$extension$" | grep -vE '^(security/.*)$')
  fi
done

# Check for changes to ignored files
if git diff --cached --name-only | grep -E '.*\.(pyc|log|swp)$'; then
  echo "Error: Changes to ignored files detected"
  exit 1
fi

# Check for changes to files in the security/api/secret directory
if git diff --cached --name-only | grep -E '^(security/api/secret/.*)$' | xargs git diff --cached --name-only -s | grep -E '^(A|M)$'; then
  echo "Error: Changes to files in the security/api/secret directory detected"
  exit 1
fi

# Check for uncommitted changes
if git status -s | grep -E '^(M|A|D)$'; then
  echo "Error: Uncommitted changes detected"
  exit 1
fi