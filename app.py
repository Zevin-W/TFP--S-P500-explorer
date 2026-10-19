import streamlit as st
import pandas as pd
from pathlib import Path
import altair as alt

st.title("TFP Growth and S&P 500 Returns")
st.write("Explore the relationship between U.S. private business productivity growth and stock-market returns, 1989–2025.")

#- import streamlit as st：导入 Streamlit，并简称为 st。后面通过它创建页面内容。
#- st.title(...)：在页面顶部显示主标题。
#- st.write(...)：在标题下显示一段说明，介绍研究内容和年份范围。
#- 中间的空行：方便阅读，不影响执行。

data_path = Path(__file__).parent / "tfp_sp500_annual.csv"
data = pd.read_csv(data_path)
st.dataframe(data)



year_range = st.sidebar.slider(
    "Select year range",
    min_value=int(data["Year"].min()),
    max_value=int(data["Year"].max()),
    value=(1989, 2025)
)

filtered_data = data[
    (data["Year"] >= year_range[0])
    & (data["Year"] <= year_range[1])
].copy()

#让页面显示当前选中了多少年的数据，方便用户知道自己正在看哪个范围。
#st.write(：在页面上显示文字。
st.write(
    f"Selected period: {year_range[0]}–{year_range[1]} | "
    f"Observations: {len(filtered_data)} years"
)

#先加“原始值／标准化”切换，完成后再加散点悬停显示年份。
view_mode = st.radio(
    "Choose time-series view",
    ["Original values", "Standardized comparison"],
    horizontal=True
)


st.dataframe(filtered_data)

if view_mode == "Original values":
    st.subheader("TFP Growth over Time")
    st.line_chart(filtered_data, x="Year", y="TFP_Growth_Pct")

    st.subheader("S&P 500 Annual Total Returns")
    st.line_chart(filtered_data, x="Year", y="SP500_Return_Pct")

else:
    standardized_data = filtered_data[["Year"]].copy()

    standardized_data["TFP Growth"] = (
        filtered_data["TFP_Growth_Pct"] - data["TFP_Growth_Pct"].mean()
    ) / data["TFP_Growth_Pct"].std()

    standardized_data["S&P 500 Return"] = (
        filtered_data["SP500_Return_Pct"] - data["SP500_Return_Pct"].mean()
    ) / data["SP500_Return_Pct"].std()

    st.subheader("Standardized Comparison")
    st.line_chart(
        standardized_data,
        x="Year",
        y=["TFP Growth", "S&P 500 Return"]
    )
    st.caption("Z-scores use the full 1989–2025 sample. Zero represents each series' full-sample mean.")

#st.subheader(...)：显示一个小标题“TFP 增长随时间的变化”。
#st.line_chart(：创建折线图。
#filtered_data,：使用筛选后的数据，因此图表会响应年份滑块。
#x="Year",：横轴使用年份列。
#y="TFP_Growth_Pct"：纵轴使用 TFP 增长率，数值单位为百分比。
#)：结束调用。


##可以。不过复制一个滑块后，还要让两个滑块保持同步，代码会稍复杂。
#更简单的做法是：把现有滑块移到侧边栏，页面向下滚动时也方便调整。
#只把原来的：year_range = st.slider(
#改为：year_range = st.sidebar.slider(

st.subheader("TFP Growth vs. S&P 500 Returns")

scatter = alt.Chart(filtered_data).mark_circle(size=80).encode(
    x=alt.X("TFP_Growth_Pct:Q", title="TFP Growth (%)"),
    y=alt.Y("SP500_Return_Pct:Q", title="S&P 500 Total Return (%)"),
    tooltip=[
        alt.Tooltip("Year:O", title="Year"),
        alt.Tooltip("TFP_Growth_Pct:Q", title="TFP Growth (%)", format=".2f"),
        alt.Tooltip("SP500_Return_Pct:Q", title="S&P 500 Return (%)", format=".2f")
    ]
)

st.altair_chart(scatter, use_container_width=True)

#显示所选年份的相关系数，让它随滑块一起更新。
if len(filtered_data) >= 3 and filtered_data["TFP_Growth_Pct"].nunique() > 1 and filtered_data["SP500_Return_Pct"].nunique() > 1:
    correlation = filtered_data["TFP_Growth_Pct"].corr(
        filtered_data["SP500_Return_Pct"]
    )
    st.metric("Pearson correlation", f"{correlation:.3f}")
else:
    st.info("Select at least 3 years with variation in both variables.")

#st.caption(：显示一段较小字号的说明文字。
st.caption(
    "Correlation ranges from -1 to 1 and describes the direction and strength "
    "of a linear relationship. It does not establish causation. "
    "Results may vary with the selected period and can be unstable for small samples."
)

#在页面末尾补充数据来源和范围，让用户知道这些数字来自哪里。
st.subheader("Data Sources and Scope")

st.write(
    "TFP: U.S. Bureau of Labor Statistics, private business sector, "
    "including farm and nonfarm private business. "
    "Values are annual percentage changes."
)

st.write(
    "S&P 500: Yahoo Finance historical data for the S&P 500 Total Return Index "
    "(^SP500TR), extracted from a saved PDF. "
    "Annual returns are calculated from consecutive year-end closing index values."
)

st.caption(
    "The merged dataset covers 1989–2025, with 37 annual observations. "
    "The 2025 TFP estimate is preliminary."
)

#补上项目的主要发现，并明确它针对完整样本
st.subheader("Key Finding: Full Sample (1989–2025)")

st.write(
    "Across 37 years, TFP growth and same-year S&P 500 total returns show "
    "a weak positive correlation (r = 0.273). "
    "The conventional Pearson test is not statistically significant "
    "at the 5% level (p = 0.102)."
)

st.caption(
    "This finding uses the full dataset and does not change with the year slider. "
    "The p-value relies on standard test assumptions; dependence across years "
    "has not been formally assessed."
)

st.subheader("Limitations")

st.write(
    "- Only 37 annual observations are available for 1989–2025.\n"
    "- Private business TFP and the S&P 500 cover different sets of businesses.\n"
    "- The analysis examines same-year associations, not causation or future prediction.\n"
    "- TFP estimates can be revised, and the analysis does not account for other economic factors."
)