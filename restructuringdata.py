import marimo

__generated_with = "0.14.13"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import altair as alt
    import pandas as pd
    import numpy as np
    import os
    import ast
    import re
    return alt, ast, mo, pd, re

##TESTING
@app.cell
def _(mo):
    mo.center(mo.md('# Data Viz Explorer'))
    return


@app.cell
def _():
    return


@app.cell
def _(mo):
    mo.center(mo.md('Contactinfo@gmail.com'))
    return


@app.cell
def _(mo):
    mo.center(mo.md('[Stanford University Cognitive Tools Lab](https://cogtoolslab.github.io/about.html)'))
    return


@app.cell
def _(mo):
    mo.md("""## insert various introductions here?""")
    return


@app.cell
def _(mo):
    mo.md("""This is a collection of data visualization literacy assessments. Definition of dvl? Features of the dashboard: filters, quick stats, graphs. Contact information for cogtools?""")
    return


@app.cell
def _():
    ###This next section will not show on ui. It loads in and restructures the csv. 
    return


@app.cell
def _(mo, pd):
    notebook_path = mo.notebook_location()
    data_dir = f'{notebook_path}/public'
    files = ['ARTIST.csv', 'NAAL.csv', 'merk2020.csv', 'rodrigues2024.csv']
    dataframes = []

    for csv_file in files:
        table_name = csv_file.rsplit(".", 1)[0]
        print(f"Loading {csv_file} as '{table_name}'")

        path = f'{data_dir}/{csv_file}'
        df = pd.read_csv(path)
        dataframes.append(df)
    return (dataframes,)


@app.cell
def _(dataframes, pd):
    concat_dfs = pd.concat(dataframes, ignore_index=True)
    return (concat_dfs,)


@app.cell
def _():
    return


@app.cell
def _(concat_dfs):
    max_len = 0

    for answers in concat_dfs['answer_choices']:
        if answers != 'open-answer':
            parsed = eval(answers)
            if len(parsed) > max_len:
                max_len = len(parsed)
    return (max_len,)


@app.cell
def _(ast, concat_dfs, max_len):
    def expand_answers(row):
        answers = row['answer_choices']
        if answers != 'open-answer':
            parsed = ast.literal_eval(answers)
            for i in range(max_len):
                if i < len(parsed):
                    row[f'answer_{i+1}'] = parsed[i]
        else:
            row['open_answer'] = 'open-answer'
        return row
    concat_dfs_expanded = concat_dfs.apply(expand_answers, axis = 1)

    return (concat_dfs_expanded,)


@app.cell
def _(concat_dfs_expanded):
    def open_ans(row):
        ans = row['open_answer']
        if ans != 'open-answer':
            row['open_answer'] = 'multiple-choice'
        return row

    concat_dfs_expanded_clean = concat_dfs_expanded.apply(open_ans, axis = 1)
    return (concat_dfs_expanded_clean,)


@app.cell
def _():
    return


@app.cell
def _(concat_dfs_expanded_clean, re):
    static_columns = ['test_name', 'item_ids', 'graph_types', 'graph_types_ctl', 'graph_url', 'question_stems', 'open_answer']
    flexible_columns = []
    for column in concat_dfs_expanded_clean.columns:
        if re.search(r'^answer_\d+$', column):
            flexible_columns.append(column)
    all_columns = static_columns + flexible_columns
    concat_dfs_complete = concat_dfs_expanded_clean[all_columns]
    return (concat_dfs_complete,)


@app.cell
def _():

    ##Display restructured csv
    return


@app.cell
def _(mo):
    mo.center(mo.md('## DATAFRAME'))
    return


@app.cell
def _(
    graph_select,
    mo,
    no_tests,
    open_prop,
    test_select,
    total_items,
    unique_graphs,
):
    mo.hstack(
        [mo.vstack(
                [mo.md('### Data Filters'), test_select, graph_select]
            ),
            mo.hstack(
                [
                    total_items,
                    no_tests,
                    unique_graphs,
                    open_prop
                ], justify = 'center', align = 'end'
            ),
        ]
    )
    return


@app.cell
def _(concat_dfs_complete, mo):
    ##buttons
    total_items = mo.stat(
        label="Total items",
        bordered=True,
        value=f"{len(concat_dfs_complete):,.0f}",
    )
    no_tests = mo.stat(
        label="Total assessments",
        bordered=True,
        value=f"{len(concat_dfs_complete['test_name'].unique()):,.0f}",
    )
    unique_graphs = mo.stat(
        label="Unique graphs",
        bordered=True,
        value=f"{len(concat_dfs_complete['graph_types_ctl'].unique()):,.0f}",
    )
    open_prop = mo.stat(label = "Proportion open-answer", 
                        bordered = True,
                        value = f"{(sum(concat_dfs_complete['open_answer'] == 'open-answer')/len(concat_dfs_complete))*100:,.0f}%")
    return no_tests, open_prop, total_items, unique_graphs


