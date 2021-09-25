import pandas as pd
from sklearn.preprocessing import StandardScaler
def floor_recognition(s):
    if s[0] == "-":
        return -1 * floor_recognition(s[1:])
    if s.isdigit():
        return int(s)
    elif "подв" in s:
        return -1
    elif "цок" in s:
        return 0
    else:
        return -100
    
def floor_parser(row):
    #"<=0",  "2-5", "6-10", "11-20", "20<"
    result = [0, 0, 0, 0, 0]
    r = str(row).lower()
    for stop_word in [".0", "этажа", "этаж", "эт", " ", "-й"]:
        r = r.replace(stop_word, "")
    r = r.replace(".", ",").split(",")[0]
    floor = floor_recognition(r)
    if floor < -99:
        return pd.Series(result)
    elif floor < 1:
        result[0] = 1
    elif floor <=5:
        result[1] = 1
    elif floor <= 10:
        result[2] = 1
    elif floor <= 20:
        result[3] = 1
    else:
        result[4] = 1
    return pd.Series(result)
def a(row):
    aa = str(row)
    bb = russian_states[ russian_states["region"] == aa] ["state"]
    if len(bb) > 0:
        return bb.item()
    else:
        print ([aa])
def parse_data_train(df, russian_states):
    df[["floor<0", "floor<=5", "floor<=10", "floor<=20", "floor>20"]] = df["floor"].apply(floor_parser)
    df["state"] = df["region"].apply(a)
    X = df[["lat", "lng", "floor<0", "floor<=5", "floor<=10", "floor<=20", "floor>20", "realty_type", "total_square", "state", "price_type", "osm_amenity_points_in_0.005", "osm_building_points_in_0.005", "osm_catering_points_in_0.005", "osm_city_closest_dist", "osm_city_nearest_population", "osm_crossing_points_in_0.005", "osm_culture_points_in_0.005", "osm_finance_points_in_0.005", "osm_healthcare_points_in_0.005", "osm_historic_points_in_0.005", "osm_hotels_points_in_0.005", "osm_leisure_points_in_0.005", "osm_offices_points_in_0.005", "osm_shops_points_in_0.005", "osm_subway_closest_dist", "osm_train_stop_closest_dist", "osm_transport_stop_closest_dist", "osm_transport_stop_points_in_0.005", "reform_count_of_houses_500", "reform_house_population_500", "reform_mean_floor_count_500", "reform_mean_year_building_500"]]
    configuration = {}
    configuration["reform_house_population_500_mean"] = X["reform_house_population_500"].mean()
    configuration["reform_mean_floor_count_500_mean"] = X["reform_mean_floor_count_500"].mean()
    configuration["reform_mean_year_building_500_mean"] = X["reform_mean_year_building_500"].mean()
    configuration["osm_city_nearest_population_mean"] = X["osm_city_nearest_population"].mean()
    X["reform_house_population_500"].fillna( configuration["reform_house_population_500_mean"], inplace = True)
    X["reform_mean_floor_count_500"].fillna( configuration["reform_mean_floor_count_500_mean"], inplace = True)
    X["reform_mean_year_building_500"].fillna( configuration["reform_mean_year_building_500_mean"], inplace = True)
    X["osm_city_nearest_population"].fillna( configuration["osm_city_nearest_population_mean"], inplace = True)
    X = pd.get_dummies(X, drop_first=True) 
    configuration["scaler"] = StandardScaler()
    X = configuration["scaler"].fit_transform(X)
    return X, configuration
def parse_data(df, russian_states, configuration):
    df[["floor<0", "floor<=5", "floor<=10", "floor<=20", "floor>20"]] = df["floor"].apply(floor_parser)
    df["state"] = df["region"].apply(a)
    X = df[["lat", "lng", "floor<0", "floor<=5", "floor<=10", "floor<=20", "floor>20", "realty_type", "total_square", "state", "price_type", "osm_amenity_points_in_0.005", "osm_building_points_in_0.005", "osm_catering_points_in_0.005", "osm_city_closest_dist", "osm_city_nearest_population", "osm_crossing_points_in_0.005", "osm_culture_points_in_0.005", "osm_finance_points_in_0.005", "osm_healthcare_points_in_0.005", "osm_historic_points_in_0.005", "osm_hotels_points_in_0.005", "osm_leisure_points_in_0.005", "osm_offices_points_in_0.005", "osm_shops_points_in_0.005", "osm_subway_closest_dist", "osm_train_stop_closest_dist", "osm_transport_stop_closest_dist", "osm_transport_stop_points_in_0.005", "reform_count_of_houses_500", "reform_house_population_500", "reform_mean_floor_count_500", "reform_mean_year_building_500"]]
    X["reform_house_population_500"].fillna( configuration["reform_house_population_500_mean"], inplace = True)
    X["reform_mean_floor_count_500"].fillna( configuration["reform_mean_floor_count_500_mean"], inplace = True)
    X["reform_mean_year_building_500"].fillna( configuration["reform_mean_year_building_500_mean"], inplace = True)
    X["osm_city_nearest_population"].fillna( configuration["osm_city_nearest_population_mean"], inplace = True)
    X = pd.get_dummies(X, drop_first=True) 
    X = configuration["scaler"].transform(X)
    return X, configuration