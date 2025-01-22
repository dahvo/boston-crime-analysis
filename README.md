# Boston Crime Data Analysis Dashboard

A comprehensive data visualization dashboard built with Streamlit that analyzes crime patterns in Boston, featuring interactive maps, temporal analysis, and detailed crime statistics.

## Features

- **Crime Overview Dashboard**
  - Interactive heatmaps showing crime distributions
  - Temporal analysis (daily, monthly, yearly patterns)
  - District-wise crime breakdown
  - Category-based analysis

- **Shooting Incidents Analysis**
  - Detailed analysis of shooting events
  - Temporal and geographical patterns
  - District-wise statistics

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/dahvo/boston-crime-analysis.git
cd boston-crime-analysis
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run src/home.py
```

## 📁 Project Structure

```
streamlit-app/
├── src/
│   ├── home.py                     # Application entry point
│   ├── pages/
│   │   ├── 1_Crime_Overview.py     # Crime overview dashboard
│   │   └── 2_Shooting_Analysis.py  # Shooting incidents analysis
│   └── utils/
│       └── helpers.py              # Utility functions
├── data/                           # Data directory
├── requirements.txt
└── README.md
```

## 🛠️ Built With

- [Streamlit](https://streamlit.io/) - The web framework used
- [Plotly](https://plotly.com/) - Interactive visualizations
- [Folium](https://python-visualization.github.io/folium/) - Geographical visualizations
- [Pandas](https://pandas.pydata.org/) - Data manipulation

## Data Sources
This analysis uses official crime incident reports from the Boston Police Department's crime incident reports database. \
Provided by: [Analyze Boston](https://data.boston.gov/) \
Dataset: [Crime Incident Reports Dataset](https://data.boston.gov/dataset/crime-incident-reports-august-2015-to-date-source-new-system)  

The dataset includes:
- Incident details and classifications
- Geographic coordinates
- Temporal information
- District assignments

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License

## Acknowledgments

- Boston Police Department and Analyze Boston for providing the data
- Streamlit team for the amazing framework

## 📫 Contact

If you have any questions or feedback, please open an issue or contact [your contact info].