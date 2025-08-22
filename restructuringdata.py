import marimo

__generated_with = "0.14.13"
app = marimo.App(width="medium")

##Importing packages
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

#Title
@app.cell
def _(mo):
    mo.center(mo.md('# Data Viz Explorer'))
    return


@app.cell
def _():
    return

##Contact info
@app.cell
def _(mo):
    mo.center(mo.md('arnavv@stanford.edu, kushinm@stanford.edu, averyyue@stanford.edu'))
    return


@app.cell
def _(mo):
    mo.center(mo.md('[Stanford University Cognitive Tools Lab](https://cogtoolslab.github.io/about.html)'))
    return

##Intro
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
    mo.md("This dashboard is meant to enable easier comparison of items between assessments. Each item typically consists of a visualization, a question stem, and if multiple-choice, a series of answer choices. The Data Vis Explorer has collected items from ten assessments that have made their items publicly available into one filterable dataframe. These assessments are <b> CALVI, WAN, BRBF, GGR, VLAT, HOLF, merk2020, rodrigues2024, ARTIST, and the NAAL.</b>")
    return


@app.cell
def _(mo):
    mo.md("Features include the dataframe itself, descriptive statistics, and the option to visualize the filtered dataframe with a contingency table. A data dictionary is available at the end of the dashboard.")
    return


@app.cell
def _():
    ###This next section will not show on ui. It loads in and restructures the csv. 
    return

##Load in new assessments
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
                    row[f'answer_choice_{i+1}'] = parsed[i]
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
    static_columns = ['test_name', 'item_ids', 'graph_types', 'graph_types_ctl', 'task_types', 'task_types_ctl', 
                      'graph_url', 'question', 'open_answer', 'prop_correct']
    flexible_columns = []
    for column in concat_dfs_expanded_clean.columns:
        if re.search(r'^answer_\d+$', column):
            flexible_columns.append(column)
    all_columns = static_columns + flexible_columns
    concat_dfs_new = concat_dfs_expanded_clean[all_columns]
    concat_dfs_new
    return (concat_dfs_new,)


@app.cell
def _(concat_dfs_new, data_dir, pd):
    remaining_files = ['CALVI.csv', 'GGR.csv', 'VLAT.csv', 'WAN.csv', 'BRBF.csv', 'HOLF.csv']
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

    concat_dfs_completed = pd.concat(standardized_dfs, ignore_index=True)
    return (concat_dfs_completed,)


@app.cell
def _(concat_dfs_completed, pd):
    #cleaning
    def standardize_format(value):
        if pd.isna(value):
            return value
        value = str(value).lower()
        if value == '100 % stacked bar chart':
            value = '100% stacked bar chart'
        return value
        
    concat_dfs_standardized = concat_dfs_completed.copy()
    concat_dfs_standardized['graph_types_ctl'] = concat_dfs_completed['graph_types_ctl'].apply(standardize_format)

    return


@app.cell
def _(concat_dfs_completed):
    find_value = ['literacy', 'Suitable', 'Find Extremum', 'retrieve_value', 'Retrieve Value', 'max', 'min', 'level_1',
             'find_extremum', 'find_clusters', 'intermediate', 'Understand & use data displays & representations', 'elementary', 'intersection', 'TextSearchExposition', 'Text Search', 'find_anomolies', 'Application, TextSearchExposition, ', 'Text SearchExposition, ']
    interpret_data = ['reasoning', 'Use statistics', 'Unsuitable', 'trend', 'Understand how to interpret data', 
                      'Understand data properties', 'Conceptual', 'find_correlations_trends',
                 'Find Correlations/Trends', 'Make Predictions', 'Application, Text Search']
    calculate_statistic = ['Aggregate data', 'Aggregate Values', 'Manipulate data', 'average', 'Computation, Text Search', 'trendComp',
                          'determine_Range', 'determine_range']
    compare_groups = ['make_comparisons', 'comprehensive', 'Understand statistics & psychometrics', 'Summarize & explain data', 'level_2', 'characterize_distribution', 'Make Comparisons', 'level_3']
    
    def combine_tasks(row):
        task = row['task_types_ctl']
        if task in find_value:
            row['task_types_comb'] = 'find_value'
        elif task in interpret_data:
            row['task_types_comb'] = 'interpret_data'
        elif task in calculate_statistic:
            row['task_types_comb'] = 'calculate_statistic'
        elif task in compare_groups:
            row['task_types_comb'] = 'compare_groups'
        else:
            print(row['question'])
            print(task)
        return row
    concat_dfs_complete=concat_dfs_standardized.apply(combine_tasks, axis = 1)
    return (concat_dfs_complete,)


