from PIL import Image
import cv2


class IKeyframeSelector:
    def get_frame_position(self, keyframe_index: int) -> int:
        """
        根据关键帧索引返回对应的视频帧序号

        Args:
            keyframe_index: 关键帧的索引（即第几个采样，从0开始）

        Returns:
            int: 对应的视频帧序号（即帧在视频中的位置）

        Note:
            实现类应该定义具体的采样策略，如均匀采样、动态间隔等
        """
        raise NotImplementedError


class KeyframeSampler:
    @staticmethod
    def sample(video_path: str, keyframe_count: int, frame_selector: IKeyframeSelector | None = None) -> list[Image.Image]:
        """
        按照固定时间间隔从视频中采样关键帧

        Args:
            video_path: 视频文件路径
            keyframe_count: 采样帧数量

        Returns:
            list[Image.Image]: 采样到的关键帧PIL图像列表
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError("无法打开视频文件")

        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0:
            cap.release()
            raise ValueError("无法获取视频帧率")

        sampling_frames: list[int] = []
        if frame_selector is not None:
            sampling_frames = [frame_selector.get_frame_position(x) for x in range(keyframe_count)]
        else:
            total_frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            interval = total_frame_count // keyframe_count
            for i in range(keyframe_count):
                sampling_frames.append(i * interval)
        sampled_frame_index = 0
        keyframes = []
        processed_frame_index = 0

        while sampled_frame_index <= len(sampling_frames) - 1:
            ret, frame = cap.read()

            if not ret:
                break

            if processed_frame_index == sampling_frames[sampled_frame_index]:
                print(f"采样第{sampled_frame_index}个关键帧(视频第{processed_frame_index}帧)")
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(frame_rgb)
                keyframes.append(pil_image)
                sampled_frame_index += 1

            processed_frame_index += 1

        cap.release()

        return keyframes
