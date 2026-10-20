# core-contributor
Contribution framework for rule storage, rule authoring and test data creation with automated regression testing. Create and/or edit rules and test data, then validate against the PostgreSQL-based CORE engine.

**BEFORE CONTRIBUTING, MAKE SURE YOU HAVE GONE THROUGH THE CDISC VOLUNTEERING ONBOARDING PROCESS** \
https://www.cdisc.org/volunteer

**SUPPLEMENTARY GUIDE** \
Instructions below will guide you step-by-step through the:
- First-time Local Setup Steps
- Rule Authoring and Test Data Creation Process
  
These steps should be sufficient to get you started but are very descriptive. If you wish to be guided in a more visual way, steps with print screens are available in the [supplementary guide](https://docs.google.com/document/d/15ydgj4AqtEnFtlXL-J4DLJV32q_Q71gKn0ucu4tYYQw/edit?pli=1&tab=t.0).

**KEY TERMS** \
You don't need to know Git or programming to follow this guide, but these words come up often:
- **Terminal**: a window where you type commands instead of clicking. In this guide it is always the terminal inside VSCode. Type (or paste) a command and press Enter to run it.
- **Repository (repo)**: the project folder, with all the rules and scripts, stored on GitHub. You download your own copy of it in step 6.
- **Branch**: your own separate copy of the rules to work on, so your changes don't affect anyone else until they are reviewed.
- **Commit**: a saved snapshot of your changes, with a short message describing them.
- **Push**: uploading your commits from your computer to GitHub.
- **Pull request (PR)**: a request, made on the GitHub website, to add your changes to the main repository after a review.
- **Virtual environment (venv)**: a private copy of Python for this project, created by the setup script. When it is active, `(venv)` is shown at the start of the terminal line.

# First-time Local Setup Steps

***IMPORTANT NOTE*** \
_You may need your IT support team to install some of the following software for you. In particular, the setup script requires Python 3.12 to run properly. If you don't have it installed, the script will attempt to install it for you, but this is likely to be blocked by your company settings. If so, you will need to contact IT._

**Follow steps 1 - 11 carefully.**

1) Create a free GitHub account: https://github.com/signup
2) Install Git, following the instructions here: https://git-scm.com/install
   - When prompted, ensure you check the **"Add to PATH"** option (or select **"Git from the command line and also from 3rd-party software"**)
   - Keep all other default settings throughout the installer
   - You DO NOT need to actually run Git as a program, so close any pop-ups that appear after the installation
3) Install VSCode, following the instructions here: https://code.visualstudio.com/download
   - On Windows, choose the **System Installer** (the file name starts with `VSCodeSetup`), ***not*** the User Installer (`VSCodeUserSetup`)
4) Open VSCode and a terminal within it: 
   - Top Menu → Terminal → New Terminal (check the three dots in the top menu if you don't see 'Terminal')
5) Create a new empty directory (folder) on your machine for storing the repository and subsequent rule authoring and editing. Navigate to it in the terminal using `cd` commands. Avoid OneDrive if possible. 
   - `cd` means "change directory": type `cd` followed by a space and the path of the folder, then press Enter (eg `cd Documents`). The terminal line always shows the folder you are currently in.
   - There is sometimes an AI 'helper' box popup in the terminal - make sure you are typing commands into the command line itself, not the box 
   - If any of the folder names you are navigating through have spaces (eg 'My Folder'), you will need to wrap the path in quotes,\
     eg: `cd "C:\Users\rich\Documents\Core Contributor Folder"`
6) Clone (download) this repo into that directory by running the following command (**DO NOT RUN MORE THAN ONCE**): \
       `git clone --recurse-submodules https://github.com/verisianHQ/core-contributor.git` 
   > **NOTE:** If you encounter `The term 'git' is not recognized as the name of a cmdlet, function, script file, or operable program.`, Git's installation directory has not been added to your system PATH. See [this StackOverflow answer](https://stackoverflow.com/questions/4492979/error-git-is-not-recognized-as-an-internal-or-external-command) for instructions on manually adding Git to your PATH.
   
   _***IMPORTANT NOTE***\
   Unless something goes badly wrong and you need to fully delete the entire directory, you should never need to run this command again._
   
7) In VSCode, select "Open Folder" and select the repository folder you just cloned - it should be called `core-contributor`
   
8) This should re-open a new terminal in the repository folder. If this doesn't happen, open a new terminal in VSCode and navigate to the repository folder again.
    
