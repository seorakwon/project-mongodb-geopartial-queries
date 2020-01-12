# MongoDB and geopartial queries

The aim of this project is to find the best location where our next office would be located.

Best location to place the office for the company to grow.

1. the companies json was filtered to:
    - include companies with less than 10 years
    - include companies that had all the coordinates listed
    - include companies that had the total money raised
    - exclude companies that had deadpooled
    
2. the json was converted to a dataframe, and cleaned to include only companies that had raised over $ 1M, conveting to json and uploading to mongodb

3. the yelp api was used to retrieve all the starbucks and vegan restaurants in new york, converting the cleaned dataframes to json and then uploading to mongodb as new collections

4. folium was used to plot the 3 collections (companies, starbucks and vegan restaurants)

5. the geoindex created was employed to get the starbucks and restaurants near each company in New York, and the company with the location [40.707954, -74.011114] was chosen as the next location
