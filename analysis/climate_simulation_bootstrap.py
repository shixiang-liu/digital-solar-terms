import pandas as pd
import numpy as np
from prophet import Prophet


def predict_climate_with_bootstrap(historical_data: list, prediction_years: int = 10) -> np.ndarray:
    """
    使用 Prophet 模型结合残差自助法来预测时间序列数据。

    参数:
    historical_data (list): 包含历史数据（1980-2020年，共41个点）的列表。
    prediction_years (int): 需要预测的未来年数。

    返回:
    numpy.ndarray: 包含10年预测值的数组。
    """

    # 1. 准备数据：将列表转换为 Prophet 需要的 DataFrame 格式
    # 创建从1980年到2020年的年份日期
    history_dates = pd.to_datetime(pd.date_range(start='1980-01-01', periods=len(historical_data), freq='Y'))
    history_df = pd.DataFrame({'ds': history_dates, 'y': historical_data})

    # 2. 拟合模型：使用 Prophet 学习历史数据的趋势
    # 关闭了季节性，因为我们处理的是年度数据，主要关心长期趋势
    model = Prophet(yearly_seasonality=False, weekly_seasonality=False, daily_seasonality=False)
    model.fit(history_df)

    # 3. 提取残差：计算模型预测与真实历史数据之间的“真实噪音”
    # 'yhat' 是模型对历史数据的拟合/预测值
    historical_forecast = model.predict(history_df)
    residuals = history_df['y'] - historical_forecast['yhat']

    # 4. 预测未来趋势：让模型预测未来10年的平滑趋势
    future_dates = model.make_future_dataframe(periods=prediction_years, freq='Y')
    future_forecast = model.predict(future_dates)

    # 只取出未来10年的趋势预测值
    future_trend = future_forecast['yhat'][-prediction_years:].values

    # 5. 残差自助法 (Bootstrap)：从历史噪音中随机抽样，并添加到未来趋势上
    # 'with replacement=True' 意味着同一个历史噪音可以被多次抽中
    sampled_residuals = np.random.choice(residuals, size=prediction_years, replace=True)

    # 最终的预测 = 未来趋势 + 随机抽取的历史噪音
    final_forecast = future_trend + sampled_residuals

    # 6. 后处理：确保降水量等指标不会出现负数
    final_forecast[final_forecast < 0] = 0

    return final_forecast


# --- 示例如何使用 ---
# 假设这是“酒泉市”1980-2020年的春季温度变化数据
sample_climate_data = [5.31, 3.08, 3.67, 4.7, 4.42, 4.88, 3.83, 5.02, 4.22, 2.82, 3.89, 4.1, 5.0, 3.69, 4.34, 2.91,
                       4.92, 3.6, 6.18, 5.96, 3.67, 4.91, 4.65, 3.82, 4.61, 3.56, 4.48, 4.11, 4.49, 4.6, 5.48, 6.66,
                       4.05, 4.48, 2.81, 3.63, 2.82, 3.63, 4.53, 5.38, 4.39]

# 生成2021-2030年的预测
predicted_values = predict_climate_with_bootstrap(sample_climate_data)

print("算法一：气候数据预测结果 (示例)")
print(np.round(predicted_values, 2))