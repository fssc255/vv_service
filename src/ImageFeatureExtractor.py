from torchvision.models import ResNet18_Weights
import torchvision.transforms as transforms
import torchvision.models as models
import torch
import numpy as np


class ImageFeatureExtractor:
    def __init__(self) -> None:
        model = models.resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)

        self.__feature_extractor = torch.nn.Sequential(*list(model.children())[:-1])
        self.__feature_extractor.eval()
        for param in self.__feature_extractor.parameters():
            param.requires_grad = False

        self.__image_transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

    def get_feature_vector(self, image: np.ndarray) -> np.ndarray | None:
        """
        将RGB像素转换为特征向量

        参数:
            image: ndarray形式的RGB图像
        返回:
            图像的特征向量，失败则返回None
        """
        try:
            # 在第0维增加一个批次维度（模型要求输入形状为[batch_size, C, H, W]）
            img_tensor = self.__image_transform(image).unsqueeze(0)  # type:ignore

            with torch.no_grad():
                # 输入预处理后的张量，得到特征输出（形状为[1, 512, 1, 1]）
                vector = self.__feature_extractor(img_tensor).squeeze().numpy()

            return vector
        except Exception as e:
            return None
