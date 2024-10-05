import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import zipfile
from io import BytesIO

@st.cache_data
def load_data_from_zip(zip_file_path, file_name):
    with zipfile.ZipFile(zip_file_path, 'r') as z:
        # Read the specific CSV file from the zip archive
        with z.open(file_name) as f:
            data = pd.read_csv(f)
    return data

# Load data from zip archive
github_data = load_data_from_zip("archive.zip", "github_dataset.csv")
repository_data = load_data_from_zip("archive.zip", "repository_data.csv")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select Dataset", ["GitHub Dataset", "Repository Dataset"])

if page == "GitHub Dataset":
    st.title('GitHub Repositories Dashboard')
    st.write('An interactive dashboard to explore GitHub dataset.')

    # Check for missing columns
    missing_columns = []
    if 'language' not in github_data.columns:
        missing_columns.append('language')
    if 'stars_count' not in github_data.columns:
        missing_columns.append('stars_count')
    if 'forks_count' not in github_data.columns:
        missing_columns.append('forks_count')

    if missing_columns:
        st.error(f"The GitHub dataset is missing the following columns: {', '.join(missing_columns)}")
    else:
        st.subheader('GitHub Dataset Overview')
        st.dataframe(github_data.head())  # Show the first few rows of the dataset
        st.write(f"Total repositories: {len(github_data)}")
        st.write(f"Total languages: {github_data['language'].nunique()}")

        st.sidebar.header("Filters for GitHub Data")
        languages = github_data['language'].unique()
        selected_languages = st.sidebar.multiselect("Select Programming Languages", languages, default=languages)

        filtered_data = github_data[github_data['language'].isin(selected_languages)]
        st.subheader('Visualizations')

        # Histogram of stars count
        fig, ax = plt.subplots()
        sns.histplot(filtered_data['stars_count'], bins=30, kde=True, ax=ax)
        ax.set_title('Distribution of Stars Across Repositories')
        ax.set_xlabel('Number of Stars')
        ax.set_ylabel('Frequency')
        st.pyplot(fig)

        # Pie chart for programming language distribution
        language_count = filtered_data['language'].value_counts()
        fig, ax = plt.subplots()
        ax.pie(language_count, labels=language_count.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.subheader('Programming Language Distribution')
        st.pyplot(fig)

        # Top repositories by stars
        st.subheader('Top Repositories by Stars')
        top_repos = filtered_data.nlargest(10, 'stars_count')
        fig, ax = plt.subplots()
        sns.barplot(data=top_repos, x='stars_count', y='repositories', ax=ax, palette='viridis')
        ax.set_title('Top 10 Repositories by Stars')
        ax.set_xlabel('Number of Stars')
        ax.set_ylabel('Repository Name')
        st.pyplot(fig)

        # Forks vs. Stars scatter plot
        st.subheader('Forks vs. Stars')
        fig, ax = plt.subplots()
        sns.scatterplot(data=filtered_data, x='stars_count', y='forks_count', ax=ax)
        ax.set_title('Forks vs. Stars')
        ax.set_xlabel('Stars')
        ax.set_ylabel('Forks')
        st.pyplot(fig)

elif page == "Repository Dataset":
    st.title('Repository Dataset Dashboard')
    st.write('An interactive dashboard to explore the repository dataset.')

    # Check for missing columns
    missing_columns = []
    if 'primary_language' not in repository_data.columns:
        missing_columns.append('primary_language')
    if 'stars_count' not in repository_data.columns:
        missing_columns.append('stars_count')
    if 'forks_count' not in repository_data.columns:
        missing_columns.append('forks_count')

    if missing_columns:
        st.error(f"The repository dataset is missing the following columns: {', '.join(missing_columns)}")
    else:
        st.subheader('Repository Dataset Overview')
        st.dataframe(repository_data.head())  
        st.write(f"Total repositories: {len(repository_data)}")
        st.write(f"Total primary languages: {repository_data['primary_language'].nunique()}")

        st.sidebar.header("Filters for Repository Data")
        primary_languages = repository_data['primary_language'].unique()
        selected_primary_languages = st.sidebar.multiselect("Select Programming Languages", primary_languages, default=primary_languages)

        filtered_data = repository_data[repository_data['primary_language'].isin(selected_primary_languages)]

        # Visualizations
        st.subheader('Visualizations')

        # Histogram of stars count
        fig, ax = plt.subplots()
        sns.histplot(filtered_data['stars_count'], bins=30, kde=True, ax=ax)
        ax.set_title('Distribution of Stars Across Repositories')
        ax.set_xlabel('Number of Stars')
        ax.set_ylabel('Frequency')
        st.pyplot(fig)

        # Pie chart for primary language distribution
        primary_language_count = filtered_data['primary_language'].value_counts()
        fig, ax = plt.subplots()
        ax.pie(primary_language_count, labels=primary_language_count.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.subheader('Programming Language Distribution')
        st.pyplot(fig)

        # Top repositories by stars
        st.subheader('Top Repositories by Stars')
        top_repos = filtered_data.nlargest(10, 'stars_count')
        fig, ax = plt.subplots()
        sns.barplot(data=top_repos, x='stars_count', y='name', ax=ax, palette='viridis')
        ax.set_title('Top 10 Repositories by Stars')
        ax.set_xlabel('Number of Stars')
        ax.set_ylabel('Repository Name')
        st.pyplot(fig)

        # Forks vs. Stars scatter plot
        st.subheader('Forks vs. Stars')
        fig, ax = plt.subplots()
        sns.scatterplot(data=filtered_data, x='stars_count', y='forks_count', ax=ax)
        ax.set_title('Forks vs. Stars')
        ax.set_xlabel('Stars')
        ax.set_ylabel('Forks')
        st.pyplot(fig)
