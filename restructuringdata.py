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
    return alt, ast, mo, np, pd, re


@app.cell
def _(mo):
    mo.center(mo.md('# Data Viz Explorer'))
    return


@app.cell
def _():
    return


@app.cell
def _(mo):
    mo.center(mo.md('arnavv@stanford.edu, kushinm@stanford.edu, averyyue@stanford.edu'))
    return


@app.cell
def _(mo):
    mo.center(mo.md('[Stanford University Cognitive Tools Lab](https://cogtoolslab.github.io/about.html)'))
    return


@app.cell
def _(mo):
    mo.md("""## Introduction to the dashboard""")
    return


@app.cell
def _(mo):
    mo.md("""The Data Vis Explorer presents a collection of data visualization literacy assessments. In an age teeming with information, methods to quickly and concisely communicate quantitative data through data visualizations have become increasingly prevalent and important in everyday life. A person's ability to correctly translate these visualizations into the underlying information is data visualization literacy, which can determine successful interpretation of anything from medical charts (Galesic & Garcia-Retamero, 2010) to SAT questions.""")
    return


@app.cell
def _(mo):
    mo.md("Over the past decades, researchers have developed a number of assessments to measure a person's data visualization literacy, targeting a wide range of cognitive tasks, contexts, and audiences. However, these assessments are largely created independently, and items from individual tests have only recently started to be compared for similarities. What skills are important to data visualization literacy? What attributes a 'difficult' item from an 'easy' item?")
    return


@app.cell
def _(mo):
    mo.md("This dashboard is meant to enable easier comparison of items between assessments. Each item typically consists of a visualization, a question stem, and if multiple-choice, a series of answer choices. The Data Vis Explorer has collected items from nine assessments that have made their items publicly available into one filterable dataframe. Features include the dataframe itself, descriptive statistics, and the option to visualize the filtered dataframe with a contingency table. A data dictionary is available at the end of the dashboard.")
    return


@app.cell
def _():
    ###This next section will not show on ui. It loads in and restructures the csv. 
    return


@app.cell
def _(mo, pd):
    data_dir = "https://raw.githubusercontent.com/data-vis-assessments/data-vis-items.github.io/refs/heads/main/public/"
    files = ['ARTIST.csv', 'NAAL.csv', 'merk2020.csv', 'rodrigues2024.csv']
    dataframes = []

    for csv_file in files:
        table_name = csv_file.rsplit(".", 1)[0]
        print(f"Loading {csv_file} as '{table_name}'")

        path = data_dir + csv_file
        df = pd.read_csv(path)
        dataframes.append(df)
    return data_dir, dataframes


@app.cell
def _():
    return


@app.cell
def _(dataframes, pd):
    concat_dfs = pd.concat(dataframes, ignore_index=True).rename(columns={'question_stems':'question'})
    return (concat_dfs,)


@app.cell
def _():
    return


@app.cell
def _():
    return


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
def _():
    return


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
    static_columns = ['test_name', 'item_ids', 'graph_types', 'graph_types_ctl', 'task_types', 'task_types_ctl', 'graph_url', 'question', 'open_answer']
    flexible_columns = []
    for column in concat_dfs_expanded_clean.columns:
        if re.search(r'^answer_\d+$', column):
            flexible_columns.append(column)
    all_columns = static_columns + flexible_columns
    concat_dfs_new = concat_dfs_expanded_clean[all_columns]
    return (concat_dfs_new,)


@app.cell
def _(concat_dfs_new, data_dir, pd):
    remaining_files = ['CALVI.csv', 'GGR.csv', 'VLAT.csv', 'WAN.csv', 'BRBF.csv']
    remaining_dataframes = [concat_dfs_new]

    for file in remaining_files:
        name = file.rsplit(".", 1)[0]
        print(f"Loading {file} as '{name}'")

        rem_path = data_dir + file
        rem_df = pd.read_csv(rem_path)
        rem_df = rem_df.drop('Unnamed: 0', axis=1)
        remaining_dataframes.append(rem_df)
    return (remaining_dataframes,)


