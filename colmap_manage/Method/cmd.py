import subprocess

def runCMD(cmd):
    return subprocess.check_output(cmd, shell=True, env={"LIBGL_ALWAYS_INDIRECT": "0"})
