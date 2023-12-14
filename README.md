# SVN Repository Analyser

## Project Specification

- You will develop a tool that studies the commits on a Subversion server to determine to what degree a team is using good XP practices.
- Your source of data will the log command in svn. Your code will run the svn -v log --xml command which forces the output of the log to be in XML format.

### Decomposing Project Description 
 1. Data Retrieval:
    1. Ability to run `svn -v log --xml` command

 2. Data Processing:
    1. Parse these XML logs and extract relevant information

 3. Commit Message Analysis:
    1. Check for suitably long commit messages
    1. Identify whether commit messages indicate if there is a Driver and Navigator

 4. Codebase Analysis:
    1. Detect the presence of .idea folder and other IDE-created files and folders in commit paths
    1. Use svn diff to determine whether commits grow the codebase or introduce large new files suddenly

 5. Unit Test Detection:
    1. Check for the presence of unit tests within the commits or the repository

 6. Test Driven Development Detection
    1. Check for the presence of unit tests before the presence of a codebase that the unit tests are testing

 7. Commit Reporting:
     1. Number of commits from eaech programmer
     1. Number of commits from each programming pair

 8. Provide a user-friendly interface for input and output:
     1. Display generated statistics in a readable format
     1. Generate report summarizing the analysis and key findings

 9. Configuration options:
    1. Allow users to configure the tool's behaviour, suc as specifying commit message length thresholds



