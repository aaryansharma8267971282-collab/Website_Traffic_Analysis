import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# WEBSITE TRAFFIC ANALYSIS
# ==========================================

# Load dataset
df = pd.read_csv("traffic_data.csv")

# Convert Date column
df["Date"] = pd.to_datetime(df["Date"])

print("=" * 50)
print("       WEBSITE TRAFFIC ANALYSIS")
print("=" * 50)

# Display dataset
print("\nDataset:")
print(df.to_string(index=False))

# ==========================================
# BASIC STATISTICS
# ==========================================

total_visitors = df["Visitors"].sum()
total_pageviews = df["PageViews"].sum()
total_conversions = df["Conversions"].sum()

print("\n--- Overall Statistics ---")
print("Total Visitors:", total_visitors)
print("Total Page Views:", total_pageviews)
print("Total Conversions:", total_conversions)

# ==========================================
# TRAFFIC SOURCE ANALYSIS
# ==========================================

source_visitors = df.groupby("Source")["Visitors"].sum()

best_source = source_visitors.idxmax()
best_source_visitors = source_visitors.max()

print("\n--- Traffic Source Analysis ---")
print("Best Traffic Source:", best_source)
print("Visitors from Best Source:", best_source_visitors)

# ==========================================
# PAGE ANALYSIS
# ==========================================

page_views = df.groupby("Page")["PageViews"].sum()

most_visited_page = page_views.idxmax()
most_visited_page_views = page_views.max()

print("\n--- Page Analysis ---")
print("Most Visited Page:", most_visited_page)
print("Page Views:", most_visited_page_views)

# ==========================================
# DAILY TRAFFIC ANALYSIS
# ==========================================

highest_day = df.loc[df["Visitors"].idxmax()]
lowest_day = df.loc[df["Visitors"].idxmin()]

print("\n--- Daily Traffic Analysis ---")
print("Highest Traffic Day:", highest_day["Date"].date())
print("Highest Visitors:", highest_day["Visitors"])

print("Lowest Traffic Day:", lowest_day["Date"].date())
print("Lowest Visitors:", lowest_day["Visitors"])

# ==========================================
# ENGAGEMENT ANALYSIS
# ==========================================

average_bounce_rate = df["BounceRate"].mean()
average_session = df["SessionDuration"].mean()

print("\n--- Engagement Analysis ---")
print("Average Bounce Rate:",
      round(average_bounce_rate, 2), "%")

print("Average Session Duration:",
      round(average_session, 2), "seconds")

# ==========================================
# CONVERSION ANALYSIS
# ==========================================

conversion_rate = (total_conversions / total_visitors) * 100

conversion_by_source = df.groupby("Source")["Conversions"].sum()
best_conversion_source = conversion_by_source.idxmax()

print("\n--- Conversion Analysis ---")
print("Overall Conversion Rate:",
      round(conversion_rate, 2), "%")

print("Best Conversion Source:",
      best_conversion_source)

# ==========================================
# GRAPH 1: DAILY VISITORS
# ==========================================

plt.figure(figsize=(10, 5))
plt.plot(df["Date"], df["Visitors"], marker="o")
plt.title("Daily Website Visitors")
plt.xlabel("Date")
plt.ylabel("Visitors")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("daily_visitors.png")
plt.show()

# ==========================================
# GRAPH 2: DAILY PAGE VIEWS
# ==========================================

plt.figure(figsize=(10, 5))
plt.bar(df["Date"].dt.strftime("%Y-%m-%d"), df["PageViews"])
plt.title("Daily Page Views")
plt.xlabel("Date")
plt.ylabel("Page Views")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("daily_pageviews.png")
plt.show()

# ==========================================
# GRAPH 3: VISITORS BY SOURCE
# ==========================================

plt.figure(figsize=(8, 5))
source_visitors.plot(kind="bar")
plt.title("Visitors by Traffic Source")
plt.xlabel("Traffic Source")
plt.ylabel("Visitors")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("visitors_by_source.png")
plt.show()

# ==========================================
# GRAPH 4: CONVERSIONS BY SOURCE
# ==========================================

plt.figure(figsize=(8, 5))
conversion_by_source.plot(kind="bar")
plt.title("Conversions by Traffic Source")
plt.xlabel("Traffic Source")
plt.ylabel("Conversions")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("conversions_by_source.png")
plt.show()

print("\n" + "=" * 50)
print("       ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 50)
print("\nGraphs generated:")
print("1. daily_visitors.png")
print("2. daily_pageviews.png")
print("3. visitors_by_source.png")
print("4. conversions_by_source.png")
