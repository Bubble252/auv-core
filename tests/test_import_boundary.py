from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_core_import_does_not_load_planners_or_learning_stacks() -> None:
    project = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys\n"
            "import auv_core\n"
            "forbidden = {'auv_planner', 'auv_local', 'auv_rl', 'auv_lowlevel', "
            "'auv_isaaclab', 'torch', 'holoocean', 'rclpy', 'python_vehicle_simulator'}\n"
            "loaded = forbidden.intersection(sys.modules)\n"
            "if loaded:\n"
            "    raise SystemExit(sorted(loaded))\n"
            "print('ok')\n",
        ],
        cwd=project,
        env={"PYTHONPATH": str(project / "src")},
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "ok"


def test_public_imports_remain_lazily_available() -> None:
    project = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from auv_core import State, ThreeDAlosGuidance\n"
            "assert State.__name__ == 'State'\n"
            "assert ThreeDAlosGuidance.__name__ == 'ThreeDAlosGuidance'\n"
            "print('ok')\n",
        ],
        cwd=project,
        env={"PYTHONPATH": str(project / "src")},
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "ok"
