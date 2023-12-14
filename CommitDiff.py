class CommitDiff:
    def __init__(self, old_commit, new_commit):
        self.old_commit = old_commit
        self.new_commit = new_commit

    def get_changes(self):
        old_paths = set(self.old_commit.paths)
        new_paths = set(self.new_commit.paths)

        added_paths = new_paths - old_paths
        deleted_paths = old_paths - new_paths
        modified_paths = old_paths.intersection(new_paths)

        print("Added paths:", list(added_paths))
        print("Deleted paths:",list(deleted_paths))
        print("Modified paths",list(modified_paths))

        return {
            "added": list(added_paths),
            "deleted": list(deleted_paths),
            "modified": list(modified_paths)
        }

    