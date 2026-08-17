import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def bar_chart(df: pd.DataFrame, group_col: str, value_col: str | None, title: str,
              top_n: int = None, aggfunc: str = "sum", pre_aggregated: bool = False):
    if pre_aggregated:
        data = df[[group_col, value_col]].copy()
    elif value_col is None:
        data = df.groupby(group_col).size().reset_index(name="value")
    elif aggfunc == "sum":
        data = df.groupby(group_col)[value_col].sum().reset_index(name=value_col)
    elif aggfunc == "mean":
        data = df.groupby(group_col)[value_col].mean().reset_index(name=value_col)
    elif aggfunc == "count":
        data = df.groupby(group_col)[value_col].count().reset_index(name=value_col)
    elif aggfunc == "nunique":
        data = df.groupby(group_col)[value_col].nunique().reset_index(name=value_col)
    else:
        data = df.groupby(group_col)[value_col].sum().reset_index(name=value_col)

    sort_col = "value" if (value_col is None and not pre_aggregated) else value_col
    data = data.sort_values(sort_col, ascending=False)
    if top_n:
        data = data.head(top_n)
    fig = px.bar(data, x=group_col, y=sort_col, title=title, text=sort_col)
    return fig


def horizontal_bar_chart(df: pd.DataFrame, group_col: str, value_col: str, title: str,
                          top_n: int = None, pre_aggregated: bool = False):
    """Horizontal bar chart for better readability with many categories"""
    if pre_aggregated:
        data = df[[group_col, value_col]].copy()
    else:
        data = df.groupby(group_col)[value_col].sum().reset_index(name=value_col)
    data = data.sort_values(value_col, ascending=True)
    if top_n:
        data = data.tail(top_n)
    fig = px.bar(data, y=group_col, x=value_col, title=title, orientation="h")
    return fig


def scatter_chart(df: pd.DataFrame, x_col: str, y_col: str, color_col: str | None, title: str):
    fig = px.scatter(df, x=x_col, y=y_col, color=color_col, title=title, hover_data=df.columns)
    return fig


def histogram(df: pd.DataFrame, column: str, title: str, color_col: str | None = None):
    fig = px.histogram(df, x=column, color=color_col, nbins=30, title=title, barmode="overlay")
    return fig


def pie_chart(df: pd.DataFrame, names_col: str, title: str, values_col: str | None = None):
    """Create a pie chart. If values_col is None, slice sizes are row counts per names_col."""
    if values_col is None:
        data = df.groupby(names_col).size().reset_index(name="count")
        fig = px.pie(data, values="count", names=names_col, title=title)
    else:
        data = df.groupby(names_col)[values_col].sum().reset_index()
        fig = px.pie(data, values=values_col, names=names_col, title=title)
    return fig


def box_plot(df: pd.DataFrame, y_col: str, x_col: str | None, title: str):
    """Create a box plot to show distribution"""
    fig = px.box(df, y=y_col, x=x_col, title=title)
    return fig


def heatmap(data: pd.DataFrame, title: str):
    """Create a heatmap from pivot/correlation data"""
    fig = go.Figure(data=go.Heatmap(
        z=data.values, x=data.columns, y=data.index,
        colorscale="RdBu", zmid=0,
    ))
    fig.update_layout(title=title)
    return fig
