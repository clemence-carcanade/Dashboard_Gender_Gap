import requests
from pathlib import Path
import time

class ProjectDataDownloader:    
    def __init__(self, max_retries: int = 3, timeout: int = 30):
        self.max_retries = max_retries
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def download_file(self, url: str, output_path: Path, description: str = "") -> bool:
        print(f"\nDownloading: {description}")
        
        for attempt in range(1, self.max_retries + 1):
            try:
                response = self.session.get(url, timeout=self.timeout, stream=True)
                response.raise_for_status()
                
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

                if output_path.exists() and output_path.stat().st_size > 0:
                    print(f"OK - {output_path}")
                    return True
                
            except Exception as e:
                if attempt == self.max_retries:
                    print(f"ERROR - {description}: {e}")
                else:
                    time.sleep(2 ** attempt)
        
        return False
    
    def download_csv_from_xlsx_page(self, page_url: str, output_path: Path, 
                                   description: str, figure_number: str, sheet_name=0) -> bool:
        page_id = page_url.split('/')[5].split('?')[0]
        xlsx_url = f"https://www.insee.fr/fr/statistiques/fichier/{page_id}/IREF_FH22-{figure_number}.xlsx"
        
        print(f"\nDownloading: {description}")
        
        temp_xlsx = output_path.parent / f"temp_{output_path.stem}.xlsx"
        
        try:
            response = self.session.get(xlsx_url, timeout=self.timeout)
            response.raise_for_status()
            
            temp_xlsx.parent.mkdir(parents=True, exist_ok=True)
            with open(temp_xlsx, 'wb') as f:
                f.write(response.content)
            
            import pandas as pd
            df = pd.read_excel(temp_xlsx, sheet_name=sheet_name, header=None)
            df.to_csv(output_path, index=False, header=False, encoding='utf-8')
            temp_xlsx.unlink()
            
            if output_path.exists() and output_path.stat().st_size > 0:
                print(f"OK - {output_path}")
                return True
            
        except Exception as e:
            print(f"ERROR - {description}: {e}")
            if temp_xlsx.exists():
                temp_xlsx.unlink()
            return False
    

def download_all_project_data():    
    print("="*70)
    print("DOWNLOADING DATA")
    print("="*70)
    
    downloader = ProjectDataDownloader()
    results = {}
    
    stem_success = downloader.download_file(
        url='https://ourworldindata.org/grapher/share-graduates-stem-female.csv',
        output_path=Path('../../data/raw/world_women_in_stem.csv'),
        description='World Women in STEM'
    )
    results['world_women_in_stem'] = stem_success
    time.sleep(1)

    boundaries_success = downloader.download_file(
        url='https://raw.githubusercontent.com/datasets/geo-boundaries-world-110m/master/countries.geojson',
        output_path=Path('../../data/raw/world_boundaries.geojson'),
        description='World Boundaries'
    )
    results['world_boundaries'] = boundaries_success
    time.sleep(1)
    
    feuille1_success = downloader.download_csv_from_xlsx_page(
        page_url='https://www.insee.fr/fr/statistiques/6047727?sommaire=6047805',
        output_path=Path('../../data/raw/fr_research_women_feuille1.csv'),
        description='INSEE Research Women Licence',
        figure_number='F7',
        sheet_name=1
    )
    results['fr_research_feuille1'] = feuille1_success
    time.sleep(1)
    
    feuille2_success = downloader.download_csv_from_xlsx_page(
        page_url='https://www.insee.fr/fr/statistiques/6047727?sommaire=6047805',
        output_path=Path('../../data/raw/fr_research_women_feuille2.csv'),
        description='INSEE Research Women Doctorat',
        figure_number='F7',
        sheet_name=2
    )
    results['fr_research_feuille2'] = feuille2_success
    time.sleep(1)
    
    departments_success = downloader.download_file(
        url='https://france-geojson.gregoiredavid.fr/repo/departements.geojson',
        output_path=Path('../../data/raw/fr_departments.geojson'),
        description='France Departements'
    )
    results['fr_departments'] = departments_success
    
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
    print("FILES TO DOWNLOAD BY HAND")
    print("="*70)
    print("\n1. world_GII.csv")
    print("   https://www.kaggle.com/code/anoopjohny/gender-inequality-study")
    print("   Place here: ../../data/raw/world_GII.csv")
    
    print("\n2. fr_regions_gender_inequality.xls")
    print("   https://www.insee.fr/fr/statistiques/2513786")
    print("   Place here: ../../data/raw/fr_regions_gender_inequality.xls")
    print("\n" + "="*70)
    
    return results


def main():
    download_all_project_data()


if __name__ == "__main__":
    main()