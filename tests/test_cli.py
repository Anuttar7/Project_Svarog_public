import subprocess
import sys
import os

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def test_cli_help():
    cmd = [sys.executable, os.path.join(REPO_ROOT, "run_all.py"), "--help"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0
    assert "Svarog" in res.stdout or "sizing" in res.stdout


def test_cli_sizing_subcommand():
    cmd = [sys.executable, os.path.join(REPO_ROOT, "run_all.py"), "sizing"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0
    assert "SVAROG TRAC BOOM SIZING ANALYSIS" in res.stdout
    assert "SAFE (Adequate)" in res.stdout


def test_cli_second_moment_subcommand():
    cmd = [sys.executable, os.path.join(REPO_ROOT, "run_all.py"), "second-moment"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0
    assert "THIN-SHELL FORMULATION" in res.stdout
    assert "839" in res.stdout


def test_cli_all_quick_subcommand():
    cmd = [sys.executable, os.path.join(REPO_ROOT, "run_all.py"), "all", "--quick"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0
    assert "All analyses finished successfully." in res.stdout
