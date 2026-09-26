# Egocentric Activity Recommendation System

This project explores the development of an egocentric activity recommendation system that recommends activities based on user preferences and contextual information.

## Dataset

We are currently using the **Google Local New York dataset**.

The project uses two files:

- **Review data** — contains user interactions, ratings, review text, timestamps, and place identifiers.
- **Metadata** — contains information about places, including names, categories, locations, average ratings, and number of reviews.

The two datasets can be connected using the `gmap_id` field.

## Project Structure

```text
Activity-Recommendation-System/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   └── 01_data_exploration.ipynb
└── README.md
```

## Dataset Setup

The raw dataset files are not stored in this repository because of their size.

To run the data exploration notebook, download the required Google Local New York files and place them inside:

```text
data/raw/
```

The current files used are:

```text
meta-New_York.json.gz
review-New_York_10 2.json
```

## Current Progress

- Selected the Google Local New York dataset
- Set up the shared project structure
- Loaded the New York place metadata
- Loaded a 100,000-review sample for initial exploration
- Examined available features
- Examined missing values

The 100,000 reviews are currently used only for initial data exploration and have **not** been selected as the final modeling dataset.

## Next Steps

- Explore place categories in the metadata
- Define which categories represent activities
- Create an activity-focused subset
- Analyze user interactions with activity places
- Determine the appropriate review data for modeling