9) You will need to set up the python environment, which will take a little bit of time. 
    - Assuming you are in the core-contributor folder in the VSCode terminal, run one of the following depending on your operating system (ignore messages and warnings): 
        - WINDOWS: `.\setup\windows_setup.bat`
        - MAC: `./setup/bash_setup.sh` 
    - Windows might prompt you asking if you want to allow the script to run with administrator privileges and/or to install python - the answer is yes! The setup then continues in a new window - wait until it says `Setup completed successfully!`
    - MAC: if the installation of the dependencies fails on `psycopg2`, rerun the setup with `./setup/bash_setup.sh --binary`
         
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
    - The result should look like this (if there are other settings in the file, keep them, and make sure there is a comma between each setting and the next one): 
      ```json
      "yaml.schemas": {
          "https://rule-editor.cdisc.org/api/schema": "/*.yml"
      }
      ```
    - Save the `settings.json` 
    - There you go! You should now see schema validation in yaml files. If you don't see this behaviour after a few seconds, try restarting VSCode

11) Install the XLSX Editor plugin: 
    - In the VS Code file explorer, locate the `verisian-xlsx-editor-0.0.1.vsix` file in the root directory of this repository 
    - Right-click the file and select "Install Extension VSIX"

**You are now ready with the setup steps and can start with the rule authoring!**

# Rule Authoring and Test Data Creation Process

**_*IMPORTANT NOTE*_**\
_In the following section, the exact process to follow with relevant Git commands to be executed in the terminal are described. If in doubt, you can always fall back to this process. However, VSCode integrates with Git very effectively, and so there are intuitive point-and-click alternatives to all of the following commands with only simple configuration required._

_If you'd like to take advantage of this (strongly recommended for at least staging, committing and pushing your changes), please see the [supplementary guide](https://docs.google.com/document/d/15ydgj4AqtEnFtlXL-J4DLJV32q_Q71gKn0ucu4tYYQw/edit?tab=t.0#bookmark=id.v2ehj99lxmyr) for extra details and screenshots. \
You'll need to run the following commands to get it working: \
`git config --global user.email "<your-github-email>"` \
`git config --global user.name "<your-github-username>"`_

_Don't forget: whenever you type a command, you should be in the core-contributor folder that you created during the set-up steps._

## Command Line Process

**Create a Local Branch.**
1) Make sure you are on the main branch and that both the main branch and the engine submodule are up to date. To do this, run the following three commands: \
       `git checkout main` \
       `git pull origin main` \
       `git submodule update --recursive`
   
2) Create a new branch to work on your changes, named as such: `<your-name>/<rule-id>/<change>` (eg `richard/CORE-000001/edit`): \
       `git branch <your-branch-name>`
   
   _Note that only branch names according to the following regex are allowed: **^[a-zA-Z]+/(CORE-[0-9]{6}|CG[0-9]{4}|FB[0-9]{4}|AD[0-9]{4})/(edit|create|delete)(-[0-9]+)?$**_ \
   _In plain words: your name using letters only (no digits or spaces), then `/`, then the rule ID (`CORE-` followed by 6 digits, or `CG`, `FB` or `AD` followed by 4 digits), then `/`, then `edit`, `create` or `delete`. If you need a second branch for the same rule and change, add a dash and a number at the end (eg `richard/CORE-000001/edit-2`)._

   **_*IMPORTANT NOTE*_**\
   _Whenever you create a local branch to work on a rule, ensure that you are on the main branch. If you create a new local branch, when you are already on a local branch, the new branch will branch off the
   local branch and not from main. If you would then want to merge changes from your new local branch, it will merge with the first local branch and not with the main branch. Therefore, ensure to be on the main
   branch first prior to creating a local branch (git checkout main). Once the local branch exists, you can check it out from any branch._
   
3) Switch to your new branch: \
       `git checkout <your-branch-name>`

**Set-up Rule Folder.**

**_*IMPORTANT NOTE*_**\
_Step 4 is only applicable in case you want to create a rule for which the folder does not exist yet in the GitHub repository. It is therefore important to first check if a folder is already present. If no folder is present, you can automatically generate the required folder structure for a new rule including a blank YAML template and template Excel files (negative and positive) for the test data._

4) Initialize your new rule folder structure:
   - In the base directory of the project, activate the virtual environment by running:
     - WINDOWS: `.\venv\Scripts\activate`
     - MAC: `source ./venv/bin/activate`
   - Then run the following command in your terminal: \
       `python new-rule.py`
   - It will prompt you a few times.
     - It will ask which rules directory to use (`sdtm` for `rules/`, `adam` for `adam_rules/`), whether the rule is part of a bundled rule structure sharing test cases (for a single new rule, answer `n`) and whether you want the test cases in CSV or XLSX format (the steps below assume XLSX).
     - If the NEW-RULE folder already exists, it will check you definitely want to make a new one. (NOTE: If the empty folder is a leftover from a previous branch, which is likely, you SHOULD run the script and overwrite the folder to make a new one, as this will set-up the template properly for you).
     - You will also be prompted to enter the number of positive and negative test cases you want to create. Don't worry if you realise you need more later. You can easily add more manually.
   - This will create a `rules/NEW-RULE` folder with all necessary subdirectories and template files (eg `new-rule.yml` and `positive/01/data/new-rule-positive-01.xlsx`).
   - The NEW-RULE folder should NOT be renamed. It will receive its final name after the PR has been merged.

