import subprocess

debug_popen_impl = False

def popen_impl(command: 'list[str]'):
    if debug_popen_impl:
        print('Execute command: "%s"...' % ' '.join(command), end=' ')
    s = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = s.communicate()
    def write_logs(out: bytes, err: bytes):
        out = out.decode("utf-8")
        err = err.decode("utf-8")
        stdout_log = str(s.pid) + "_stdout.log"
        stderr_log = str(s.pid) + "_stderr.log"
        with open(stdout_log, "w") as f:
            f.write(out)
        with open(stderr_log, "w") as f:
            f.write(err)
        print(f"Output log files: {stdout_log}, {stderr_log}")
        
    if s.returncode != 0:
        if debug_popen_impl:
            print('failed')
        write_logs(out, err)
        raise RuntimeError(f"Command failed: {command}. Exitcode: {s.returncode}")
    if debug_popen_impl:
        print(f'result: {s.returncode == 0}')
        write_logs(out, err)