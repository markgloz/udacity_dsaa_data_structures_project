class Group:
    def __init__(self, name) -> None:
        self.name = name
        self.groups = []
        self.users = []
    
    def add_group(self, group) -> None:
        self.groups.append(group)

    def add_user(self, user) -> None:
        self.users.append(user)

    def get_groups(self) -> list:
        return self.groups
    
    def get_users(self) -> list:
        return self.users
    
    def get_name(self) -> str:
        return self.name


def is_user_in_group(user, group: Group):
    """
    Return True if user is in the group, False otherwise.

    Args:
      user(str): username/ id
      group(class: Group): group to check user membership against
    """
    if user in group.get_users():
        return True
    else:
        for sub_group in group.get_groups():
            if sub_group:
                result = is_user_in_group(user, sub_group)
                if result:
                    return result
    return False

parent = Group("parent")
child = Group("child")
sub_child = Group("subchild")

sub_child_user = "sub_child_user"
sub_child.add_user(sub_child_user)

child.add_group(sub_child)
parent.add_group(child)

# Test case 1 - basic test
assert is_user_in_group(sub_child_user, sub_child) == True

# Test case 2 - basic test
assert is_user_in_group(sub_child_user, child) == True

# Test case 3 - basic test
assert is_user_in_group(sub_child_user, parent) == True

# Test case 4 - test invalid users
parent_user_1 = 'Sys admin'
parent_user_2 = 'Org admin'
invalid_parent_user_3 = 'User 1'
parent.add_user(parent_user_1)
parent.add_user(parent_user_2)
assert is_user_in_group(parent_user_1, parent) == True
assert is_user_in_group(parent_user_2, parent) == True
assert is_user_in_group(invalid_parent_user_3, parent) == False

# Test case 5 - test complex, large, branched groups
sub_child_2 = Group('subchild_2')
parent.add_group(sub_child_2)

sub_child_3 = Group('subchild_3')
parent.add_group(sub_child_3)

sub_sub_child_3 = Group('sub_sub_child_3')
sub_child_3.add_group(sub_sub_child_3)

sub_child_4 = Group('subchild_4')
parent.add_group(sub_child_4)

sub_child_2_user = 'subchild_2_user'
sub_child_2.add_user(sub_child_2_user)
sub_child_3_user = 'subchild_3_user'
sub_child_3.add_user(sub_child_3_user)
sub_sub_child_3_user = 'sub_child_3_group_user'
sub_sub_child_3.add_user(sub_sub_child_3_user)
sub_child_4_user = 'subchild_4_user'
sub_child_4.add_user(sub_child_4_user)

assert is_user_in_group(sub_sub_child_3_user, parent) == True
assert is_user_in_group(sub_child_2_user, parent) == True
assert is_user_in_group(sub_sub_child_3_user, sub_child_2) == False

# Test case 6 - test duplicate ids within duplicate group names.
# This subproject is purely focused on search, so duplicate usernames/ ids are allowed.
duplicate_1 = Group('duplicate_1')
duplicate_1.add_user('duplicate_1_user')
duplicate_2 = Group('duplicate_2')
duplicate_2.add_user('duplicate_2_user')
duplicate_2.add_user('duplicate_2_user')
assert is_user_in_group('duplicate_1_user', duplicate_1) == True
assert is_user_in_group('duplicate_2_user', duplicate_2) == True
assert is_user_in_group('duplicate_1_user', duplicate_2) == False
assert is_user_in_group('duplicate_2_user', duplicate_1) == False
duplicate_1.add_group(duplicate_2)
assert is_user_in_group('duplicate_1_user', duplicate_1) == True
assert is_user_in_group('duplicate_2_user', duplicate_2) == True
assert is_user_in_group('duplicate_1_user', duplicate_2) == False
assert is_user_in_group('duplicate_2_user', duplicate_1) == True

# Test case 7 - null
null_group = Group(None)
valid_user = 'A valid user'
null_user = None
null_group.add_user(valid_user)
assert is_user_in_group(valid_user, null_group) == True
null_group.add_user(null_user)
assert is_user_in_group(null_user, null_group) == True
assert is_user_in_group('Unknown user', null_group) == False

# Test case 8 - empty
empty_group = Group('')
valid_user = 'A valid user'
empty_user = ''
assert is_user_in_group(valid_user, empty_group) == False
assert is_user_in_group(empty_user, empty_group) == False

empty_group.add_user(valid_user)
assert is_user_in_group(valid_user, empty_group) == True
empty_group.add_user(empty_user)
assert is_user_in_group(empty_user, empty_group) == True
assert is_user_in_group('Unknown user', empty_group) == False

# Test case 9 - overwrite group
original_group = Group('Original group')
original_group.add_user('User 1')
assert is_user_in_group('User 1', original_group) == True
overwriten_group = Group('Original group')
assert is_user_in_group('User 1', overwriten_group) == False