**Write or Edit Rule.**

5) Edit a rule as desired:
   - Ensure that you save any changes (File → Save, or Ctrl/Cmd + S)
     
6) Create test data as desired:
   - Ensure that positive test data are created (= no data issues expected to be flagged for that particular rule).
   - Ensure that negative test data are created (= data issues expected to be flagged for that particular rule).
   - Each dataset is a separate sheet named after the dataset (eg `cm.xpt`) and listed in the `Datasets` sheet. Row 1 holds the variable names, rows 2 - 4 hold the metadata (label, type, length) and the data starts from row 5. The `Library` sheet holds the standard and version (eg `sdtmig`, `3-4`) the rule is tested against.
   - In addition to creating negative test data, predefined discrepancies should be marked in the negative test data. This will ensure that the validation can be automatically tested based on the expected errors you've indicated upfront.
   - To mark predefined discrepancies in the negative test data, highlight each cell causing an error in **yellow** (the test script only looks for yellow highlighting) and complete the `Validation` sheet in the negative test data:
     - **Error group**:
       - Add each error as a new validation group (note that this might not be only a single row - for example if you highlight two cells that will cause a single error, and be outputted as a single error, then you should create TWO rows in the same validation group (ie both in group '1')).
       - Create groups using sequential numbers for the validation group column.
     - **Sheet**: Name of the data sheet with the error e.g. cm.xpt
     - **Error level**:
       - Add 'Record' if it is a normal row error
       - 'Variable' if it is an error related to an entire column
       - 'Dataset' if it is an error related to a whole dataset (ie missing ae.xpt sheet or similar).
     - **Row num**: Provide the row number (using the row count of the excel sheet - note that the variable names are in row 1 and the first data row is row 5 due to the metadata rows we always have in the sheets).
     - **Variable**: Provide the variable name (found in the first row of the column) - with the row number this fully identifies the error cell.
     - **Error value**:
       - Finally, copy the error value from the highlighted cell into the 'Error value'.
       - If the highlighted cell has no value, use '[ABSENT]' to indicate this (including the square brackets).
   - Repeat for all the highlighted error cells (remembering to group using the 'Error group' column where appropriate).
   - Ensure that you save any changes (File → Save, or Ctrl/Cmd + S).
  
**Perform Unit Testing.**
     
7) When you want to run the rule against test data, make sure you are in the core-contributor folder and run one of the following:\
   WINDOWS: `.\run\windows_run.bat` \
   MAC: `./run/bash_run.sh` 
   - If you haven't run the setup script before, don't worry; it will run automatically when you execute this command.
   - You will be prompted to select the rule you wish to run (eg `NEW-RULE`), as well as the test case(s).
   - This runs the rules in the `rules` folder. To run ADaM rules (`adam_rules` folder), see [Advanced Usage](#advanced-usage).

**Verify Results.**
     
8) Check your run results in the `results` folder.
   - Note that there is a separate `results` folder for each test case (eg `rules/NEW-RULE/negative/01/results`), which contains only the information relevant to that particular case.
   - There will be a `results.json` file, with the code-produced rule output, and a `results.txt` file, which will summarise your results in a more human-readable format. Feel free to examine both.
   - Once you've run the rule, check to make sure there are no issues mentioned in the rule output - if the highlighting or validation in the validation sheet hasn't been done correctly, you will see an `***ISSUES***` section in `results.txt` (and `unvalidated_highlights`, `unhighlighted_validations` or `unmatched_validation` entries in `results.json`), and you can correct them.
   - Ideally you see no issues, and `"validated": true` for every error in the negative test case results (shown as `Fully Validated in Test Case: Yes` in `results.txt`). 

**_*IMPORTANT NOTE*_**\
_Note that if the rule or test data is wrong (and you're getting unexpected errors or lacking errors you expect to see), you will almost certainly see some highlight/validation issues. In this case, obviously the priority is to correct the rule and test data before checking the highlights and validation!_

9) If you are unhappy with the results of your changes, continue to edit and run the rule until you are satisfied.

**Request Review via PR.**

