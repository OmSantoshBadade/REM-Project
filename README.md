# 🏫 Smart Campus Energy Efficiency Dashboard

A data-driven dashboard to monitor and analyze energy consumption, efficiency, and sustainability metrics across campus blocks. Built with Python and Streamlit.

## 🚀 Features

-   **Interactive Dashboard**: Real-time visualization of energy data.
-   **Key Metrics Display**: Track Peak/Non-Peak Energy, Efficiency Scores, Solar Offset, and CO₂ Impact.
-   **Granular Filtering**: Filter data by specific campus blocks and efficiency ranges via the sidebar.
-   **Visual Analytics**:
    -   **Energy Usage Pattern**: Stacked bar charts for Peak vs. Non-Peak energy.
    -   **Efficiency Comparison**: Trends across different blocks.
    -   **Solar vs. Grid**: Scatter plot analyzing dependency relationships.
    -   **Environmental Impact**: CO₂ emissions breakdown.
    -   **Distribution**: Energy consumption share by block.
-   **Insights & Action Plan**: Automated insights and sustainability roadmap suggestions.

## 🛠️ Tech Stack

-   **Python 3.9+**
-   **Streamlit**: For building the web application interface.
-   **Pandas & NumPy**: For data manipulation and processing.
-   **Plotly Express & Graph Objects**: For interactive charts and visualizations.

## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/OmSantoshBadade/REM-Project.git
    cd REM-Project
    ```

2.  **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## ▶️ Usage

1.  **Run the Streamlit app:**
    ```bash
    streamlit run main.py
    ```

2.  **Access the dashboard:**
    Open your web browser and go to `http://localhost:8501`.

## 📂 Project Structure

```
REM-Project/
├── main.py              # Main application script
├── requirements.txt     # Python dependencies
├── .gitignore           # Git ignore file
└── README.md            # Project documentation
```

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or new features.
