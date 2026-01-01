import geopandas as gpd

world = gpd.read_file("../../data/raw/world_boundaries.geojson")

# simplification géométrique
world["geometry"] = world["geometry"].simplify(
    tolerance=0.05,
    preserve_topology=True
)

world.to_file(
    "../../data/cleaned/world_boundaries_simplified.geojson",
    driver="GeoJSON"
)