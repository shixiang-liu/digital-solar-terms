import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor


def predict_quality_with_random_forest(climate_train: pd.DataFrame,
                                       quality_train: pd.Series,
                                       climate_future: pd.DataFrame) -> np.ndarray:
    """
    使用随机森林回归模型，根据气候数据预测葡萄品质。

    参数:
    climate_train (pd.DataFrame): 用于训练的历史气候数据 (行: 年份, 列: 气候指标)。
    quality_train (pd.Series): 用于训练的历史葡萄品质数据。
    climate_future (pd.DataFrame): 用于预测的未来气候数据。

    返回:
    numpy.ndarray: 包含未来品质预测值的数组。
    """

    # 1. 初始化模型
    # n_estimators=100 表示我们建立100棵决策树来共同决策，结果更稳定
    # random_state=42 确保每次运行代码时，随机过程都一样，保证结果可复现
    model = RandomForestRegressor(n_estimators=100, random_state=42)

    # 2. 训练模型：让模型学习历史气候和品质之间的关系
    model.fit(climate_train, quality_train)

    # 3. 进行预测：将未来的气候数据输入训练好的模型，得到品质预测
    predicted_quality = model.predict(climate_future)

    return predicted_quality


# --- 示例如何使用 ---
# 假设这是某个城市1980-2020年的数据 (41年)
# 在实际使用中，需要用我们第一步生成的真实气候数据来填充
climate_feature_names = ['spring_tempVar', 'spring_precip', 'summer_avgTemp', 'summer_effTemp', 'autumn_precip',
                         'autumn_avgTemp', 'autumn_sunshine']
X_train_climate = pd.DataFrame(np.random.rand(41, 7), columns=climate_feature_names)  # 41年的历史气候数据
y_train_quality = pd.Series(np.random.rand(41) * 2 + 0.5)  # 41年的历史品质数据

# 假设这是我们用算法一预测出的2021-2030年的气候数据 (10年)
X_future_climate = pd.DataFrame(np.random.rand(10, 7), columns=climate_feature_names)

# 预测未来10年的品质
predicted_quality_values = predict_quality_with_random_forest(X_train_climate, y_train_quality, X_future_climate)

print("\n算法二：葡萄品质预测结果 (示例)")
print(np.round(predicted_quality_values, 2))