@app.cell
def _():
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
    mo,
    no_tests,
    open_prop,
    total_items,
    unique_graphs,
    unique_images,
    unique_questions,
    unique_tasks_og,
):
    mo.hstack(
                [
                    total_items,
                    no_tests,
                    unique_graphs,
                    unique_tasks_og,
                    unique_images,
                    unique_questions,
                    open_prop
                ], justify='center', align='end'
            )
    return


@app.cell
def _(mo):
    mo.md('### Data Filters')
    return


@app.cell
def _(ans_select, graph_select, hum_select, mo, task_select, test_select):
    mo.hstack(  # <- Added 'return' here
        [mo.vstack(
                [test_select, graph_select, task_select]
            ),
     mo.vstack([hum_select, ans_select])
        ]
    )
    return


@app.cell
def _():
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
        label="Unique graph types",
        bordered=True,
        value=f"{len(filtered_df2['graph_types_ctl'].unique()):,.0f}",
    )
    unique_tasks_og = mo.stat(
        label="Unique tasks (original)",
        bordered=True,
        value=f"{len(filtered_df2['task_types_ctl'].unique()):,.0f}",
    )
    unique_tasks_ctl = mo.stat(
        label="Unique tasks (combined)",
        bordered=True,
        value=f"{len(filtered_df2['task_types_comb'].unique()):,.0f}",
    )
    open_prop = mo.stat(label = "Proportion open-answer", 
                        bordered = True,
                        value = f"{(sum(filtered_df2['open_answer'] == 'open-answer')/len(filtered_df2))*100:,.0f}%")
    unique_images = mo.stat(label = "Unique images", 
                        bordered = True,
                        value = f"{len(filtered_df2['graph_url'].unique()):,.0f}"
                           )
    unique_questions = mo.stat(label = "Unique questions", 
                        bordered = True,
                        value = f"{len(filtered_df2['question'].unique()):,.0f}"
                           )

    return (
        no_tests,
        open_prop,
        total_items,
        unique_graphs,
        unique_images,
        unique_questions,
        unique_tasks_og,
    )
    

@app.cell
def _(concat_dfs_complete, mo):
    ##filters
    default_tests = list(concat_dfs_complete['test_name'].unique())
    default_graphs= list(concat_dfs_complete['graph_types_ctl'].unique())
    default_tasks_ctl= list(concat_dfs_complete['task_types_comb'].unique())
    default_ans_ctl= list(concat_dfs_complete['open_answer'].unique())

    test_select = mo.ui.multiselect(options=concat_dfs_complete['test_name'].unique(),
                                   label = 'Filter tests:',
                                    value = default_tests
                                   )
    graph_select = mo.ui.multiselect(options=concat_dfs_complete['graph_types_ctl'].unique(),
                                    label = 'Filter graphs:',
                                    value = default_graphs)
    task_select = mo.ui.multiselect(options=concat_dfs_complete['task_types_comb'].unique(),
                                    label = 'Filter tasks (comb):',
                                    value = default_tasks_ctl)
    hum_select = mo.ui.multiselect(options=['available', 'unavailable'],
                                    label = 'Filter responses available:',
                                    value = ['available', 'unavailable'])
    ans_select = mo.ui.multiselect(options=concat_dfs_complete['open_answer'].unique(),
                                    label = 'Filter answer type:',
                                    value = default_ans_ctl)
    ##Another one here?
    return ans_select, graph_select, hum_select, task_select, test_select


