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
def _(mo, pd):
    notebook_path = mo.notebook_location()
    data_dir = f'{notebook_path}/public'
    csv_file = 'ARTIST.csv'
    path = f'{data_dir}/{csv_file}'
    
    mo.md(f"""
    ### 🔍 URL Construction Debug
    - **notebook_path:** `{notebook_path}`
    - **data_dir:** `{data_dir}`
    - **final_path:** `{path}`
    - **path_type:** `{type(path)}`
    """)
    return ()


if __name__ == "__main__":
    app.run()
