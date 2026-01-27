import os
from subprocess import Popen, check_output

def runCMD(cmd, print_progress=False):
    # 复制当前环境变量，确保继承 conda 环境
    env = os.environ.copy()
    env["LIBGL_ALWAYS_INDIRECT"] = "0"
    env["QT_QPA_PLATFORM"] = "offscreen"

    print(cmd)

    if not print_progress:
        return check_output(cmd, shell=True, env=env)

    ex = Popen(cmd, shell=True, env=env)
    _, _ = ex.communicate()
    status = ex.wait()
    return status == 0
