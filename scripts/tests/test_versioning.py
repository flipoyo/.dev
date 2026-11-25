"""Tests of versioning.py on a small fake cawaqs tree."""

import importlib.util
from pathlib import Path

import pytest

SPEC = importlib.util.spec_from_file_location("versioning", Path(__file__).resolve().parents[1] / "versioning.py")
v = importlib.util.module_from_spec(SPEC)
import sys

sys.modules["versioning"] = v
SPEC.loader.exec_module(v)


@pytest.fixture
def tree(tmp_path):
    (tmp_path / "src/libaq/src").mkdir(parents=True)
    (tmp_path / "pixi.toml").write_text('[workspace]\nname = "cawaqs"\nversion = "4.1.3"\n')
    (tmp_path / "src/param_caw.h").write_text('#define NVERSION_CAW "4.1.3" // x\n')
    (tmp_path / "src/Makefile").write_text("V_CAW=4.1.3\nV_AQ=0.74\n")
    (tmp_path / "CITATION.cff").write_text("version: '4.1.3'\ndate-released: '2026-01-01'\n")
    (tmp_path / "README.md").write_text("badge Current_version-4.1.3-orange\nthe SemVer in `pixi.toml` (`4.1.3`)\n")
    (tmp_path / "src/libaq/src/Makefile").write_text("V_AQ=0.74\nV_LP=1.24\n")
    (tmp_path / "src/libaq/src/param_AQ.h").write_text("#define VERSION_AQ 0.74\n")
    return tmp_path


def test_next_version():
    assert v.next_version("4.1.3", "patch") == "4.1.4"
    assert v.next_version("4.1.3", "minor") == "4.2.0"
    assert v.next_version("4.1.3", "major") == "5.0.0"


def test_next_build():
    assert v.next_build("0.74") == "0.75"
    assert v.next_build("0.99", major=True) == "1.00"
    with pytest.raises(SystemExit):
        v.next_build("0.99")


def test_bump_version_moves_every_copy(tree):
    assert v.main(["bump-version", "minor"], tree) == 0
    assert 'version = "4.2.0"' in (tree / "pixi.toml").read_text()
    assert '"4.2.0"' in (tree / "src/param_caw.h").read_text()
    assert "V_CAW=4.2.0" in (tree / "src/Makefile").read_text()
    assert "version: '4.2.0'" in (tree / "CITATION.cff").read_text()
    assert "date-released: '2026-01-01'" not in (tree / "CITATION.cff").read_text()
    assert (tree / "README.md").read_text().count("4.2.0") == 2
    assert v.main(["check-version"], tree) == 0


def test_dry_run_writes_nothing(tree):
    before = (tree / "pixi.toml").read_text()
    assert v.main(["bump-version", "patch", "--dry-run"], tree) == 0
    assert (tree / "pixi.toml").read_text() == before


def test_a_copy_edited_by_hand_fails_and_blocks_a_bump(tree):
    (tree / "src/param_caw.h").write_text('#define NVERSION_CAW "4.0.0"\n')
    assert v.main(["check-version"], tree) == 1
    with pytest.raises(SystemExit):
        v.main(["bump-version", "patch"], tree)
    assert 'version = "4.1.3"' in (tree / "pixi.toml").read_text()


def test_bump_build_moves_the_library_and_cawaqs_copy(tree):
    assert v.main(["bump-build", "libaq"], tree) == 0
    assert "V_AQ=0.75" in (tree / "src/libaq/src/Makefile").read_text()
    assert "V_AQ=0.75" in (tree / "src/Makefile").read_text()
    assert "VERSION_AQ 0.75" in (tree / "src/libaq/src/param_AQ.h").read_text()
    assert "V_LP=1.24" in (tree / "src/libaq/src/Makefile").read_text()


def test_library_header_disagreeing_fails(tree):
    (tree / "src/libaq/src/param_AQ.h").write_text("#define VERSION_AQ 0.73\n")
    assert v.main(["check-version"], tree) == 1