@app.cell
def _(np, pd, remaining_dataframes):
    def standardize_answer_columns(df):
        df_copy = df.copy()
    
        for i in range(1, 16):
            col_name = f'answer_{i}'
            if col_name not in df_copy.columns:
                df_copy[col_name] = np.nan
    
        return df_copy

    standardized_dfs = [standardize_answer_columns(df) for df in remaining_dataframes]

    concat_dfs_complete = pd.concat(standardized_dfs, ignore_index=True)
    return (concat_dfs_complete,)


@app.cell
def _(concat_dfs_complete, pd):
    #cleaning
    def standardize_format(value):
        if pd.isna(value):
            return value
        value = str(value).lower()
        if value == '100 % stacked bar chart':
            value = '100% stacked bar chart'
        return value

    concat_dfs_complete['graph_types_ctl'] = concat_dfs_complete['graph_types_ctl'].apply(standardize_format)
    
    return


@app.cell
def _():
    return


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
    unique_tasks,
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
                    unique_tasks,
                    open_prop
                ], justify = 'center', align = 'end'
            ),
        ]
    )
    return


@app.cell
def _(filtered_df2, mo):
    ##buttons
    total_items = mo.stat(
        label="Total items",
        bordered=True,
        value=f"{len(filtered_df2):,.0f}",
    )
    no_tests = mo.stat(
        label="Total assessments",
        bordered=True,
        value=f"{len(filtered_df2['test_name'].unique()):,.0f}",
    )
    unique_graphs = mo.stat(
        label="Unique graphs",
        bordered=True,
        value=f"{len(filtered_df2['graph_types_ctl'].unique()):,.0f}",
    )
    unique_tasks = mo.stat(
        label="Unique tasks",
        bordered=True,
        value=f"{len(filtered_df2['task_types_ctl'].unique()):,.0f}",
    )
    open_prop = mo.stat(label = "Proportion open-answer", 
                        bordered = True,
                        value = f"{(sum(filtered_df2['open_answer'] == 'open-answer')/len(filtered_df2))*100:,.0f}%")
    return no_tests, open_prop, total_items, unique_graphs, unique_tasks


@app.cell
def _(concat_dfs_complete, mo):
    ##filters
    default_tests = list(concat_dfs_complete['test_name'].unique())
    default_graphs= list(concat_dfs_complete['graph_types_ctl'].unique())
    default_tasks= list(concat_dfs_complete['task_types'].unique())
    test_select = mo.ui.multiselect(options=concat_dfs_complete['test_name'].unique(),
                                   label = 'Filter tests:',
                                    value = default_tests
                                   )
    graph_select = mo.ui.multiselect(options=concat_dfs_complete['graph_types_ctl'].unique(),
                                    label = 'Filter graphs:',
                                    value = default_graphs)
    task_select = mo.ui.multiselect(options=concat_dfs_complete['task_types'].unique(),
                                    label = 'Filter tasks (og):',
                                    value = default_tasks)
    ##Another one here?
    return graph_select, test_select


@app.cell
def _():
    return


@app.cell
def _(concat_dfs_complete, graph_select, test_select):
    filtered_df1 = concat_dfs_complete[concat_dfs_complete['test_name'].isin(test_select.value)]
    filtered_df2 = filtered_df1[filtered_df1['graph_types_ctl'].isin(graph_select.value)]
    start = ['item_ids', 'graph_url', 'open_answer', 'question']
    for i in range(1, 15):
        if not filtered_df2[f'answer_{i}'].isna().all():
            start.append(f'answer_{i}')
    gen = ['task_types_ctl', 'graph_types_ctl', 'task_types', 'graph_types']
    display = filtered_df2[start + gen]
    return display, filtered_df2