@app.cell
def _(
    ans_select,
    concat_dfs_complete,
    graph_select,
    hum_select,
    prop_correct,
    task_select,
    test_select,
):
    filtered_df1 = concat_dfs_complete

    if len(test_select.value) > 0:
        filtered_df1 = concat_dfs_complete[concat_dfs_complete['test_name'].isin(test_select.value)]
    else:
        filtered_df1 = concat_dfs_complete
    
    if len(task_select.value)> 0:
        filtered_df1_2 = filtered_df1[filtered_df1['task_types_comb'].isin(task_select.value)]
    else:
        filtered_df1_2 = filtered_df1
    
    if len(graph_select.value) > 0:
        filtered_df2_2 = filtered_df1_2[filtered_df1_2['graph_types_ctl'].isin(graph_select.value)]
    else: 
        filtered_df2_2 = filtered_df1_2 
    
    if len(ans_select.value) > 0:
        filtered_df3_2 = filtered_df2_2[filtered_df2_2['open_answer'].isin(ans_select.value)]
    else: 
        filtered_df3_2 = filtered_df2_2 
    
    if len(hum_select.value) == 1:
        if hum_select.value == ['available']:
            filtered_df2 = filtered_df3_2[filtered_df3_2['prop_correct'].notna()]
        elif hum_select.value == ['unavailable']:
            filtered_df2 = filtered_df3_2[filtered_df3_2['prop_correct'].isna()]
    else:
        filtered_df2 = filtered_df3_2


    start = ['item_ids', 'graph_url', 'open_answer', 'prop_correct', 'question']
    for i in range(1, 15):
        if not filtered_df2[f'answer_{i}'].isna().all():
            start.append(f'answer_{i}')
    gen = ['task_types_ctl', 'graph_types_ctl']
    display = filtered_df2[start + gen]
    return display, filtered_df2


@app.cell
def _(display, mo):
    mo.ui.table(display, selection=None)
    return

@app.cell
def _(filtered_df2, mo):
    csv_download = mo.download(
        data=filtered_df2.to_csv().encode("utf-8"),
        filename="datavis_filtered.csv",
        mimetype="text/csv",
        label="Download filtered data (CSV)",
    )
    mo.hstack([csv_download], justify = 'center')
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
    xaxis = mo.ui.dropdown(options=["Graph type", 'Task type (og)', 'Task type (comb)', "Assessment"], label="X-axis", value = 'Graph type')
    color = mo.ui.dropdown(options=["open-answer", 'Graph type', 'Task type (og)', 'Task type (comb)', 'None'], label="Encoding", value = 'None')
    return color, xaxis