@app.cell
def _(concat_dfs_complete, mo):
    ##filters
    default_tests = list(concat_dfs_complete['test_name'].unique())
    default_graphs= list(concat_dfs_complete['graph_types_ctl'].unique())
    test_select = mo.ui.multiselect(options=concat_dfs_complete['test_name'].unique(),
                                   label = 'Filter tests:',
                                    value = default_tests
                                   )
    graph_select = mo.ui.multiselect(options=concat_dfs_complete['graph_types_ctl'].unique(),
                                    label = 'Filter graphs:',
                                    value = default_graphs)
    ##Another one here?
    return graph_select, test_select


@app.cell
def _():
    return


@app.cell
def _(concat_dfs_complete, graph_select, test_select):
    filtered_df1 = concat_dfs_complete[concat_dfs_complete['test_name'].isin(test_select.value)]
    filtered_df2 = filtered_df1[filtered_df1['graph_types_ctl'].isin(graph_select.value)]
    return (filtered_df2,)


@app.cell
def _(filtered_df2, mo):
    mo.ui.table(filtered_df2, selection=None)
    return


@app.cell
def _():
    ##Visualize the data
    return


@app.cell
def _(alt, chosen_title, chosen_x, encodings, filtered_df2, mo):
    _bar_chart = (
        alt.Chart(filtered_df2)
        .mark_bar(color="#2B2083")
        .encode(**encodings)
    )
    bar_chart = mo.ui.altair_chart(_bar_chart)

    _pie_chart = (
        alt.Chart(filtered_df2).mark_arc().encode(
        theta="count()",
        color=alt.Color(field=chosen_x, type="nominal", title = chosen_title, scale=alt.Scale(scheme="category20"))
        )
    )
    bar_chart = mo.ui.altair_chart(_bar_chart)
    pie_chart = mo.ui.altair_chart(_pie_chart)
    return bar_chart, pie_chart


@app.cell
def _(mo):
    xaxis = mo.ui.dropdown(options=["Graph type", "Assessment"], label="X-axis", value = 'Graph type')
    color = mo.ui.dropdown(options=["open-answer", 'None'], label="Encoding", value = 'None')
    return color, xaxis


@app.cell
def _(color, graph_select, mo, test_select, xaxis):
    mo.hstack([mo.hstack(
                [test_select, graph_select], justify = 'start'
            ), mo.hstack(
        [xaxis, color], justify = 'end', align = 'end')
              ]
               )
    return


@app.cell
def _():
    return


@app.cell
def _(alt, color, xaxis):
    if xaxis.value == 'Graph type':
        chosen_x = 'graph_types_ctl'
        chosen_title = 'Graph type'
    if xaxis.value == 'Assessment':
        chosen_x = 'test_name'
        chosen_title = 'Assessment name' 
    encodings = {
        "x": alt.X(chosen_x, sort="-y", title=chosen_title),
        "y": alt.Y("count()", title="Count"),
        "tooltip": ["count()"]
    }
    if color.value == "open-answer":
        encodings["color"] = alt.Color(
            field="open_answer",
            type="nominal",
            title=chosen_title,
            scale=alt.Scale(scheme="paired")
        )
    return chosen_title, chosen_x, encodings


@app.cell
def _(bar_chart):
    bar_chart
    return


@app.cell
def _(pie_chart):
    pie_chart
    return


@app.cell
def _(mo):
    mo.md("""### Data dictionary:""")
    return


@app.cell
def _(mo):
    mo.md("""<i> test_name</i>. The name of the assessment. Current assessments in dataframe: ARTIST, merk2020, rodrigues2024, NAAL""")
    return


@app.cell
def _(mo):
    mo.md("""<i> item_ids</i>. Item number. Format: test_number, where 'number' is the item's placement in the test. You can use this column to cross-reference items with other material.""")
    return


@app.cell
def _(mo):
    mo.md("""<i> graph_type </i>. The assessment's labels used for the item's visualization as understood from the assessment material. If no labels are given in the material, the value of this column is None.""")
    return


@app.cell
def _(mo):
    mo.md("""<i> graph_types_ctl </i>. Our categorization of the item's visualization as understood from viewing the assessment material. This may or may not align with the assessment maker's understanding of the item.""")
    return


@app.cell
def _(mo):
    mo.md("""<i> graph_url </i>. A link to the visualization used in the item, to be displayed in the table itself""")
    return


@app.cell
def _(mo):
    mo.md("""<i> question_stems</i>. The question used in the visualization. E.g., 'how many people caught a cold in August, 2019?' or 'Draw a histogram that matches this data.'""")
    return


@app.cell
def _(mo):
    mo.md("""<i> open_answer </i>. An indicator variable for non-multiple-choice questions (a.k.a, free-response, numerical, or""")
    return


@app.cell
def _(mo):
    mo.md("""<i> answer_# </i>. The multiple choice answer for the item's question, if it applies.""")
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
