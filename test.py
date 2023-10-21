import altair as alt
from vega_datasets import data

source = data.cars()

chart = alt.Chart(source).mark_circle(size=60, clip=False).transform_calculate(
    x = alt.datum.Horsepower-100,
    y = alt.datum.Miles_per_Gallon - 25
).encode(
    x=alt.X('x:Q', axis=alt.Axis(offset=-150)),
    y=alt.Y('y:Q', axis=alt.Axis(offset=-190)),
    color='Origin',
).configure_axisX(
    domainWidth =3
).configure_axisY(
    domainWidth =3
)
# save
chart.save('debug.svg')
