from subprocess import Popen, check_output

def runCMD(cmd, print_progress=False):
    if not print_progress:
        return check_output(cmd, shell=True, env={"LIBGL_ALWAYS_INDIRECT": "0"})

    ex = Popen(cmd, shell=True)
    _, _ = ex.communicate()
    status = ex.wait()
    return status == 0