@app.cell
def _(color, graph_select, mo, test_select, xaxis):
    mo.hstack(
        [mo.hstack([
            mo.vstack([test_select, graph_select]),
            mo.vstack([task_select, ans_select])
        ], justify = 'start', align = 'start'),
         mo.vstack(
             [xaxis, color], justify = 'end', align = 'end'
         )]
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
    if xaxis.value == 'Task type (og)':
        chosen_x = 'task_types'
        chosen_title = 'Task type (original)'
    if xaxis.value == 'Task type (comb)':
        chosen_x = 'task_types_comb'
        chosen_title = 'Task type (combined)'

    tooltip_list = []
    tooltip_list.append(alt.Tooltip(chosen_x, title=chosen_title))
    if color.value != 'None':
        color_field_map = {
            "open-answer": ("open_answer", "Open Answer"),
            "Graph type": ("graph_types_ctl", "Graph Type"), 
            "Task type (og)": ("task_types_ctl", "Task Type (original)"),
            "Task type (comb)": ("task_types_comb", "Task Type (combined)")
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
    elif color.value == "Graph type":
        enc_data = "graph_types_ctl"
        encodings["color"] = alt.Color(
            field=enc_data,
            type="nominal",
            title=chosen_title,
            scale=alt.Scale(scheme="paired")
        )
    elif color.value == "Task type (og)":
        enc_data = "task_types_ctl"
        encodings["color"] = alt.Color(
            field=enc_data,
            type="nominal",
            title=chosen_title,
            scale=alt.Scale(scheme="paired")
        )
    elif color.value == "Task type (comb)":
        enc_data = "task_types_comb"
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
def _(bar_chart, display_type, heatmap_final, pie_chart):
    if display_type.value == 'Bar chart':
        display_chart = bar_chart
    elif display_type.value == 'Pie chart':
        display_chart = pie_chart
    else:
        display_chart = heatmap_final
    display_chart
    return


@app.cell
def _():
    ##Descriptive stats

    return


@app.cell
def _(mo):
    display_type = mo.ui.dropdown(options=["Bar chart", 'Pie chart', 'Heatmap'], label="Type of display", value = 'Bar chart')
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
def _(final_chart):
    print("Chart object type:", type(final_chart))
    print("Chart object:", final_chart)

    # Try to convert to dict to see the spec
    try:
        chart_dict = final_chart.to_dict()
        print("Chart dict keys:", chart_dict.keys())
    except Exception as e:
        print("Error converting to dict:", e)
    return


@app.cell
def _(alt, color, filtered_df2, mo, pd, xaxis):
    if xaxis.value == 'Graph type':
        x = 'graph_types_ctl'
        x_title = 'Graph type'
    elif xaxis.value == 'Assessment':
        x = 'test_name'
        x_title = 'Assessment name'
    elif xaxis.value == 'Task type (og)':
        x = 'task_types_ctl' # Note: was 'task_types' - make sure this matches your DataFrame
        x_title = 'Task type (original)'
    elif xaxis.value == 'Task type (comb)':
        x = 'task_types_comb'
        x_title = 'Task type (combined)'
    else:
        # Add a default case
        x = 'graph_types_ctl'
        x_title = 'Graph type'
    if color.value == 'None':
        chosen_y = None
        y_title = 'Frequency'
    elif color.value == "open-answer":
        chosen_y = "open_answer"
        y_title = "Open Answer"
    elif color.value == "Graph type":
        chosen_y = "graph_types_ctl"
        y_title = "Graph Type"
    elif color.value == "Task type (og)":
        chosen_y = "task_types_ctl"
        y_title = "Task Type (Original)"
    elif color.value == "Task type (comb)":
        chosen_y = "task_types_comb"
        y_title = "Task Type (Combined)"
    elif color.value == "Assessment":
        chosen_y = "test_name"
        y_title = "Assessment"
    # Create the chart based on whether we have one or two variables
    if chosen_y is None:
        # Single variable frequency - create a simple bar chart
        freq_data = filtered_df2[x].value_counts().reset_index()
        freq_data.columns = [x, 'count']
   
        final_chart = alt.Chart(freq_data).mark_bar().encode(
            x=alt.X(f'{x}:O', title=x_title, axis=alt.Axis(labelAngle=-45)),
            y=alt.Y('count:Q', title='Count'),
            tooltip=[alt.Tooltip(f'{x}:O', title=x_title),
                    alt.Tooltip('count:Q', title='Count')]
        ).properties(
            width=600,
            height=400,
            title=f'Frequency of {x_title}'
        )
    else:
        # Two variables - create heatmap
        # Create crosstab for the selected variables
        heatmap_data = pd.crosstab(filtered_df2[chosen_y], filtered_df2[x])
   
        # Convert to long format for Altair
        heatmap_long = heatmap_data.reset_index().melt(id_vars=chosen_y,
                                                       var_name=x,
                                                       value_name='freq')
   
        # Handle empty data case
        if len(heatmap_long) == 0:
            print("Warning: No data available for the selected combination")
            final_chart = alt.Chart(pd.DataFrame({'x': [0], 'y': [0], 'text': ['No Data']})).mark_text(
                fontSize=20, color='gray'
            ).encode(
                x=alt.value(300),
                y=alt.value(200),
                text='text:N'
            ).properties(width=600, height=400)
        else:
            # Calculate 95th percentile for robust color scaling
            percentile_95 = heatmap_long['freq'].quantile(0.95)
            max_count = heatmap_long['freq'].max()
       
            # Use percentile_95 or 30, whichever is smaller, for better color scaling
            color_max = min(percentile_95, 30) if percentile_95 > 0 else max_count
       
            # Create base chart
            base = alt.Chart(heatmap_long)
       
            # Create the heatmap rectangles
            rect = base.mark_rect().encode(
                x=alt.X(f'{x}:O',
                        title=x_title,
                        axis=alt.Axis(labelAngle=-45)),
                y=alt.Y(f'{chosen_y}:O',
                        title=y_title),
                color=alt.Color('freq:Q',
                               scale=alt.Scale(scheme='blues',
                                             domain=[0, color_max]),
                               legend=alt.Legend(title='Count')),
                stroke=alt.value('white'),
                strokeWidth=alt.value(1),
                tooltip=[alt.Tooltip(f'{x}:O', title=x_title),
                        alt.Tooltip(f'{chosen_y}:O', title=y_title),
                        alt.Tooltip('freq:Q', title='Count')]
            )
       
            # Create the text overlay
            text = base.mark_text(
                fontSize=12,
                fontWeight='bold'
            ).encode(
                x=alt.X(f'{x}:O'),
                y=alt.Y(f'{chosen_y}:O'),
                text=alt.Text('freq:Q'),
                color=alt.condition(alt.datum.count > 5, alt.value('white'), alt.value('gray'))
            )
       
            # Combine rectangles and text
            final_chart = alt.layer(rect, text).properties(
                width=650,
                height=450,
                title=alt.TitleParams(
                    text=f'{y_title} × {x_title} Distribution',
                    fontSize=16,
                    fontWeight='bold'
                )
            )
    heatmap_final = mo.ui.altair_chart(final_chart)
    return final_chart, heatmap_final


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
    mo.md("""<i> test_name</i>. The name of the assessment. Current assessments in dataframe: ARTIST, merk2020, rodrigues2024, NAAL, CALVI, WAN, VLAT, GGR, BRBF""")
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
    mo.md(""" """)
    return


@app.cell
def _(mo):
    mo.md("""<i> task_types_ctl </i>. Our categorization of the item's cognitive task as understood from viewing the assessment material and matching items with the task coding schema presented in the assessment paper. This may or may not align with the assessment maker's understanding of the item. (i.e. the authors intended an item as "Identify averages", but as this was not in the assessment material, we coded the item as "Identify trends.")""")
    return


@app.cell
def _(mo):
    mo.md("""<i> task_types_comb </i>. A  set of task types that aims to standardize the different task type coding schemas across assessments into one universal schema. This schema was based on task_types_ctl, and not the questions themselves.""")
    return


@app.cell
def _(mo):
    mo.md(
        """
    <pre><i> find_value </i>. The "Find value" task involves identifying values within the graph. It does not differentiate between identifying extrema or multiple values. Examples: "How many of the scores are above 15?", "How many Facebook likes are there for the score of 1.6?"
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
    <pre><i> interpret_data </i>. The "Interpret data" task involves describing trends, distributions, and predictions based on the graph. Examples: "What is the relationship between Drama and Action movies?", "Which referencenorm underlies this table?"
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
    <pre><i> calculate_statistic </i>. The "Calculate statistic" task involves calculating averages, differences, and ranges. Examples: "What is the approximate average life expectancy on this group of planets?", "What was the price range of a barrel of oil in 2015?"
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
    <pre><i> compare_groups </i>. The "Compare groups" task involves comparing one or more groups within the graph and their values, trends, interpretations, or other qualities. Examples: "Which of the treatments contributes to a larger decrease in the percentage of sick patients?", "Which season has more rain, the summer or the spring?"
    """
    )
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
