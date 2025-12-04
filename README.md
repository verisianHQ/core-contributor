# core-contributor
Contribution framework for rules and test data with automated regression testing. Edit rules and test data, then validate against the PostgreSQL-based CORE engine.

# Steps

1) Install git
2) Install vscode
3) Open your terminal
4) Navigate to the directory you wish to use for rule editing by using `cd` commands 
5) Clone this repo using the following command: \
       `git clone --recurse-submodules https://github.com/verisianHQ/core-contributor.git`
6) Right click on the 'core-contributor' folder and open with VSCode (if this is not an option, do `cd core-contributor` and then `code .`
7) Make sure the in-built terminal is visible within VSCode - if it isn't, go to View > Terminal
8) You will need to setup the python environment, which will take a little bit of time. You can do this now or wait until you want to run a rule
  a) To setup now, make sure you are in the core-contributor folder in the VSCode terminal, and run one of the following: \
        WINDOWS: `.\setup\windows_setup.bat` \
        MAC: `./setup/bash_setup.sh`
9) Edit a rule and test data as desired
10) When you want to run the rule against test data, make sure you are in the core-contributor folder and run one of the following: \
        WINDOWS: `.\run\windows_run.bat` \
        MAC: `./run/bash_run.sh`
  a) If you haven't run the setup script, don't worry, it will run automatically when you execute this command
11) Check your run results in the `results` folder. Note that there is a separate `results` folder for each test case, which contains only the information relevant to that particular case
12) If everything looks good: FOLLOW THE GUIDE FOR ADD, COMMIT AND PRs

*IMPORTANT NOTE* - if you start the setup script and stop it midway through, you may get some strange errors when you try to run rules. If you have any doubts, rerun the setup script, and make sure it completes.

# YAML Validation

If you want to set up YAML validation for your rule files, follow these steps:
1) Go to the `Extensions` tab in the VSCode left sidebar
2) Search `yaml` and install the Red Hat YAML extension (it should be the top one)
3) Once it's installed, go to File > Preferences > Settings, and search 'yaml schema'. Click the `Edit in settings.json` option under Yaml: Schemas
4) Paste the following into "yaml.schemas": \
       `"https://rule-editor.cdisc.org/api/schema": "/*.yml"`
5) There you go! You will now see errors and pop-ups if you try to use erroneous options in your yml files. If, after a few seconds, you don't see this behaviour, try restarting VSCode.
