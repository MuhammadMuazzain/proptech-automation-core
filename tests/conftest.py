import sys
from pathlib import Path


# Ensure `import eaia` works in tests even if editable install isn't used.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
