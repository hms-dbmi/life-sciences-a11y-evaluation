import pandas as pd

def data_load():
    TIME_STAMP_FOLDER = 'JAN-10-2024'
    A11Y_COLORS = {
        'd': '#56B4E9',
        'j': '#CC79A7',
        'g': '#009E73'
    }
    A11Y_CATEGORIES = [
        ('d', 'data-portal', 'Data Portals', '#56B4E9'),
        ('j', 'journal-portal', 'Journal Websites',  '#CC79A7'),
        ('g', 'gov', "US Government Websites", '#009E73'),
    ]
    AGG_CATEGORIES = [
        '', 
        '_agg', 
        '_agg_alt'
    ]
    TOP_CNT = 10 # for printing top websites
    
    issues_df = pd.DataFrame()
    for (id, category, title, color) in A11Y_CATEGORIES:
        _ = pd.read_csv(
            f'../javascript/{TIME_STAMP_FOLDER}/{category}_a11y_issues.csv',
            header=None,
            names=['id', 'impact', 'description']
        )
        issues_df = pd.concat([issues_df, _])
    issues_df.drop_duplicates(inplace=True)
    issues_df.to_csv(f'../javascript/{TIME_STAMP_FOLDER}/all_a11y_issues.csv', index=False)
    issues_df.id.unique().tolist()
    
    ISSUE_IDS = issues_df.id.tolist()
    
    issues_df[issues_df.description.str.contains('alternate')]
    ALT_ISSUE_IDS = issues_df[issues_df.description.str.contains('alternate')].id.tolist()
    ALT_ISSUE_IDS
    
    df = {}
    
    for (id, category, title, color) in A11Y_CATEGORIES:
        df[id] = pd.read_csv(
            f'../javascript/{TIME_STAMP_FOLDER}/{category}_a11y_results.csv',
            header=None,
            names=['page_id', 'issue_id', 'violations', 'passes']
        )
    
    df['d']
    
    nei = pd.read_csv(
        f'../javascript/{TIME_STAMP_FOLDER}/nei-data-portal_a11y_results.csv',
        header=None,
        names=['page_id', 'issue_id', 'violations', 'passes']
    )
    df['d'] = pd.concat([df['d'], nei])
    df['d']
    
    nih = pd.read_csv(
        f'../javascript/{TIME_STAMP_FOLDER}/nih-data-portal_a11y_results.csv',
        header=None,
        names=['page_id', 'issue_id', 'violations', 'passes']
    )
    df['d'] = pd.concat([df['d'], nih])
    df['d']
    
    for (id, category, title, color) in A11Y_CATEGORIES:
        _ = df[id].copy()
        
        # To group by page_id, uncomment the following lines
        # _df.drop(['issue_id'], axis=1, inplace=True)
        # _df = _df.groupby(['page_id']).sum().reset_index()
        
        _['total_checks'] = _['violations'] + _['passes']
        _['failure_rate'] = _['violations'] / _['total_checks']
        df[id] = _
    df['d'].head(5)
    
    for (id, category, title, color) in A11Y_CATEGORIES:
        _ = df[id].copy()
        
        # CHECKING...
        # _ = _[_.issue_id != 'region']
    
        _.drop(['issue_id'], axis=1, inplace=True)
        _ = _.groupby(['page_id']).sum().reset_index()
        _['failure_rate'] = _['violations'] / _['total_checks']
        df[id + '_agg'] = _
    df['d_agg'].head(5)
    
    for (id, category, title, color) in A11Y_CATEGORIES:
        _ = df[id].copy()
        _ = _[_['issue_id'].isin(ALT_ISSUE_IDS)]
        _.drop(['issue_id'], axis=1, inplace=True)
        _ = _.groupby(['page_id']).sum().reset_index()
        _['failure_rate'] = _['violations'] / _['total_checks']
        df[id + '_agg_alt'] = _
    df['d_agg_alt'].head(5)
    
    for (id, category, title, color) in A11Y_CATEGORIES:
        if(category == 'gov'):
            continue
    
        for ver in ['', '_agg', '_agg_alt']:
            _ = df[id + ver].copy()
            _['id'] = _['page_id'].apply(lambda x: x.split('_')[0])
            meta = pd.read_csv(f'../output/Nov-21-2023/{category}_metadata.csv')
    
            _['id'] = _['id'].astype(str)
            meta['id'] = meta['id'].astype(str)
    
            _ = _.merge(meta, left_on='id', right_on='id', how='left')
    
            # Some data cleaning
            if id == 'd':
                # Group NIH 
                NIH_INSTS = [
                    'National Center for Biotechnology Information',
                    'National Cancer Institute',
                    'National Heart, Lung, and Blood Institute',
                    'National Center for Advancing Translational Sciences',
                    'National Institutes of Health',
                    'National Human Genome Research Institute',
                    'National Institute of Environmental Health Sciences',
                    'National Library of Medicine',
                    'National Institute of Standards and Technology',
                    'National Institute of Health',
                    'National Institute on Aging',
                    'National Institute of Neurological Disorders & Stroke',
                    'National Institute of Child Health and Human Development',
                    'National Eye Institute', # none found
                    'National Institute of Allergy and Infectious Diseases',
                    'National Institute of Arthritis and Musculoskeletal and Skin Diseases'
                ]
                # _.loc[_.host_institution.isin(NIH_INSTS), 'host_institution'] = 'National Institutes of Health'
            # elif id == 'jp':
                # _.loc[_.publisher.str.contains('Elsevier') == True, 'publisher'] = 'Elsevier'
                # _.loc[_.publisher.str.contains('Springer') == True, 'publisher'] = 'Springer-related'
    
            df[id + ver] = _
    df['j'].head(5)
    
    for (id, category, title, color) in A11Y_CATEGORIES:
        for ver in ['', '_agg', '_agg_alt']:
            df[id + ver]['page_type'] = df[id + ver].page_id.apply(lambda x: x.split('_')[1] if '_' in str(x) else 'home')
    df['d_agg'].head(5)
    
    for var in AGG_CATEGORIES:
        gov_meta = pd.read_csv(f'../javascript/{TIME_STAMP_FOLDER}/gov_pages.csv', sep=',', header=None, names=['name', 'type', 'inst', 'desc', 'city', 'state', 'blank'])
        gov_meta.reset_index(inplace=True)
        df['g' + var] = df['g' + var].merge(gov_meta, left_on='page_id', right_on='index', how='left')
        df['g' + var]['url'] = df['g' + var]['name']
    
    for var in AGG_CATEGORIES:
        _meta = pd.read_csv(f'../javascript/{TIME_STAMP_FOLDER}/nei-data-portal_pages.csv')
        _meta.set_index('page_id', inplace=True)
        
        _ = df['d' + var].copy()
        _.set_index('page_id', inplace=True)
        _[_.isnull()] = _meta
        _.reset_index(inplace=True)
        df['d' + var] = _
    
    for var in AGG_CATEGORIES:
        _meta = pd.read_csv(f'../javascript/{TIME_STAMP_FOLDER}/nih-data-portal_pages.csv')
        _meta['short_name'] = _meta.Repository_Name
        _meta['host_institution'] = 'National Institutes of Health'
        _meta['country'] = 'United States'
        _meta.set_index('page_id', inplace=True)
    
        _ = df['d' + var].copy()
        _.set_index('page_id', inplace=True)
        _[_.isnull()] = _meta
        _.reset_index(inplace=True)
        df['d' + var] = _
    
    for var in AGG_CATEGORIES:
        df['d' + var]['title'] = df['d' + var]['short_name']
        df['g' + var]['title'] = df['g' + var]['name']
    
    def rename_countries(x: str):
        if x == 'Korea Republic of' or x == 'Korea, Republic of':
            return 'South Korea'
        elif x == 'Korea, Democratic People"S Republic of' or x == 'Korea, Democratic People':
            return 'North Korea'
        elif x == 'Russian Federation':
            return 'Russia'
        elif x == 'Iran, Islamic Republic Of':
            return 'Iran'
        else:
            return x
        
    for var in AGG_CATEGORIES:
        df['d' + var].country = df['d' + var].country.apply(lambda x: rename_countries(x))
        df['j' + var].country = df['j' + var].country.apply(lambda x: rename_countries(x))
    
    # Print
    # countries = [x for x in list(set(df['d'].country.tolist() + df['j'].country.unique().tolist())) if str(x) != 'nan']
    # countries.sort()
    # countries
    
    continent_country_map = pd.read_csv('https://raw.githubusercontent.com/dbouquin/IS_608/master/NanosatDB_munging/Countries-Continents.csv')
    continent_country_map = continent_country_map.rename(columns={
        'Country': 'country',
        'Continent': 'continent'
    })
    
    def clean_country_names(x):
        if x == 'US':
            return 'United States'
        elif x == 'Korea, South':
            return 'South Korea' 
        elif x == 'Korea, North':
            return 'North Korea'
        elif x == 'Russian Federation':
            return 'Russia'
        elif x == 'Samoa':
            return 'American Samoa'
        elif x == 'Vietnam':
            return 'Viet Nam'
        elif x == 'Serbia':
            return 'Serbia and Montenegro'
        else:
            return x
    
    continent_country_map.country = continent_country_map.country.apply(lambda x: clean_country_names(x))
    
    for id in ['d', 'j']:
        for var in AGG_CATEGORIES:
            _ = df[id + var].copy()
            _ = _.merge(continent_country_map, left_on='country', right_on='country', how='left')
            _.loc[_.continent.isnull(), 'continent'] = _[_.continent.isnull()].country.apply(lambda x: 'Europe' if x == 'Czech Republic' or x == 'Guadeloupe' else x)
    
            # Some manual correction
            _.continent = _.continent.apply(lambda x: 'Europe' if x == 'Serbia' else 'Asia' if x == 'Taiwan' or x == 'Hong Kong' or x == 'Brunei Darussalam' else 'North America' if x == 'Puerto Rico' else x)
            
            df[id + var] = _
    # _[_.continent.isnull()].country.unique().tolist()
    _.head(5)
    
    _ = pd.read_csv(f'../javascript/{TIME_STAMP_FOLDER}/Publishers of Journal Portals - Sheet1.csv')
    _.Cleaned.fillna(_.Original, inplace=True)
    mapping = dict(zip(_.Original, _.Cleaned))
    
    for var in AGG_CATEGORIES:
        df['j' + var].publisher = df['j' + var].publisher.apply(lambda x: mapping[x] if x in mapping else x)
    df['j'].head(5)
    
    _ = pd.read_csv(f'../javascript/{TIME_STAMP_FOLDER}/Filtering of Journals - Sheet1.csv')
    _.rename(columns={'If filter "v", otherwise empty': 'is_filter'}, inplace=True)
    _.is_filter = _.is_filter.apply(lambda x: True if x == 'v' else False)
    mapping = dict(zip(_.Title, _.is_filter))
    
    for var in AGG_CATEGORIES:
        df['j' + var]['is_filter'] = df['j' + var].title.apply(lambda x: mapping[x] if x in mapping else False)
        df['j' + var] = df['j' + var][df['j' + var].is_filter == False]
    df['j'].head(5)
    
    # What are the unique areas?
    combined_list = [area.split('; ') for area in df['j'].areas.unique().tolist()]
    flat_list = [item for sublist in combined_list for item in sublist]
    flat_list = list(set(flat_list))
    flat_list.sort()
    # flat_list
    
    keep = [
        'Agricultural and Biological Sciences',
        'Biochemistry, Genetics and Molecular Biology',
        'Dentistry',
        'Health Professions',
        'Immunology and Microbiology',
        'Medicine',
        'Multidisciplinary',
        'Neuroscience',
        'Nursing',
        'Pharmacology, Toxicology and Pharmaceutics',
        'Psychology'
    ]
    def isKeeping(areas: str):
        if areas == 'Multidisciplinary' or any([k in areas for k in keep]):
            return True
        return False
    
    for var in AGG_CATEGORIES:    
        df['j' + var]['is_keep'] = df['j' + var].areas.apply(lambda x: isKeeping(x))
        df['j' + var] = df['j' + var][df['j' + var].is_keep == True]
        df['j' + var].drop(['is_keep'], axis=1, inplace=True)
        df['j' + var]
    
    def remove_unkeep_areas(areas):
            area_list = areas.split("; ")
            filtered_list = list(filter(lambda area: area in keep, area_list))
            
            # if len(filtered_list) >= 2 and 'Medicine' in filtered_list:
            #     filtered_list.remove('Medicine')
            # if len(filtered_list) >= 2 and 'Multidisciplinary' in filtered_list:
            #     filtered_list.remove('Multidisciplinary')
            # if len(filtered_list) >= 2 and 'Health Professions' in filtered_list:
            #     filtered_list.remove('Health Professions')
            # if len(filtered_list) >= 2 and 'Nursing' in filtered_list:
            #     filtered_list = ['Nursing']
                
            return "; ".join(filtered_list)
        
    for var in AGG_CATEGORIES:
        # _ = df['j' + var].copy()
        df['j' + var]['areas_filtered'] = df['j' + var].areas.apply(lambda areas: remove_unkeep_areas(areas))
        
    
    # _['is_multi_area'] = _.area.apply(lambda x: len(list(x.split("; "))) > 1)
    # test = "Agricultural and Biological Sciences; Business, Management and Accounting; Economics, Econometrics and Finance"
    # "; ".join(list(filter(lambda x: x in keep, test.split("; "))))
    # unique_area = _.area.unique().tolist()
    # unique_area = filter(lambda x: '; ' in x, unique_area)
    # list(unique_area)
    # print(len(_[_.is_multi_area]))
    
    # What are the unique categories?
    combined_list = [area.split('; ') for area in df['j'].categories.unique().tolist()]
    flat_list = [item for sublist in combined_list for item in sublist]
    flat_list = list(set(flat_list))
    flat_list.sort()
    flat_list = [item.split(' (')[0] for item in flat_list]
    set(flat_list)
    
    categories_to_keep = [
     'Advanced and Specialized Nursing',
     'Aging',
     'Agricultural and Biological Sciences',
     'Agronomy and Crop Science',
     'Anatomy',
     'Anesthesiology and Pain Medicine',
     'Animal Science and Zoology',
     'Anthropology',
     'Applied Microbiology and Biotechnology',
     'Applied Psychology',
     'Assessment and Diagnosis',
     'Atmospheric Science',
     'Atomic and Molecular Physics, and Optics',
     'Behavioral Neuroscience',
     'Biochemistry',
     'Biochemistry, Genetics and Molecular Biology',
     'Bioengineering',
     'Biological Psychiatry',
     'Biomaterials',
     'Biomedical Engineering',
     'Biophysics',
     'Biotechnology',
     'Cancer Research',
     'Cardiology and Cardiovascular Medicine',
     'Catalysis',
     'Cell Biology',
     'Cellular and Molecular Neuroscience',
     'Chemical Health and Safety',
     'Chiropractics',
     'Clinical Biochemistry',
     'Clinical Psychology',
     'Cognitive Neuroscience',
     'Complementary and Alternative Medicine',
     'Complementary and Manual Therapy',
     'Critical Care Nursing',
     'Critical Care and Intensive Care Medicine',
     'Demography',
     'Dental Assisting',
     'Dental Hygiene',
     'Dentistry',
     'Dermatology',
     'Development',
     'Developmental Biology',
     'Developmental Neuroscience',
     'Developmental and Educational Psychology',
     'Drug Discovery',
     'Drug Guides',
     'Emergency Medical Services',
     'Emergency Medicine',
     'Emergency Nursing',
     'Endocrine and Autonomic Systems',
     'Endocrinology',
     'Endocrinology, Diabetes and Metabolism',
     'Epidemiology',
     'Experimental and Cognitive Psychology',
     'Food Animals',
     'Food Science',
     'Gastroenterology',
     'Gender Studies',
     'Genetics',
     'Health',
     'Health Informatics',
     'Health Information Management',
     'Health Policy',
     'Health Professions',
     'Health, Toxicology and Mutagenesis',
     'Hematology',
     'Hepatology',
     'Histology',
     'Horticulture',
     'Human Factors and Ergonomics',
     'Immunology',
     'Immunology and Allergy',
     'Immunology and Microbiology',
     'Infectious Diseases',
     'Insect Science',
     'Internal Medicine',
     'Life-span and Life-course Studies',
     'Linguistics and Language',
     'Maternity and Midwifery',
     'Medical Assisting and Transcription',
     'Medical Laboratory Technology',
     'Medical Terminology',
     'Medical and Surgical Nursing',
     'Medicine',
     'Microbiology',
     'Molecular Biology',
     'Molecular Medicine',
     'Multidisciplinary',
     'Nanoscience and Nanotechnology',
     'Nephrology',
     'Neurology',
     'Neuropsychology and Physiological Psychology',
     'Neuroscience',
     'Nurse Assisting',
     'Nursing',
     'Nutrition and Dietetics',
     'Obstetrics and Gynecology',
     'Occupational Therapy',
     'Oncology',
     'Ophthalmology',
     'Optometry',
     'Oral Surgery',
     'Organic Chemistry',
     'Orthodontics',
     'Orthopedics and Sports Medicine',
     'Otorhinolaryngology',
     'Paleontology',
     'Parasitology',
     'Pathology and Forensic Medicine',
     'Pediatrics',
     'Pediatrics, Perinatology and Child Health',
     'Periodontics',
     'Pharmaceutical Science',
     'Pharmacology',
     'Pharmacology, Toxicology and Pharmaceutics',
     'Pharmacy',
     'Physical Therapy, Sports Therapy and Rehabilitation',
     'Physiology',
     'Plant Science',
     'Podiatry',
     'Process Chemistry and Technology',
     'Psychiatry and Mental Health',
     'Psychology',
     'Public Health, Environmental and Occupational Health',
     'Pulmonary and Respiratory Medicine',
     'Radiation',
     'Radiological and Ultrasound Technology',
     'Radiology, Nuclear Medicine and Imaging',
     'Rehabilitation',
     'Reproductive Medicine',
     'Respiratory Care',
     'Rheumatology',
     'Sensory Systems',
     'Social Psychology',
     'Speech and Hearing',
     'Structural Biology',
     'Surgery',
     'Tourism, Leisure and Hospitality Management',
     'Toxicology',
     'Transplantation',
     'Urology',
     'Veterinary',
     'Virology'
    ]
    
    def remove_unkeep_areas(areas):
            area_list = areas.split("; ")
            area_list = [a.split(' (')[0] for a in area_list]
            filtered_list = list(filter(lambda area: area in categories_to_keep, area_list))
            
            # if len(filtered_list) >= 2 and 'Medicine' in filtered_list:
            #     filtered_list.remove('Medicine')
            # if len(filtered_list) >= 2 and 'Multidisciplinary' in filtered_list:
            #     filtered_list.remove('Multidisciplinary')
            # if len(filtered_list) >= 2 and 'Health Professions' in filtered_list:
            #     filtered_list.remove('Health Professions')
            # if len(filtered_list) >= 2 and 'Nursing' in filtered_list:
            #     filtered_list = ['Nursing']
                
            return "; ".join(filtered_list)
        
    for var in AGG_CATEGORIES:
        # _ = df['j' + var].copy()
        df['j' + var]['categories_filtered'] = df['j' + var].categories.apply(lambda areas: remove_unkeep_areas(areas))
        
    
    # _['is_multi_area'] = _.area.apply(lambda x: len(list(x.split("; "))) > 1)
    # test = "Agricultural and Biological Sciences; Business, Management and Accounting; Economics, Econometrics and Finance"
    # "; ".join(list(filter(lambda x: x in keep, test.split("; "))))
    # unique_area = _.area.unique().tolist()
    # unique_area = filter(lambda x: '; ' in x, unique_area)
    # list(unique_area)
    # print(len(_[_.is_multi_area]))
    return df