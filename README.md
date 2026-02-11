# core-contributor
Contribution framework for rule storage, rule authoring and test data creation with automated regression testing. Create and/or edit rules and test data, then validate against the PostgreSQL-based CORE engine.

**BEFORE CONTRIBUTING, MAKE SURE YOU HAVE GONE THROUGH THE CDISC VOLUNTEERING ONBOARDING PROCESS** \
https://www.cdisc.org/volunteer

**SUPPLEMENTARY GUIDE** \
Instructions below will guide you step-by-step through the:
- First-time Local Setup Steps
- Rule Authoring and Test Data Creation Process
  
These steps should be sufficient to get you started but are very descriptive. If you wish to be guided in a more visual way, steps with print screens are available in the [supplementary guide](https://docs.google.com/document/d/15ydgj4AqtEnFtlXL-J4DLJV32q_Q71gKn0ucu4tYYQw/edit?pli=1&tab=t.0).

# First-time Local Setup Steps

***IMPORTANT NOTE*** \
_You may need your IT support team to install some of the following software for you. In particular, the setup script requires python3.12 to run properly. If you don't have it installed, the script will attempt to install it for you, but this is likely to be blocked by your company settings. If so, you will need to contact IT._

**Follow steps 1 - 11 carefully.**

1) Create a free GitHub account: https://github.com/signup
2) Install Git, following the instructions here: https://git-scm.com/install
   - Keep all the default settings throughout the installer 
   - You DO NOT need to actually run Git as a program, so close any pop-ups that appear after the installation
3) Install VSCode (***not*** VSCodeUser), following the instructions here: https://code.visualstudio.com/download
4) Open VSCode and a terminal within it: 
   - Top Menu → Terminal → New Terminal (check the three dots in the top menu if you don't see 'Terminal')
5) Create a new empty directory on your machine for storing the repository and subsequent rule authoring and editing. Navigate to it in the terminal using `cd` commands. Avoid OneDrive if possible. 
   - There is sometimes an AI 'helper' box popup in the terminal - make sure you are typing commands into the command line itself, not the box 
   - If any of the folder names you are navigating through have spaces (eg 'My Folder'), you will need to wrap the path in quotes,\
     eg: `cd "C:\Users\rich\Documents\Core Contributor Folder"`
6) Clone this repo into that directory by running the following command (**DO NOT RUN MORE THAN ONCE**): \
       `git clone --recurse-submodules https://github.com/verisianHQ/core-contributor.git` 
   
   _***IMPORTANT NOTE***\
   Unless something goes badly wrong and you need to fully delete the entire directory, you should never need to run this command again._
   
8) In VSCode, select "Open Folder" and select the repository folder you just cloned - it should be called `core-contributor`
9) This should re-open a new terminal in the repository folder. If this doesn't happen, open a new terminal in VSCode and navigate to the repository folder again.
10) You will need to setup the python environment, which will take a little bit of time. 
    - Assuming you are in the core-contributor folder in the VSCode terminal, run one of the following depending on your operating system (ignore messages and warnings): 
      - WINDOWS: `.\setup\windows_setup.bat`
      - MAC: `./setup/bash_setup.sh` 
    - Windows might prompt you asking if you want to install python - the answer is yes!
         
    _***IMPORTANT NOTE***\
    If you start the setup script and stop it midway through, you may get some strange errors when you try to run rules in the future. If you have any doubts, rerun the setup script, and make sure it completes._

10) Set up the rule authoring auto-completion and real-time schema validation: 
    - Go to the `Extensions` tab in the VSCode left sidebar 
    - Search `yaml` and install the Red Hat YAML extension (it should be the top one) 
    - Once it's installed, search 'yaml schema' using the search bar at the top of the settings: 
      - WINDOWS: File → Preferences → Settings
      - MAC: Code → Settings → Settings 
    - Click the `Edit in settings.json` option under Yaml: Schemas 
    - Paste the following into "yaml.schemas": 
              `"https://rule-editor.cdisc.org/api/schema": "/*.yml"` 
    - Save the `settings.json` 
    - There you go! You should now see schema validation in yaml files. If you don't see this behaviour after a few seconds, try restarting VSCode

11) Install the XLSX Editor plugin: 
    - In the VS Code file explorer, locate the `.vsix` file in the root directory of this repository 
    - Right-click the file and select "Install Extension VSIX"

**You are now ready with the setup steps and can start with the rule authoring!**

# Rule Authoring and Test Data Creation Process

**_*IMPORTANT NOTE*_**\
_In the following section, the exact process to follow with relevant Git commands to be executed in the terminal are described. If in doubt, you can always fall back to this process. However, VSCode integrates with Git very effectively, and so there are intuitive point-and-click alternatives to all of the following commands with only simple configuration required._

_If you'd like to take advantage of this (strongly recommended for at least staging, committing and pushing your changes), please see [supplementary guide](https://docs.google.com/document/d/15ydgj4AqtEnFtlXL-J4DLJV32q_Q71gKn0ucu4tYYQw/edit?tab=t.0#bookmark=id.v2ehj99lxmyr) for extra details and screenshots. \
You'll need to run the following commands to get it working: \
`git config --global user.email "<your-github-email>"` \
`git config --global user.name "<your-github-username>"`__

_Don't forget that whenever you type a command, that you are in the core-contributor folder that you created during the set-up steps._

## Command Line Process

**Create a Local Branch.**
1) Make sure you are on the main branch and that both the main branch and the engine submodule are up to date. To do this, run the following three commands: \
       `git checkout main` \
       `git pull origin main` \
       `git submodule update --remote`
   
