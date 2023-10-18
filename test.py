import altair as alt
from vega_datasets import data

source = data.iowa_electricity()

print(source)

charts = alt.Chart(source).mark_area().encode(
    x="year:T",
    y="net_generation:Q",
    color="source:N"
)
# save to data/debug.svg
charts.save('debug.svg')

import altair as alt
from vega_datasets import data

source = data.stocks()
print(source)

charts = alt.Chart(source).mark_line().encode(
    x='date:T',
    y='price:Q',
    color='symbol:N',
)

# save to data/debug.svg
charts.save('debug.svg')
