from PIL import Image
import numpy as np
import cv2


class IKeyframeSelector:
    def get_frame_position(self, keyframe_index: int, total_frame_count: int) -> int:
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


class KeyframesSampler:
    @staticmethod
    def sample(video_file_path: str, keyframe_count: int, keyframe_selector: IKeyframeSelector | None = None) -> list[np.ndarray]:
        """
        从视频中采样固定数量的关键帧

        Args:
            video_file_path: 视频文件路径
            keyframe_count: 需要的关键帧数量
            frame_selector: 帧位选择器，决定第n个关键帧在视频的第几帧采样；若为None则自动平均间隔采样。

        Returns:
            list[Image.Image]: 采样到的关键帧图像RGB像素ndarray列表
        """
        cap = cv2.VideoCapture(video_file_path)
        if not cap.isOpened():
            raise ValueError("无法打开视频文件")

        total_frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        sampling_frames: list[int] = []
        if keyframe_selector is not None:
            sampling_frames = [
                keyframe_selector.get_frame_position(x, total_frame_count) for x in range(keyframe_count)
            ]
        else:
            interval = total_frame_count // keyframe_count
            for i in range(keyframe_count):
                sampling_frames.append(i * interval)
        sampled_frame_index = 0
        keyframes: list[np.ndarray] = []
        processed_frame_index = 0

        while len(keyframes) < keyframe_count:
            ret, frame = cap.read()

            if not ret:
                break

            if processed_frame_index == sampling_frames[sampled_frame_index]:
                print(f"采样第{sampled_frame_index}个关键帧(视频第{processed_frame_index}帧)")
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                keyframes.append(frame_rgb)
                sampled_frame_index += 1

            processed_frame_index += 1

        cap.release()

        return keyframes

    @staticmethod
    def sample_at_fixed_interval(video_file_path: str, interval: float) -> list[np.ndarray]:
        """
        从视频中按固定时间间隔采样关键帧

        Args:
            video_file_path: 视频文件路径
            interval: 采样间隔（秒）

        Returns:
            list[Image.Image]: 采样到的关键帧图像RGB像素ndarray列表
        """
        cap = cv2.VideoCapture(video_file_path)
        if not cap.isOpened():
            raise ValueError("无法打开视频文件")

        fps = cap.get(cv2.CAP_PROP_FPS)  #
        if fps == 0:
            cap.release()
            raise ValueError("无法获取视频帧率")

        frame_interval = int(interval * fps)
        if frame_interval <= 0:
            frame_interval = 1

        keyframes: list[np.ndarray] = []
        processed_frame_index = 0

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            if processed_frame_index % frame_interval == 0:
                print(f"采样第{len(keyframes) + 1}个关键帧(视频第{processed_frame_index}帧)")
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                keyframes.append(frame_rgb)

            processed_frame_index += 1

        cap.release()

        return keyframes