2) Create a new branch to work on your changes, named as such: `<your-name>/<rule-id>/<change>` (eg `richard/CORE-000001/edit`): \
       `git branch <your-branch-name>`
   
   _Note that only branch names according to following regex are allowed: **^[a-zA-Z]+/(CORE-[0-9]{6}|CG[0-9]{4})/(edit|create|delete)$**_
   
4) Switch to your new branch: \
       `git checkout <your-branch-name>`

**Edit YAML code and test data.**

4) Edit a rule and test data as desired
   - Ensure that you create negative and positive test data that cover all functionalities of the rule (condition and rule), scope, exceptions,...
   - Indicate in the negative test data for which records you expect output = setting pre-defined discrepancies
   - Ensure that you save any changes (File → Save, or Ctrl/Cmd + S)
   
**Perform Automated Testing.**

5) Run the rule against the test data 
    - When you want to run the rule against test data, make sure you are in the core-contributor folder and run one of the following: 
      - WINDOWS: `.\run\windows_run.bat` 
      - MAC: `./run/bash_run.sh` 
    - If you haven't run the setup script before, don't worry; it will run automatically when you execute this command 
    - You will be prompted to select the rule you wish to run, as well as the test case(s)
      
**Check Testing Output.**
     
6) Check your run results in the `results` folder.
    - Note that there is a separate `results` folder for each test case, which contains only the information relevant to that particular case
    - There will be a `results.json` file, with the code-produced rule output, and a `results.txt` file, which will summarise your results in a more human-readable format.
    - Feel free to examine both
      
7) If you are unhappy with the results of your changes, continue to edit and run the rule until you are satisfied

**Request adding Local Branch to Main Branch.**

8) Create a PR to add your changes to the repository. To do this, run the following commands: \
       `git add .` \
       `git commit -m "your custom message"` \
       `git push origin <your-branch-name>` \
   The first time you commit, you may have to log in to github
   
9) Go to the online repository and create a pull request (PR) from your newly pushed branch
    
10) On the PR page, make sure the information at the top is correct. It should be: \
       `base: main ← compare: <branch-name>`
    
11) Name your PR using the format `<rule-id> <fix>` and add a brief description of your changes
    
12) On the PR, add reviewers (both the 'Rules Team' and 'Engineers Team' are required) by clicking the cog in the top right corner, and add yourself as an assignee
    
**You're done! Keep an eye on the PR to make sure the automated checks pass, as well as to respond to any comments from reviewers.**\

13) If you need to edit any changes on the PR, you can simply checkout your branch (`git checkout <your-branch-name>`), make your changes, and commit and push them - the PR will automatically update!

14) If you want to start editing another rule, don't forget to run the below commands on VSCode terminal again: \
       `git checkout main` \
       `git pull origin main`

For further detail on any of these steps or git in general, see [supplementary guide](https://docs.google.com/document/d/15ydgj4AqtEnFtlXL-J4DLJV32q_Q71gKn0ucu4tYYQw/edit?pli=1&tab=t.0)


# Advanced Usage

Below are some additional functionalities in the test script. To take advantage of this, you will need to run the test script directly, rather than using the run script.

1) In VSCode terminal, in the core-contributor directory, activate the virtual environment by running one of the following: \
   - WINDOWS: `.\venv\Scripts\activate` \
   - MAC: `source ./venv/bin/activate`
   
2) You can now run the test script directly with various options:
   - `python test.py` - Interactive mode (prompts you for rule and test case selection)
   - `python test.py -r <rule-id>` - Test all cases for a specific rule
   - `python test.py -r <rule-id> -tc <test-case>` - Test a specific case (eg `positive/01`)
   - `python test.py -r <rule-id> -v` - Test with verbose output (prints results to terminal)
   - `python test.py --all-rules` - Test all rules
   - `python test.py -h` - See all available options
3) When you're done, you can deactivate the venv by running `deactivate`


# Something's Wrong!

Git is great, but it is easy to overlook something and make a mistake. \
If you're stuck or confused, please reach out to Richard (richard@verisian.com) or Maximo (maximo@verisian.com) for support - we're always happy to help! \
However, here are some quick fixes for common issues you might experience: \
<br />

> ***I accidentally made my changes on the main branch but haven't committed them yet***

If the branch you want to move your changes to already exists, run: \
`git checkout main` \
`git stash` \
`git checkout <existing-branch-name>` \
`git stash pop` \
If you want to move the changes to a new branch, you can run this useful one-liner: \
`git switch -c <new-branch-name>` \
<br />

> ***I accidentally made my changes on the main branch and committed them***

In this case, you won't be able to move your changes to an already existing branch easily. If you desperately need to do this, reach out to us \
Otherwise, create a new branch from main which includes your changes and then reset main: \
`git checkout -b <new-branch-name>` \
`git checkout main` \
`git reset --hard HEAD~1` \
`git checkout <new-branch-name>` \

***IMPORTANT NOTE*** - if you've committed more than once on main, you'll need to replace `HEAD~1` with `HEAD~n` where `n` is the number of commits you've made \
<br />

> ***I've made some changes that I want to push to the repo and other changes that I don't want to keep***

In the source control sidebar panel (the icon is three dots connected by lines), you will see all of the changes you've made. \
You can right-click on any of these and select 'Discard Changes' \
This will completely remove your changes, so make sure you don't want them before doing this! \
<br />

> ***I want to work on multiple rules at once!***

You can! You can create multiple branches for different rules and they will all be isolated from each other. \
Just make sure to use `checkout` commands or the console to switch to the relevant branch before you make changes. \
<br />

> ***The XLSX editor isn't loading or looks strange***

Ensure you have no other Excel-related extensions enabled. There may be conflicts if multiple VSCode extensions try to handle .xlsx files simultaneously. Try disabling other Excel extensions and restarting VSCode to fix this.
