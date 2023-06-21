#!/bin/bash

# Define the list of secrets to search for
secrets=("pswd" "password" "SECRET" "SECRET1" "SECRET2" "SECRET3")

# Function to search for secrets in a file
check_secrets_in_file() {
    file=$1
    secrets_found=0

    while IFS= read -r line; do
        ((line_number++))

        for secret in "${secrets[@]}"; do
            if [[ $line == *"$secret"* ]]; then
                echo "Secret '$secret' found in <$file, line $line_number>: $line"
                ((secrets_found++))
            fi
        done
    done < "$file"

    return $secrets_found
}

# Function to check secrets in all files
check_secrets_in_files() {
    secrets_found=0

    for file in $(git diff --name-only); do
        line_number=0
        check_secrets_in_file "$file"
        ((secrets_found+=$?))
    done

    return $secrets_found
}

# Main script
echo "Checking for secrets before committing to Git..."

check_secrets_in_files

secrets_found=$?

if [ $secrets_found -gt 0 ]; then
    echo "$secrets_found secret(s) found. Resolve them before committing."
    exit 1
else
    echo "No secrets found. Committing changes."
    exit 0
fi
