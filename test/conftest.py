import sys
from pathlib import Path

src_dir = Path(__file__).resolve().parents[1] / 'src'
sys.path.append(str(src_dir))