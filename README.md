# TaskMason: macOS Task Management Toolkit

Tool to write and schedule tasks on macOS faster, enhanced with AI.

## Structure

```bash
├── README.md
├── requirements.txt
├── scripts
│   ├── generate_plist_with_gpt.py
│   └── prepTasks.py
└── taskMason.sh
└── < tasks you'll geneWrite ;) >
```

## Description

**WARNING**
*Scripts may produce inaccurate scripts and it's your job to verify that they work as you think they should.*

### generate

Use the `generate_plist_with_gpt.py` script to generate a launchd plist file with a task description of any kind. The script will use GPT-3.5 to generate a task description based on the input you provide. The script will then generate a launchd plist file with the task description and time interval you provide. The script will then save the launchd plist file to the path you provide.

```bash
python3 ./scripts/generate_plist_with_gpt.py "will create hello_there.txt in ~/tmp directory every 30s." hello_there.plist
```

### improve

Use prepTasks.py to improve the task description, by removing potentially dummy data received, and pretty print condensed XML.

```python3
python3 ./scripts/prepTasks.py hello_there.plist 
```

### schedule

To add created job:

```bash
./taskMason.sh -a hello_there.plist
```

To list existing jobs:

```bash
./taskMason.sh -l
# or
./taskMason.sh -vl
```

To delete your jobs:

```bash
./taskMason.sh -d hello_there.plist
```

### Installation

```bash
git clone https://github.com/gkk-dev-ops/taskMason.git ~/tmp
cd ~/tmp/
python3 -m venv venv
pip install -r requirements.txt
```
