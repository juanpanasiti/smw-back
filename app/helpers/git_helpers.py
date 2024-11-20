
import subprocess


def get_latest_git_tag() -> str:
    try:
        # Primero obtenemos el commit del último tag
        latest_commit = subprocess.check_output(
            ["git", "rev-list", "--tags", "--max-count=1"],
            text=True
        ).strip()

        # Luego obtenemos el tag asociado a ese commit
        latest_tag = subprocess.check_output(
            ["git", "describe", "--tags", latest_commit],
            text=True
        ).strip()

        return latest_tag
    except subprocess.CalledProcessError:
        return 'v0.0.1'  # En caso de error, como que no haya ningún tag