@app.cell
def _(display, mo):
    mo.ui.table(display, selection=None)
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
    xaxis = mo.ui.dropdown(options=["Graph type", 'Task type', "Assessment"], label="X-axis", value = 'Graph type')
    color = mo.ui.dropdown(options=["open-answer", 'Graph type', 'Task type', 'None'], label="Encoding", value = 'None')
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
    if xaxis.value == 'Task type':
        chosen_x = 'task_types'
        chosen_title = 'Task type'

    tooltip_list = []
    tooltip_list.append(alt.Tooltip(chosen_x, title=chosen_title))
    if color.value != 'None':
        color_field_map = {
            "open-answer": ("open_answer", "Open Answer"),
            "Graph type": ("graph_types_ctl", "Graph Type"), 
            "Task type": ("task_types", "Task Type")
        }

        color_field, color_display_title = color_field_map[color.value]

        tooltip_list.append(alt.Tooltip(color_field, title=color_display_title))

        # Add descriptive count for the specific segment
        tooltip_list.append(alt.Tooltip("count()", title=f"Count"))
    else:
        # If no color encoding, just show basic count
        tooltip_list.append(alt.Tooltip("count()", title="Count"))

    encodings = {
        "x": alt.X(chosen_x, sort="-y", title=chosen_title, axis = alt.Axis(labelAngle=-45)),
        "y": alt.Y("count()", title="Count"),
        "tooltip": tooltip_list
    }

    if color.value == "open-answer":
        enc_data = "open_answer"
        encodings["color"] = alt.Color(
            field=enc_data,
            type="nominal",
            title=chosen_title,
            scale=alt.Scale(scheme="paired")
        )
    if color.value == "Graph type":
        enc_data = "graph_types_ctl"
        encodings["color"] = alt.Color(
            field=enc_data,
            type="nominal",
            title=chosen_title,
            scale=alt.Scale(scheme="paired")
        )
    if color.value == "Task type":
        enc_data = "task_types_ctl"
        encodings["color"] = alt.Color(
            field=enc_data,
            type="nominal",
            title=chosen_title,
            scale=alt.Scale(scheme="paired")
        )
    else:
        enc_data = ' '
    return chosen_title, chosen_x, enc_data, encodings


@app.cell
def _(bar_chart, display_type, pie_chart):
    if display_type.value == 'Bar chart':
        display_chart = bar_chart
    else:
        display_chart = pie_chart
    display_chart
    return


@app.cell
def _():
    ##Descriptive stats

    return


@app.cell
def _(mo):
    display_type = mo.ui.dropdown(options=["Bar chart", 'Pie chart'], label="Type of display", value = 'Bar chart')
    show_table = mo.ui.dropdown(options=['True', 'False'], label="Show contingency table?", value = 'False')
    mo.hstack([display_type, show_table], justify = 'center', gap = 3)
    return display_type, show_table


@app.cell
def _(chosen_x, color, enc_data, filtered_df2, pd, show_table):
    if show_table.value == 'True' and color.value != 'None':
        showing = pd.crosstab(filtered_df2[chosen_x], filtered_df2[enc_data])
    elif show_table.value == 'True' and color.value == 'None':
        showing = filtered_df2[chosen_x].value_counts()
    elif show_table.value == 'False':
        showing = None
    showing
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _(mo):
    mo.center(mo.md("""### Data dictionary"""))
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
    mo.md("""<i> task_types </i>. The assessment's labels used for the item's cognitive task as understood from the assessment material. If no labels are given in the material, the value of this column is None.""")
    return


@app.cell
def _(mo):
    mo.md("""<i> graph_types_ctl </i>. Our categorization of the item's cognitive task as understood from viewing the assessment material and matching items with the task coding schema presented in the assessment paper. This may or may not align with the assessment maker's understanding of the item. (i.e. the authors intended an item as "Identify averages", but as this was not in the assessment material, we coded the item as "Identify trends.")""")
    return


@app.cell
def _(mo):
    mo.md("""<i> graph_url </i>. A link to the visualization used in the item, to be displayed in the table itself""")
    return


@app.cell
def _(mo):
    mo.md("""<i> question</i>. The question used in the visualization. E.g., 'how many people caught a cold in August, 2019?' or 'Draw a histogram that matches this data.'""")
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
