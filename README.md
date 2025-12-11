# core-contributor
Contribution framework for rules and test data with automated regression testing. Edit rules and test data, then validate against the PostgreSQL-based CORE engine.

# First-time Local Setup Steps

*IMPORTANT NOTE* - you may need your IT support team to install some of the following software for you. In particular, the setup script requires python3.12 to run properly. If you don't have it installed, the script will attempt to install it for you, but this is likely to be blocked by your company settings. If so, you will need to contact IT.

1) Create a free github account: https://github.com/signup
2) Install git, following the instructions here: https://git-scm.com/install/ \
       - Keep all the default settings throughout the installer \
       - You DO NOT need to actually run git as a program, so close any pop-ups that appear after the installation
3) Install VSCode, following the instructions here: https://code.visualstudio.com/download
4) Open VSCode and a terminal within it: \
       - Top Menu → Terminal → New Terminal (check the three dots in the top menu if you don't see 'Terminal')
5) Create a new empty directory on your machine for storing the repository and subsequent rule editing, and navigate to it in the terminal using `cd` commands. Avoid OneDrive if possible. \
       - There is sometimes an AI 'helper' box popup in the terminal - make sure you are typing commands into the command line itself, not the box \
       - If any of the folder names you are navigating through have spaces (eg 'My Folder'), you will need to wrap the path in quotes, eg: `cd "C:\Users\rich\Documents\Core Contributor Folder"`
6) Clone this repo into that directory by running the following command: \
       `git clone --recurse-submodules https://github.com/verisianHQ/core-contributor.git` \
       *IMPORTANT NOTE* - unless something goes badly wrong and you need to fully delete the entire directory, you should never need to run this command again. 
7) In VSCode, select "Open Folder" and select the repository folder you just cloned - it should be called `core-contributor`
8) This should re-open a new terminal in the repository folder. If this doesn't happen, open a new terminal in VSCode and navigate to the repository folder again.
9) You will need to setup the python environment, which will take a little bit of time. \
       - Assuming you are in the core-contributor folder in the VSCode terminal, run one of the following depending on your operating system (ignore messages and warnings): \
              WINDOWS: `.\setup\windows_setup.bat` \
              MAC: `./setup/bash_setup.sh` \
       - Windows might prompt you asking if you want to install python - the answer is yes!

*IMPORTANT NOTE* - if you start the setup script and stop it midway through, you may get some strange errors when you try to run rules in the future. If you have any doubts, rerun the setup script, and make sure it completes.

10) Set up the rule authoring auto-completion and real-time schema validation: \
        - Go to the `Extensions` tab in the VSCode left sidebar \
        - Search `yaml` and install the Red Hat YAML extension (it should be the top one) \
        - Once it's installed, search 'yaml schema' in the settings: \
              WINDOWS: File → Preferences → Settings \
              MAC: Code → Settings → Settings \
        - Click the `Edit in settings.json` option under Yaml: Schemas
        - Paste the following into "yaml.schemas": \
              `"https://rule-editor.cdisc.org/api/schema": "/*.yml"` \
        - Save the `settings.json` \
        - There you go! You should now see schema validation in yaml files. If you don't see this behaviour after a few seconds, try restarting VSCode


# Rule and Test Data Editing Process

*IMPORTANT NOTE* - For the following section, I have detailed the exact process to follow with relevant git commands to be executed in the terminal. If in doubt, you can always fall back to this process. \
However, VSCode integrates with git very effectively, and so there are intuitive point-and-click alternatives to all of the following commands with only simple configuration required. \
If you'd like to take advantage of this (and I strongly recommend it for at least staging, committing and pushing your changes), please see [this](https://docs.google.com/document/d/15ydgj4AqtEnFtlXL-J4DLJV32q_Q71gKn0ucu4tYYQw/edit?pli=1&tab=t.0#bookmark=id.mnk2lsoectvz) supplementary guide, complete with screenshots \
You'll need to run the following commands to get it working: \
`git config --global user.email "<your-github-email>"` \
`git config --global user.name "<your-github-username>"`

## Command Line Process

1) Make sure you are on the main branch and that it and the engine submodule is up to date. Run the following three commands: \
       `git checkout main` \
       `git pull origin main` \
       `git submodule update --remote`
2) Create a new branch to work on your changes, named as such: `<your-name>/<rule-id>/<change>` (eg `richard/CORE-000001/edit`): \
       `git branch <your-branch-name>`
3) Switch to your new branch: \
       `git checkout <your-branch-name>`
