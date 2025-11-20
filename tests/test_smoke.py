from pathlib import Path

def test_project_structure():
    assert Path("final_project").exists()

    assert Path("final_project/app.py").exists()
    assert Path("final_project/models.py").exists()
    assert Path("final_project/storage.py").exists()