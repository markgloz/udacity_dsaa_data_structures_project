import os

"""
Useful functions:

print(os.path.isdir("testdir"))
print(os.path.isfile("testdir/t1.c"))
print(os.path.isfile("testdir/subdir1"))
print(os.listdir("testdir"))
print(os.listdir("testdir/subdir1"))
print(os.listdir("testdir/subdir3"))
print(os.path.join("testdir", "testdir/subdir1"))
print("testdir/t1.c".endswith(".c"))
"""


def find_files(suffix: str, path: str) -> list[str]:
    """
    Find all files beneath path with file name suffix.

    Note that a path may contain further subdirectories
    and those subdirectories may also contain further subdirectories.

    There are no limit to the depth of the subdirectories can be.

    Args:
      suffix(str): suffix if the file name to be found
      path(str): path of the file system

    Returns:
       a list of paths
    """

    if not suffix or not path or not os.path.isdir(path):
        return []

    files = []

    contents = os.listdir(path)

    for content in contents:
        subpath = os.path.join(path, content)
        if os.path.isfile(subpath):
            if subpath.endswith(suffix):
                files.append(subpath)
        elif os.path.isdir(subpath):
            files.extend(find_files(suffix, subpath))
        else:
            continue

    return files


# Add your own test cases: include at least three test cases
# and two of them must include edge cases, such as null, empty or very large values

# Test Case 1
files = find_files(".c", "testdir")
answer = ["testdir/subdir1/a.c", "testdir/subdir3/subsubdir1/b.c", "testdir/subdir5/a.c", "testdir/t1.c"]
assert len(files) == len(answer)
for file in files:
    assert file in answer

# Test Case 2
files = find_files(".h", "testdir")
answer = ["testdir/subdir1/a.h", "testdir/subdir3/subsubdir1/b.h", "testdir/subdir5/a.h", "testdir/t1.h"]
assert len(files) == len(answer)
for file in files:
    assert file in answer

# Test Case 3
files = find_files(".gitkeep", "testdir")
answer = ["testdir/subdir2/.gitkeep", "testdir/subdir4/.gitkeep"]
assert len(files) == len(answer)
for file in files:
    assert file in answer

# Test Case 4 - Test NoneType
files = find_files(None, "testdir")
answer = []
assert files == answer

files = find_files(None, None)
answer = []
assert files == answer

files = find_files(".h", None)
answer = []
assert files == answer

# Test Case 5 - Test empty
files = find_files("", None)
answer = []
assert files == answer

files = find_files("", "")
answer = []
assert files == answer

files = find_files("", "testdir")
answer = []
assert files == answer

# Test Case 6 - Test non-existent files
files = find_files(".py", "testdir")
answer = []
assert files == answer

# Test Case 7 - Test non-existent dir
files = find_files(".py", "notestdir")
answer = []
assert files == answer

# Test Case 8 - Test subdir
files = find_files(".c", "testdir/subdir3")
answer = ["testdir/subdir3/subsubdir1/b.c"]
assert files == answer
