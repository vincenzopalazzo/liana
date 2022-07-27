import os

from test_framework.utils import (
    TailableProc,
    VERBOSE,
    LOG_LEVEL,
    MINISAFED_PATH,
)


class Minisafed(TailableProc):
    def __init__(
        self,
        datadir,
        main_desc,
        bitcoind_rpc_port,
        bitcoind_cookie_path,
    ):
        TailableProc.__init__(self, datadir, verbose=VERBOSE)

        self.prefix = os.path.split(datadir)[-1]

        self.conf_file = os.path.join(datadir, "config.toml")
        self.cmd_line = [MINISAFED_PATH, "--conf", f"{self.conf_file}"]

        with open(self.conf_file, "w") as f:
            f.write(f"data_dir = '{datadir}'\n")
            f.write("daemon = false\n")
            f.write(f"log_level = '{LOG_LEVEL}'\n")

            f.write(f'main_descriptor = "{main_desc}"\n')

            f.write("[bitcoind_config]\n")
            f.write('network = "regtest"\n')
            f.write(f"cookie_path = '{bitcoind_cookie_path}'\n")
            f.write(f"addr = '127.0.0.1:{bitcoind_rpc_port}'\n")
            f.write("poll_interval_secs = 1\n")

    def start(self):
        TailableProc.start(self)
        self.wait_for_logs(
            [
                "Database initialized and checked",
                "Connection to bitcoind established and checked.",
            ]
        )

    def stop(self, timeout=5):
        return TailableProc.stop(self)

    def cleanup(self):
        try:
            self.stop()
        except Exception:
            self.proc.kill()
