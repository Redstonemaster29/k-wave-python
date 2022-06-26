import unittest.mock
import logging
import sys
from kwave.executor import Executor
import pytest
import os

check_is_linux = pytest.mark.skipif(not sys.platform.startswith('linux'), reason="Currently only implemented for linux.")


@check_is_linux
@pytest.mark.skipif(os.environ.get("CI") == 'true', reason="Running in GitHub Workflow.")
class TestExecutor(unittest.TestCase):

    @unittest.mock.patch('os.system')
    def test_system_call_correct(self, os_system):
        ex = Executor('cpu')

        input_filename = '/tmp/input.h5'
        output_filename = '/tmp/output.h5'
        try:
            ex.run_simulation(input_filename, output_filename, options='')
        except OSError:
            logging.info("Caught 'Unable to open file' exception.")

        call_str = f"export LD_LIBRARY_PATH=;OMP_PLACES=cores;OMP_PROC_BIND=SPREAD;" \
                   f" {ex.binary_path} -i {input_filename} -o {output_filename} "
        os_system.assert_called_once_with(call_str)


if __name__ == '__main__':
    unittest.main()
