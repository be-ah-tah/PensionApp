import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import textwrap

def pensionComponentsInStackedBarChart(df):
    fig = px.bar(df, x=df.index, y=["Interest", "Contributions", "Current Fund"])
    fig.update_layout(title = "Breakdown of your pension fund over time",width=500, height=400, legend = dict(orientation ='h', x=-0.1, y=-0.2),xaxis_title=None,
    yaxis_title=None)
    return fig
def pieChart(values):
    fig = go.Figure(data=[go.Pie(values=values, pull=[0, 0, 0.2, 0])], mode='markers', marker=dict(color=values, colorscale='viridis'))
    return fig
def targetCompletionPie(PV_pension, desirable_income):
    perc_pension_target = (PV_pension / 12) / desirable_income

    names = ['perc. of target', 'perc. missing of target']
    percentage = [perc_pension_target, 1 - min(1, perc_pension_target)]

    # pull is given as a fraction of the pie radius
    fig = go.Figure(data=[go.Pie(labels=names, values=percentage, textinfo=None, hole=.4, pull=[0.2, 0])])


    fig.update_layout(title={'text' : f'You are on track to achieve {perc_pension_target:.0%}<br>of your target pension income', 'x': 0.5, 'xanchor': 'center'},
        annotations=[dict(text=f'{perc_pension_target:.0%}', x=0.5, font_size=30, showarrow=False)], showlegend=False)
    fig.update_traces(textinfo='none')

    return fig

def totalFundTraceIndicator (fund_size, yearly_pension_fund):

    fig = go.Figure(go.Indicator(
        mode="number+delta",
        value=fund_size,
        delta={"valueformat": ",.0f"}
        ))

    fig.add_trace(go.Scatter(y=yearly_pension_fund))
    fig.update_layout(title = "Total Pension Fund", width=500, height=400)

    return fig

def compositionFinalPensionFunnel(names, values):

    fig = go.Figure(go.Funnelarea(
        text = names,
        values = values
        ))
    proportion = 1 if sum(values) == 0 else values[0] / sum(values)
    fig.update_layout(title={'text' : f'The largest component of your pension<br>at retirement is {names[0]} at {proportion:.1%}','x': 0.5, 'xanchor': 'center'},
                      showlegend=False)
    return fig

def changeInKeyIndicators (revised_figure, old_figure):
    fig = go.Figure(go.Indicator(
        mode="number+delta",
        value=revised_figure,
        number={'prefix': "£"},
        delta={'position': "top", 'prefix': "£",'reference': old_figure, 'font':{'size':40}}
        ))
    #fig.update_layout(height=150, width=250)

    return fig

def displayKeyIndicator(value):
    fig = go.Figure(go.Indicator(
        mode="number",
        value=value,
        number={'font_color':'blue','prefix': "£",'font':{'size':60}}))
    fig.update_layout(height=150, width=250)

    return fig



