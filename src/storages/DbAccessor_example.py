from storages.DbAccessor import DbAccessor


def example():
    with DbAccessor() as db_accessor:
        for v in db_accessor.get_videos():
            print(f"Video(id={v.id}, file_path={v.file_path})")
            print()
