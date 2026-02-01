import pandas as pd
import geopandas as gpd
from pathlib import Path


def clean_regions_data():
    print("\nCleaning France regions data...")
    
    xls_path = Path("../../data/raw/fr_regions_gender_inequality.xls")
    output_path = Path("../../data/cleaned/fr_regions_gender_inequality_cleaned.csv")
    
    xls = pd.ExcelFile(xls_path)
    
    df_education = pd.read_excel(xls, sheet_name=3, header=None)
    df_salaire = pd.read_excel(xls, sheet_name=5, header=None)
    
    skip_entries = {
        '976 - Mayotte',
        'OM – DROM y compris Mayotte',
        'FR – France'
    }
    
    education_data = {}
    for i in range(5, len(df_education)):
        code_region = df_education.iloc[i, 1]
        education = df_education.iloc[i, 5]
        
        if pd.notna(code_region):
            code_region_str = str(code_region).strip()
            
            if code_region_str in skip_entries:
                continue
            
            if code_region_str == 'OM – DROM hors Mayotte':
                code = 'OM'
                region = 'DROM hors Mayotte'
            elif ' - ' in code_region_str:
                parts = code_region_str.split(' - ', 1)
                code = parts[0].strip()
                region = parts[1].strip()
            else:
                continue
            
            education_val = education if pd.notna(education) and str(education) != 'nondiffusé' else ''
            education_data[code] = {'Region': region, 'Education_Gap_2021': education_val}
    
    salaire_data = {}
    for i in range(5, len(df_salaire)):
        code_region = df_salaire.iloc[i, 1]
        salaire = df_salaire.iloc[i, 6]
        
        if pd.notna(code_region):
            code_region_str = str(code_region).strip()
            
            if code_region_str in skip_entries:
                continue
            
            if code_region_str == 'OM – DROM hors Mayotte':
                code = 'OM'
            elif ' - ' in code_region_str:
                parts = code_region_str.split(' - ', 1)
                code = parts[0].strip()
            else:
                continue
            
            salaire_val = salaire if pd.notna(salaire) and str(salaire) != 'nondiffusé' else ''
            salaire_data[code] = salaire_val
    
    all_codes = sorted(set(education_data.keys()) | set(salaire_data.keys()), 
                       key=lambda x: (len(x), x))
    
    data = []
    for code in all_codes:
        edu_info = education_data.get(code, {})
        region = edu_info.get('Region', '')
        education_val = edu_info.get('Education_Gap_2021', '')
        salaire_val = salaire_data.get(code, '')
        
        if education_val != '' and education_val != 'nondiffusé':
            try:
                education_val = round(float(education_val), 1)
            except (ValueError, TypeError):
                pass
        
        if salaire_val != '' and salaire_val != 'nondiffusé':
            try:
                salaire_val = round(float(salaire_val), 1)
            except (ValueError, TypeError):
                pass
        
        data.append({
            'Code': code,
            'Region': region,
            'Education_Gap_2021': education_val,
            'Salary_Gap_2022': salaire_val
        })
    
    df_cleaned = pd.DataFrame(data)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_cleaned.to_csv(output_path, index=False)
    
    print(f"OK - {output_path}")
    return True


def simplify_world_boundaries():
    print("\nSimplifying world boundaries...")
    
    input_path = Path("../../data/raw/world_boundaries.geojson")
    output_path = Path("../../data/cleaned/world_boundaries_simplified.geojson")
    
    world = gpd.read_file(input_path)
    
    if 'iso_a3' in world.columns and 'iso3' not in world.columns:
        world = world.rename(columns={'iso_a3': 'iso3'})
    
    if 'name' not in world.columns and 'admin' in world.columns:
        world = world.rename(columns={'admin': 'name'})
    
    world["geometry"] = world["geometry"].simplify(
        tolerance=0.05,
        preserve_topology=True
    )
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    world.to_file(output_path, driver="GeoJSON")
    
    print(f"OK - {output_path}")
    return True


def main():
    print("="*70)
    print("CLEANING DATA")
    print("="*70)
    results = {}
    
    try:
        results['regions'] = clean_regions_data()
    except Exception as e:
        print(f"ERROR - Regions: {e}")
        results['regions'] = False
    
    try:
        results['boundaries'] = simplify_world_boundaries()
    except Exception as e:
        print(f"ERROR - Boundaries: {e}")
        results['boundaries'] = False
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    for name, success in results.items():
        status = "OK" if success else "FAILED"
        print(f"{status:10} - {name}")
    
    success_count = sum(1 for s in results.values() if s)
    total_count = len(results)
    print(f"\nSuccess level: {success_count}/{total_count}")
    print("\n" + "="*70)


if __name__ == "__main__":
    main()