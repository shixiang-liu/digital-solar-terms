# Data pipeline

The visualisation is the last step of this project, not the substance. The substance is turning multi-decade daily weather records into comparable solar-term windows across regions and years, so that a term in one city and a term forty years earlier can be put on the same axis.

## 1. Sources

Weather observations (below) are the project's own data work. Administrative boundary geometry used by the map comes from Alibaba DataV GeoAtlas (public boundary data, display only) and is inlined directly in `index.html`; it is not this project's own work.

| Region | Raw form | Files | Coverage |
|---|---|---|---|
| Ningxia (5 cities) | xlsx / tab-separated text | `宁夏历史数据.xlsx`, three per-window exports | 1980–2022 |
| Shandong | daily sunshine xlsx → per-city yearly CSV | 13 MB xlsx + 977-row CSV | 1960– |
| Xinjiang | daily sunshine xlsx → per-city yearly CSV | 21 MB xlsx + 1,465-row CSV | 1960– |
| Gansu | daily sunshine xlsx → per-city yearly CSV | 11.5 MB xlsx + 855-row CSV (not committed) | 1960– |

Daily records cannot be compared across years directly: the calendar date that "小暑" (Minor Heat) falls on moves every year. Everything downstream therefore depends on slicing the daily series by **solar-term window** first.

## 2. Solar-term windows

Three windows are used, each defined by its start and end term rather than by fixed dates:

| Window | Terms | Indicators extracted |
|---|---|---|
| Spring | 春分 → 清明 | temperature variation, precipitation |
| Summer | 立夏 → 小满 | average temperature, effective temperature |
| Autumn | 小暑 → 立秋 | sunshine hours, average temperature, precipitation |

The Ningxia per-window exports are marked **插补后** (after gap filling) — missing daily observations were interpolated before aggregation, because a missing week inside a 15-day window would otherwise dominate the average.

## 3. Aggregation output

The regional statistics files are long-format tables, one row per city-year:

```csv
地级市,年份,累计日照时数(小时)
乌鲁木齐市,1960,452.82
```

Samples of these outputs are committed as-is under `data/samples/` (Shandong 977 lines and Xinjiang 1,465 lines including the header; the Gansu export is not committed), which is also the schema the visualisation consumes after conversion to JSON.

## 4. Feature vector

Aggregation produces a seven-value vector per city-year, which is the interface between the data work and the modelling work:

```
spring_tempVar, spring_precip,
summer_avgTemp, summer_effTemp,
autumn_precip, autumn_avgTemp, autumn_sunshine
```

Effective temperature (`summer_effTemp`) is the accumulated thermal measure used in agricultural suitability work rather than a plain mean, which is why it is carried alongside `summer_avgTemp`.

## 5. Modelling (companion step)

`analysis/` holds the two modelling utilities from the same project:

- `climate_simulation_bootstrap.py` — extrapolates a 41-year annual series ten years forward with Prophet (seasonality disabled, annual data), then adds bootstrapped historical residuals so the projection carries the observed variance instead of a smooth trend line.
- `climate_to_quality_model.py` — a random-forest regressor mapping the seven-value climate vector to a quality label, with a fixed seed for reproducibility.

They are the climate→quality half of the pipeline and are shared with the companion agricultural climate-quality system; the quality label series itself is not part of this repository.
