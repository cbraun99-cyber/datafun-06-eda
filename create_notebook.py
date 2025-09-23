import json

# Create the notebook structure
notebook_content = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Amazon Product Reviews - Exploratory Data Analysis\n",
                "## Comprehensive EDA Notebook for Amazon Dataset"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import pandas as pd\n",
                "import numpy as np\n",
                "import matplotlib.pyplot as plt\n",
                "import seaborn as sns\n",
                "import sqlite3\n",
                "from datetime import datetime\n",
                "import warnings\n",
                "warnings.filterwarnings('ignore')\n",
                "\n",
                "# Set up plotting style\n",
                "plt.style.use('seaborn-v0_8')\n",
                "sns.set_palette(\"husl\")\n",
                "%matplotlib inline\n",
                "\n",
                "print(\"✅ Libraries imported successfully!\")"
            ]
        },
        # ... continue with all the other cells from the provided content
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {
                "name": "ipython",
                "version": 3
            },
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.8.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

# Save as .ipynb file
with open('amazon_eda_notebook.ipynb', 'w') as f:
    json.dump(notebook_content, f)

print("✅ Jupyter notebook created successfully!")