#!/bin/bash

# This is the user's numeric ID. In Unix-like systems, each user is assigned
# a unique numerical user ID (UID). UID 501 is typically the first non-system
# user created on a macOS system, and it's often the UID for the first user
# account that is set up during the system installation.
USER_ID=$(id -u $USER)
# Define the target directory
TARGET_DIR="$HOME/Library/LaunchAgents"
debugFlag=false

# Pre-process the arguments to detect --DEBUG flag
for arg in "$@"; do
    if [ "$arg" == "--DEBUG" ]; then
        debugFlag=true
    fi
done

# Remove --DEBUG from the arguments list
set -- "${@//--DEBUG/}"


# Display help information
show_help() {
    echo "Usage: tasks OPTION [TASKS]"
    echo "Manage launchd tasks."
    echo ""
    echo "Options:"
    echo "  -a,             Add tasks. If '.' is used, all tasks in the current directory are added."
    echo "  -d,             Delete tasks. If '.' is used, all tasks in the current directory are deleted."
    echo "  -l, --list      List all user-created, loaded tasks."
    echo "  -vl, --verbose-list
                            List all non-system-created, loaded tasks."
    echo "  --DEBUG         Display addition debug information for troubleshooting."
    echo "  -h, --help      Display this help message and exit."
    echo ""
    echo "Examples:"
    echo "  tasks -a .                              Add all tasks from the current directory."
    echo "  tasks -d .                              Delete all tasks from the current directory."
    echo "  tasks -a task1.plist task2.plist        Add specific tasks."
    echo "  tasks -d task1.plist                    Delete a specific task."
}

# Function to list user-created tasks
list_tasks() {
    echo "User-created, loaded tasks:"
    for task in $TARGET_DIR/*.plist; do
        filename=$(basename "$task")
        echo "  $filename"
    done
}

# Function to list all non system tasks
list_all_tasks() {
    echo "All non system tasks:"
    launchctl list | grep -v com.apple
}

# Function to add tasks
add_tasks() {
    for task in "$@"; do
        if [ -f "$task" ]; then
            # Extract the filename from the full path
            filename=$(basename "$task")
            
            # Create a symbolic link for the .plist file
            ln -s "$(pwd)/$filename" "$TARGET_DIR/$filename"
            
            # Load the task into launchd
            launchctl load "$TARGET_DIR/$filename"

            echo "Added and loaded $filename."
        else
            echo "File $task does not exist."
        fi
    done
}

# Function to delete tasks
delete_tasks() {
    for task in "$@"; do
        filename=$(basename "$task")

        if [ "$filename" == "" ]; then
           continue # Skip empty arguments. Fixes DEBUG flag issue.
        fi
        if [ "$debugFlag" = true ]; then
            echo "[DEBUG]: Unloading task: gui/$USER_ID/com.$USER.$(basename "$filename" .plist)"
        fi

        # Unload the task from launchd
        launchctl bootout gui/$USER_ID/com.$USER.$(basename "$filename" .plist)

        # Remove the symbolic link from the target directory
        rm "$TARGET_DIR/$filename"

        echo "Unloaded and removed $filename."
    done
}

# Main execution
case "$1" in
    -a)
        shift
        if [ "$1" = "." ]; then
            add_tasks *.plist
        else
            add_tasks "$@"
        fi
        ;;
    -d)
        shift
        if [ "$1" = "." ]; then
            delete_tasks *.plist
        else
            delete_tasks "$@"
        fi
        ;;
    -l|--list)
        list_tasks
        ;;
    -vl|--verbose-list)
        list_tasks
        ;;
    -h|--help)
        show_help
        ;;
    *)
        echo "Invalid option."
        echo "Use 'tasks -h' or 'tasks --help' to see available options."
        ;;
esac
