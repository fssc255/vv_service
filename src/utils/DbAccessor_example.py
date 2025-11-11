from utils.DbAccessor import DbAccessor


def example():
    with DbAccessor() as db_accessor:
        for v in db_accessor.get_videos():
            print(f"Video: {v.content}")
            result = db_accessor.get_video_metadata(v.id)
            if result is not None:
                print(result)
            else:
                print("未找到元数据信息")
            print()