10) Create a PR to add your changes to the repository. To do this, run the following commands: \
       `git add .` (selects all your changes - note the dot at the end) \
       `git commit -m "your custom message"` (saves them as a commit, with a short description of what you changed between the quotes) \
       `git push origin <your-branch-name>` (uploads the commit to GitHub)
       - The first time you push, you may have to log in to github
       - Make sure you have re-run the rule (step 7) after your last change, so that the updated `results.json` files are included in your commit - the automated checks on the PR re-run your rule and compare the output against them (`results.txt` files are not committed)
         
11) Go to the online repository (https://github.com/verisianHQ/core-contributor) and create a pull request (PR) from your newly pushed branch: GitHub usually shows a yellow banner with a **Compare & pull request** button for a branch you have just pushed
    
12) On the PR page, make sure the information at the top is correct. It should be: \
       `base: main ← compare: <branch-name>`
  
13) Name your PR using the format `<rule-id> <fix>` and add a brief description of your changes. Or if you are making a new rule with your PR, `<conformance-rule-id> create`.
    
14) On the PR, reviewers are added automatically (review from 'Rules Team' and 'Engineers Team' are required). Practically speaking, there is no need to assign yourself as you will be notified by default but it is 'good practice' to do it.
    
15) You're done!
    - Keep an eye on the PR to make sure the automated checks (YAML schema validation and a re-run of your test cases) pass, as well as to respond to any comments from reviewers.
    - If you need to edit any changes on the PR, you can simply checkout your branch (`git checkout <your-branch-name>`), make your changes, and commit and push them - the PR will automatically update!

**Approval - Merge PR**

16) Once your PR is approved, merge your changes to the source code. If you created a new rule in your PR, a new CORE-id will be assigned to it automatically (the NEW-RULE folder and files are renamed).

**Let's do another rule!**    

17) If you want to start editing another rule, don't forget to run the below commands on VSCode terminal again: \
       `git checkout main` \
       `git pull origin main` \
       `git submodule update --recursive`

For further detail on any of these steps or git in general, see the [supplementary guide](https://docs.google.com/document/d/15ydgj4AqtEnFtlXL-J4DLJV32q_Q71gKn0ucu4tYYQw/edit?pli=1&tab=t.0)


# Advanced Usage

Below are some additional functionalities in the test script. To take advantage of this, you will need to run the test script directly, rather than using the run script.
NOTE: You must still run all First-time Local Setup Steps from above before this.

1) In VSCode terminal, in the core-contributor directory, activate the virtual environment by running one of the following (you need to do this every time you open a new terminal; `(venv)` is then shown at the start of the terminal line):
   - WINDOWS: `.\venv\Scripts\activate`
   - MAC: `source ./venv/bin/activate`
   
2) You can now run the test script directly with various options:
   - `python test.py` - Interactive mode (prompts you for rule and test case selection)
   - `python test.py -r <rule-id>` - Test all cases for a specific rule
   - `python test.py -r <rule-id> -tc <test-case>` - Test a specific case (eg `positive/01`)
   - `python test.py -r <rule-id> -v` - Test with verbose output (prints results to terminal)
   - `python test.py --all-rules` - Test all rules
   - `python test.py -s adam` - Test ADaM rules (in the `adam_rules` folder) instead of SDTM rules (the default); can be combined with the options above
   - `python test.py -r <rule-id> -md <path-to-meddra-files>` - Provide external dictionary files (`-wd` WHODrug, `-md` MedDRA, `-un` UNII, `-mrt` Med-RT, `-lo` LOINC, `-sno` SNOMED). For UNII, Med-RT, LOINC and SNOMED you can pass `default` to use the dummy dictionaries in `dummy_ex_dicts`
   - `python test.py -h` - See all available options
3) When you're done, you can deactivate the venv by running `deactivate`

See also [streamlit/README.md](streamlit/README.md) for the rules contributor dashboard and [.regression/README.md](.regression/README.md) for regression testing across all rules.


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
`git checkout <new-branch-name>`

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
<br />

> ***I'm getting a pgserver-related subprocess error after I tried running the test script***

Close VSCode and reopen it WITHOUT selecting "Run As Administrator". PostgreSQL blocks the actual database server that the file "initdb.exe" spins up from running directly under a Windows administrator account for security reasons. Then, re-run your test script. If the same error appears, then delete the `venv` folder in your repo and run the setup script again as mentioned in "First Time Local Setup Steps" section 9 above and then afterwards, simply re-run the test script again.
<br />

> ***Windows: activating the virtual environment fails with "running scripts is disabled on this system"***

Windows blocks PowerShell scripts by default. Run this command once in the VSCode terminal (it only applies to your user account), then try again: \
`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` \
If your company settings don't allow this, contact your IT support team.
<br />

> ***Mac: running a setup or run script fails with "permission denied"***

Run the script through `bash` instead, eg `bash ./setup/bash_setup.sh` or `bash ./run/bash_run.sh`.
<br />
