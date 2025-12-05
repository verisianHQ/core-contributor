# core-contributor
Contribution framework for rules and test data with automated regression testing. Edit rules and test data, then validate against the PostgreSQL-based CORE engine.

# First-time Local Setup Steps

1) Create a free github account: https://github.com/signup
2) Install git, following the instructions here: https://git-scm.com/install/
3) Install VSCode, following the instructions here: https://code.visualstudio.com/download
4) Open your terminal
5) Navigate to the directory you wish to use for rule editing by using `cd` commands 
6) Clone this repo using the following command: \
       `git clone --recurse-submodules https://github.com/verisianHQ/core-contributor.git`
7) Right click on the 'core-contributor' folder and open with VSCode (if this is not an option, do `cd core-contributor` and then `code .`)
8) Make sure the in-built terminal is visible within VSCode - if it isn't, go to View > Terminal
9) You will need to setup the python environment, which will take a little bit of time. You can do this now or wait until you want to run a rule \
       - To setup now, make sure you are in the core-contributor folder in the VSCode terminal, and run one of the following: \
              WINDOWS: `.\setup\windows_setup.bat` \
              MAC: `./setup/bash_setup.sh`

*IMPORTANT NOTE* - if you start the setup script and stop it midway through, you may get some strange errors when you try to run rules. If you have any doubts, rerun the setup script, and make sure it completes.


# Rule and Test Data Editing Process

1) Make sure you are on the main branch and that it is up to date. Run the following two commands: \
       `git checkout main` \
       `git pull origin main`
2) Create a new branch to work on your changes, named as such: `<your-name>/<rule-id>/<change>` (eg `richard/CG00001/edit`): \
       `git branch <your-branch-name>`
3) Switch to your new branch: \
       `git checkout <your-branch-name>`
4) Edit a rule and test data as desired
5) When you want to run the rule against test data, make sure you are in the core-contributor folder and run one of the following: \
              WINDOWS: `.\run\windows_run.bat` \
              MAC: `./run/bash_run.sh` \
       - If you haven't run the setup script before, don't worry, it will run automatically when you execute this command
6) Check your run results in the `results` folder. Note that there is a separate `results` folder for each test case, which contains only the information relevant to that particular case
       - There will be a `results.json` file, with the code-produced rule output, and a `results.txt` file, which will summarise your results in a more human-readable format. Feel free to examine both
7) If you are unhappy with the results of your changes, continue to edit and run the rule until you are satisfied
8) Create a PR to add your changes to the repository. To do this, run the following commands: \
       `git add .` \
       `git commit -m "your custom message"` \
       `git push origin <your-branch-name>` \
       - It may be easier to use VSCode to stage, commit and push your changes for you. To do this, see the SUPPLEMENTARY GUIDE
9) Go to the online repository and create a pull request (PR) from your newly pushed branch
10) On the PR page, make sure the information at the top is correct. It should be: \
       `base: main ← compare: <branch-name>`
11) Name your PR using the format `<rule-id> <fix>` and add a brief description of your changes
12) On the PR, add reviewers (Els, Richard, Maximo) by clicking the cog in the top right corner, and add yourself as an assignee
13) You're done! Keep an eye on the PR to make sure the automated checks pass, as well as to respond to any comments from reviewers. If you need to edit any changes on the PR, you can simply checkout your branch (`git checkout <your-branch-name>`), make your changes, and commit and push them - the PR will automatically update!
14) If you want to start editing another rule, don't forget to run the below commands on VSCode terminal again: \
       `git checkout main` \
       `git pull origin main`

For further detail on any of these steps or git in general, see *SUPPLEMENTARY GUIDE HERE*


# YAML Validation

If you want to set up YAML validation for your rule files, follow these steps:

1) Go to the `Extensions` tab in the VSCode left sidebar
2) Search `yaml` and install the Red Hat YAML extension (it should be the top one)
3) Once it's installed, go to File > Preferences > Settings, and search 'yaml schema'.
4) Click the `Edit in settings.json` option under Yaml: Schemas
5) Paste the following into "yaml.schemas": \
       `"https://rule-editor.cdisc.org/api/schema": "/*.yml"`
6) There you go! You will now see errors and pop-ups if you try to use erroneous options in your yml files. If, after a few seconds, you don't see this behaviour, try restarting VSCode.
