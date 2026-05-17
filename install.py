import subprocess
import sys
import os
import subprocess
import time

def install_packages():
    """Install all required packages"""
    packages = [
        'pandas', 'numpy', 'matplotlib', 'seaborn', 
        'requests', 'plotly', 'streamlit', 'wordcloud'
    ]
    
    print("Installing packages...")
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])
            print(f"✅ {package}")
        except:
            print(f"⚠️  {package} (skipped)")
    print("✅ Installation complete!")

def main():
    print("🎬 NETFLIX DASHBOARD - AUTO SETUP")
    print("=" * 50)
    
    # Install packages
    install_packages()
    
    # Create analysis script
    analysis_code = '''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import io
import warnings
warnings.filterwarnings("ignore")

print("🔄 Downloading Netflix data...")
response = requests.get("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2021/2021-04-20/netflix_titles.csv")
df = pd.read_csv(io.StringIO(response.text))
df.to_csv("netflix_titles.csv", index=False)
print(f"✅ Data saved! {df.shape}")

# Clean data
df_clean = df.copy()
df_clean["date_added"] = pd.to_datetime(df_clean["date_added"], errors="coerce")
df_clean["country"] = df_clean["country"].fillna("Unknown")
df_clean["year_added"] = df_clean["date_added"].dt.year
df_clean.drop_duplicates(inplace=True)

print(f"✅ Cleaned: {df_clean.shape}")

# Dashboard
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle("🎬 NETFLIX DASHBOARD", fontsize=20, fontweight="bold")

# 1. Content Type
df_clean["type"].value_counts().plot(kind="pie", ax=axes[0,0], autopct="%1.1f%%")
axes[0,0].set_title("Movies vs TV")

# 2. Over Time
years = df_clean["year_added"].value_counts().sort_index()
axes[0,1].plot(years.index, years.values, "o-")
axes[0,1].set_title("Added Over Time")

# 3. Top Countries
top_countries = df_clean["country"].value_counts().head(10)
axes[0,2].barh(top_countries.index, top_countries.values)
axes[0,2].set_title("Top Countries")

# 4. Top Genres
genres = df_clean["listed_in"].str.split(", ", expand=True).stack().value_counts().head(10)
axes[1,0].barh(genres.index, genres.values)
axes[1,0].set_title("Top Genres")

# 5. Ratings
df_clean["rating"].value_counts().plot(kind="bar", ax=axes[1,1])
axes[1,1].set_title("Ratings")
axes[1,1].tick_params(axis="x", rotation=45)

# 6. Duration
movies = df_clean[df_clean["type"]=="Movie"]
durations = movies["duration"].str.extract(r"(\\d+)").astype(float)[0].dropna()
axes[1,2].hist(durations, bins=25, color="gold")
axes[1,2].set_title("Movie Duration")

plt.tight_layout()
plt.savefig("netflix_dashboard.png", dpi=300, bbox_inches="tight")
plt.show(block=False)
plt.close()

print("🎉 Dashboard saved as netflix_dashboard.png!")
print(f"📊 Stats: {len(df_clean):,} titles, {len(movies):,} movies")
'''
    
    with open("netflix_analysis.py", "w") as f:
        f.write(analysis_code)
    
    print("\n📁 Files created:")
    print("   📊 netflix_analysis.py")
    print("   📈 netflix_dashboard.png")
    print("   💾 netflix_titles.csv")
    
    print("\n🚀 Run: python netflix_analysis.py")
    print("🌐 Web: streamlit run netflix_web.py")

if __name__ == "__main__":
    main()