4) Edit a rule and test data as desired \
       - Ensure that you save any changes (File → Save, or Ctrl/Cmd + S)
5) When you want to run the rule against test data, make sure you are in the core-contributor folder and run one of the following: \
              WINDOWS: `.\run\windows_run.bat` \
              MAC: `./run/bash_run.sh` \
       - If you haven't run the setup script before, don't worry; it will run automatically when you execute this command \
       - You will be prompted to select the rule you wish to run, as well as the test case(s)
6) Check your run results in the `results` folder. Note that there is a separate `results` folder for each test case, which contains only the information relevant to that particular case \
       - There will be a `results.json` file, with the code-produced rule output, and a `results.txt` file, which will summarise your results in a more human-readable format. Feel free to examine both
7) If you are unhappy with the results of your changes, continue to edit and run the rule until you are satisfied
8) Create a PR to add your changes to the repository. To do this, run the following commands: \
       `git add .` \
       `git commit -m "your custom message"` \
       `git push origin <your-branch-name>` \
9) Go to the online repository and create a pull request (PR) from your newly pushed branch
10) On the PR page, make sure the information at the top is correct. It should be: \
       `base: main ← compare: <branch-name>`
11) Name your PR using the format `<rule-id> <fix>` and add a brief description of your changes
12) On the PR, add reviewers (both the 'Rules Team' and 'Engineers Team' are required) by clicking the cog in the top right corner, and add yourself as an assignee
13) You're done! Keep an eye on the PR to make sure the automated checks pass, as well as to respond to any comments from reviewers. If you need to edit any changes on the PR, you can simply checkout your branch (`git checkout <your-branch-name>`), make your changes, and commit and push them - the PR will automatically update!
14) If you want to start editing another rule, don't forget to run the below commands on VSCode terminal again: \
       `git checkout main` \
       `git pull origin main`

For further detail on any of these steps or git in general, see [this](https://docs.google.com/document/d/15ydgj4AqtEnFtlXL-J4DLJV32q_Q71gKn0ucu4tYYQw/edit?pli=1&tab=t.0) supplementary guide


# Advanced Usage

We have included some additional functionality in the test script. To take advantage of this, you will need to run the test script directly, rather than using the run script

1) In VSCode terminal, in the core-contributor directory, activate the virtual environment by running one of the following: \
              WINDOWS: `.\venv\Scripts\activate` \
              MAC: `source ./venv/bin/activate`
2) You can now run the test script directly with various options: \
              `python test.py` - Interactive mode (prompts you for rule and test case selection) \
              `python test.py -r <rule-id>` - Test all cases for a specific rule \
              `python test.py -r <rule-id> -tc <test-case>` - Test a specific case (eg `positive/01`) \
              `python test.py -r <rule-id> -v` - Test with verbose output (prints results to terminal) \
              `python test.py --all-rules` - Test all rules \
              `python test.py -h` - See all available options
3) When you're done, you can deactivate the venv by running `deactivate`


# Something's Wrong!

Git is great, but it is easy to overlook something and make a mistake. If you're stuck or confused, please reach out to [Richard](mailto:richard@verisian.com) or [Maximo](mailto:maximo@verisian.com) for support - we're always happy to help! /
However, here are some quick fixes for common issues you might experience:

> ***I accidentally made my changes on the main branch but haven't committed them yet***

If the branch you want to move your changes to already exists, run: \
`git checkout main` \
`git stash` \
`git checkout <existing-branch-name>` \
`git stash pop` \
If you want to move the changes to a new branch, you can run this useful one-liner: \
`git switch -c <new-branch-name>` 

> ***I accidentally made my changes on the main branch and committed them***

In this case, you won't be able to move your changes to an already existing branch easily. If you desperately need to do this, reach out to us \
Otherwise, create a new branch from main which includes your changes and then reset main:
`git checkout -b <new-branch-name>` \
`git checkout main` \
`git reset --hard HEAD~1` \
`git checkout <new-branch-name>` \
*IMPORTANT NOTE* - if you've committed more than once on main, you'll need to replace `HEAD~1` with `HEAD~n` where `n` is the number of commits you've made

> ***I've made some changes that I want to push to the repo and other changes that I don't want to keep***

In the source control sidebar panel (the icon is three dots connected by lines), you will see all of the changes you've made. \
You can right-click on any of these and select 'Discard Changes' \
This will completely remove your changes, so make sure you don't want them before doing this!

> ***I want to work on multiple rules at once!***

You can! You can create multiple branches for different rules and they will all be isolated from each other.
Just make sure to use `checkout` commands or the console to switch to the relevant branch before you make changes.

