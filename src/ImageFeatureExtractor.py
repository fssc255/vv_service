import torch
import numpy as np
import open_clip
from PIL import Image
from utils.Logger import Logger


class ImageFeatureExtractor:
    """使用OpenCLIP模型提取图像特征"""
    
    def __init__(self, model_name: str = "ViT-B-32", pretrained: str = "laion2b_s34b_b79k") -> None:
        """
        初始化OpenCLIP模型
        
        Args:
            model_name: 模型名称，默认使用EVA02-E-14-plus
            pretrained: 预训练权重
        """
        try:
            Logger.info(f"正在加载OpenCLIP模型: {model_name}")
            
            # 检测设备
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            Logger.info(f"使用设备: {self.device}")
            
            # 加载模型和预处理器
            model_result = open_clip.create_model_and_transforms(
                model_name,
                pretrained=pretrained,
                device=self.device
            )
            self.__model = model_result[0]
            self.__preprocess = model_result[2]
            
            # 设置为评估模式
            self.__model.eval()
            
            # GPU模式下启用半精度以减少显存占用
            if self.device == "cuda":
                self.__model.half()
            
            Logger.info(f"OpenCLIP模型加载成功")
            
        except Exception as e:
            Logger.error(f"加载OpenCLIP模型失败: {e}")
            raise

    def get_feature_vector(self, image: np.ndarray) -> np.ndarray:
        """
        将RGB像素转换为特征向量

        参数:
            image: ndarray形式的RGB图像
        返回:
            图像的特征向量 (1024维)
        """
        try:
            # 转换为PIL Image
            if isinstance(image, np.ndarray):
                pil_image = Image.fromarray(image.astype('uint8'), 'RGB')
            else:
                pil_image = image
            
            # 预处理
            image_tensor = self.__preprocess(pil_image).unsqueeze(0).to(self.device)
            if self.device == "cuda":
                image_tensor = image_tensor.half()
            
            # 提取特征向量
            with torch.no_grad():
                vector = self.__model.encode_image(image_tensor)
                # 归一化
                vector = vector / vector.norm(dim=-1, keepdim=True)
                vector = vector.cpu().numpy()[0]
            
            return vector
            
        except Exception as e:
            Logger.error(f"提取图像特征失败: {e}")
            raise
