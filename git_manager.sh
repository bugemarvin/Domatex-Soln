#!/bin/bash

##############################################################################
# Git Manager Script for Local Repository
#
# This script automates the process of committing and pushing changes in a
# local Git repository. It runs asynchronously every 30 minutes, checks for
# edited files, and waits for files to be closed before committing and pushing.
#
# The commit_and_push_changes function is responsible for committing and
# pushing the changes. It adds all modified files with a commit message
# mentioning "Update [filename]" and all newly created files with a commit
# message mentioning "Add [filename]".
#
# The check_editor_status function checks if any files in the repository are
# open in a text editor. It uses the lsof command to identify open files. The
# script will wait until all files are closed before proceeding.
#
# Please make sure to update ~/Hackathon-Projects/Domatex-Soln with the actual
# path to your local Git repository. Also, ensure that you have the necessary
# permissions and proper Git configuration set up to perform the operations.
#
# To start the script, simply execute it in the terminal. It will run
# asynchronously in the background, continuously checking for edited files and
# waiting for them to be closed before committing and pushing the changes.
#
# Please note that this script relies on the lsof command to check if files are
# open in an editor. Make sure lsof is installed on your system for the script
# to work correctly. Additionally, keep in mind that this script will run
# indefinitely until manually stopped.
##############################################################################

# Set the path to the local Git repository
repo_path="/Domatex-Soln"

# Set the Git remote URL
remote_url="https://github.com/Dovineowuor/Domatex-Soln"

# Function to commit and push changes
commit_and_push_changes() {
    # Change to the repository directory
    cd "$repo_path"

    # Configure Git if not already configured
    git config --global --get user.name > /dev/null || git config --global user.name "Dovineowuor"
    git config --global --get user.email > /dev/null || git config --global user.email "owuordove@gmail.com"

    # Add all modified files to the Git repository
    modified_files=$(git status --porcelain | awk '$1 ~ /[MA]/ {print $2}')
    for file in $modified_files; do
        filename=$(basename "$file")
        git add "$file"
        git commit -m "Update $filename"
    done

    # Add all newly created files to the Git repository
    new_files=$(git status --porcelain | awk '$1 ~ /[??]/ {print $2}')
    for file in $new_files; do
        filename=$(basename "$file")
        git add "$file"
        git commit -m "Add $filename"
    done

    # Push the changes to the remote repository
    git push "$remote_url"

    echo "Changes committed and pushed successfully."
}

# Check if the repository is already being edited in a text editor
check_editor_status() {
    while true; do
        opened_files=$(lsof +D "$repo_path" 2>/dev/null | awk '$4=="txt" || $4=="DEL" {print $NF}')
        if [[ -n "$opened_files" ]]; then
            echo "Repository files are open in an editor. Waiting for files to be closed..."
            sleep 1m
        else
            echo "All files in the repository are closed. Proceeding with commit and push."
            break
        fi
    done
}

# Add the script file to .gitignore
# echo "git_manager.sh" >> "$repo_path/.gitignore"

# Start the script asynchronously
while true; do
    # Check for edited files every 30 minutes
    sleep 5m

    # Check if any files are open in an editor
    check_editor_status

    # Wait for a grace period of 30 minutes before committing and pushing changes
    sleep 5m

    # Commit and push the changes
    commit_and_push_changes
done

