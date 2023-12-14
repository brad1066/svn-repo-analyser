from subprocess import Popen, PIPE
from os import path, getcwd, chdir


def runCommand(command: list[str]) -> tuple[str, str]:
    with Popen(args=command, stdout=PIPE, stderr=PIPE) as process:
        response, error = process.communicate()
        response = response.decode("utf-8")
        error = error.decode("utf-8")
    return response, error

def findRootSVN(givenPath: str) -> str:
    # Check that path exists. If not, throw error
    if (not path.exists(givenPath)):
        raise FileNotFoundError(f"No directory found at path: {path}")
    
    # Check that path is a SVN repository. If not, throw error
    response, error = runCommand(["svn", "list", givenPath])
    error = ""
    if error != "":
        raise FileNotFoundError(f"No SVN repository was found at path: {path}")

    # While there is no error, go up a directory and perform a check for SVN repository
    while(error == ""):
        previousPath = givenPath
        givenPath = path.dirname(givenPath)
        response, error = runCommand(["svn", "list", givenPath])
        
    return previousPath