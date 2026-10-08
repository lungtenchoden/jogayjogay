# data.py

DZONGKHAGS = [
    "Bumthang", "Chukha", "Dagana", "Gasa", "Haa", "Lhuentse",
    "Mongar", "Paro", "Pema Gatshel", "Punakha", "Samdrup Jongkhar",
    "Samtse", "Sarpang", "Thimphu", "Trashigang", "Trashi Yangtse",
    "Trongsa", "Tsirang", "Wangdue Phodrang", "Zhemgang",
]

VEHICLE_TYPES = [
    "Maruti Alto", "Maruti WagonR", "Maruti Swift", "Maruti Dzire",
    "Hyundai i10", "Hyundai Accent", "Hyundai Santro",
    "Toyota Corolla", "Toyota Prius", "Honda City", "Honda Civic",
    "Suzuki Celerio", "Kia Picanto", "Other",
]

STATUSES = ["Active", "Review", "Inactive"]


TAXI_RECORDS = [
    ("TX001", "BP-1-A1234", "Thimphu",          "Maruti Alto",     "2023-05-12", "Active"),
    ("TX002", "BP-2-B5678", "Paro",             "Hyundai i10",     "2022-11-03", "Active"),
    ("TX003", "BP-3-C9012", "Chukha",           "Maruti WagonR",   "2023-08-20", "Active"),
    ("TX004", "BP-4-D2468", "Punakha",          "Toyota Corolla",  "2023-02-14", "Active"),
    ("TX005", "BP-5-E1357", "Wangdue Phodrang", "Hyundai Accent",  "2022-09-28", "Review"),
    ("TX006", "BP-6-F8642", "Samtse",           "Maruti Swift",    "2023-10-05", "Active"),
    ("TX007", "BP-1-G7834", "Phuentsholing",    "Suzuki Celerio",  "2024-01-18", "Active"),
    ("TX008", "BP-7-H4921", "Trashigang",       "Honda City",      "2023-06-30", "Active"),
    ("TX009", "BP-8-J5810", "Mongar",           "Maruti Dzire",    "2022-12-11", "Active"),
]

TRIP_RECORDS = [
    ("Thimphu",          "Paro",             "2024-01-15", "45"),
    ("Phuentsholing",    "Thimphu",          "2024-01-16", "72"),
    ("Paro",             "Punakha",          "2024-01-17", "28"),
    ("Thimphu",          "Wangdue Phodrang", "2024-01-18", "33"),
    ("Mongar",           "Trashigang",       "2024-02-06", "19"),
    ("Samtse",           "Phuentsholing",    "2024-02-18", "56"),
    ("Bumthang",         "Thimphu",          "2024-03-02", "24"),
    ("Punakha",          "Thimphu",          "2024-03-11", "61"),
    ("Chukha",           "Paro",             "2024-03-15", "38"),
    ("Trashigang",       "Mongar",           "2024-03-19", "16"),
    ("Thimphu",          "Haa",              "2024-01-20", "22"),
    ("Haa",              "Paro",             "2024-01-21", "18"),
    ("Paro",             "Haa",              "2024-01-22", "15"),
    ("Thimphu",          "Gasa",             "2024-02-01", "12"),
    ("Gasa",             "Punakha",          "2024-02-02", "14"),
    ("Punakha",          "Gasa",             "2024-02-03", "10"),
    ("Sarpang",          "Tsirang",          "2024-02-10", "26"),
    ("Tsirang",          "Dagana",           "2024-02-11", "19"),
    ("Dagana",           "Tsirang",          "2024-02-12", "21"),
    ("Samdrup Jongkhar", "Trashigang",       "2024-03-20", "17"),
]

ANALYSIS_DATA = [
    ("Thimphu",          "82", "510", "412", "High"),
    ("Paro",             "46", "188", "245", "High"),
    ("Phuentsholing",    "31", "326", "211", "High"),
    ("Punakha",          "24", "96",  "128", "Medium"),
    ("Wangdue Phodrang", "18", "72",  "89",  "Medium"),
    ("Bumthang",         "7",  "18",  "24",  "Low"),
]

PARKING_ZONES = [
    ("Bumthang Taxi Stand",         "Bumthang dzongkhag",         "7"),
    ("Chukha Taxi Stand",           "Chukha dzongkhag",           "14"),
    ("Dagana Taxi Stand",           "Dagana dzongkhag",           "8"),
    ("Gasa Taxi Stand",             "Gasa dzongkhag",             "4"),
    ("Haa Taxi Stand",              "Haa dzongkhag",              "5"),
    ("Lhuentse Taxi Stand",         "Lhuentse dzongkhag",         "6"),
    ("Mongar Taxi Stand",           "Mongar dzongkhag",           "9"),
    ("Paro Taxi Stand",             "Paro dzongkhag",             "18"),
    ("Pema Gatshel Taxi Stand",     "Pema Gatshel dzongkhag",     "7"),
    ("Punakha Taxi Stand",          "Punakha dzongkhag",          "12"),
    ("Samdrup Jongkhar Taxi Stand", "Samdrup Jongkhar dzongkhag", "15"),
    ("Samtse Taxi Stand",           "Samtse dzongkhag",           "11"),
    ("Sarpang Taxi Stand",          "Sarpang dzongkhag",          "13"),
    ("Thimphu Taxi Stand",          "Thimphu dzongkhag",          "34"),
    ("Trashigang Taxi Stand",       "Trashigang dzongkhag",       "10"),
    ("Trashi Yangtse Taxi Stand",   "Trashi Yangtse dzongkhag",   "6"),
    ("Trongsa Taxi Stand",          "Trongsa dzongkhag",          "7"),
    ("Tsirang Taxi Stand",          "Tsirang dzongkhag",          "8"),
    ("Wangdue Phodrang Taxi Stand", "Wangdue Phodrang dzongkhag", "11"),
    ("Zhemgang Taxi Stand",         "Zhemgang dzongkhag",         "5"),
]

DRIVERS = [
    {"name":"Sonam Dorji","license":"DL-2024-0456","contact":"17123456","status":"On Trip","vehicle":"Maruti Alto","plate":"BP-1-A1234","dzongkhag":"Thimphu","trips":"320","rating":"4.6 / 5","cancellations":"5","activity":[("21 Mar 2024","Thimphu → Paro","On Trip"),("20 Mar 2024","Thimphu → Punakha","Completed"),("19 Mar 2024","Paro → Thimphu","Completed")]},
    {"name":"Karma Wangchuk","license":"DL-2023-0112","contact":"17654321","status":"Available","vehicle":"Hyundai i10","plate":"BP-2-B5678","dzongkhag":"Paro","trips":"245","rating":"4.8 / 5","cancellations":"2","activity":[("21 Mar 2024","Paro → Thimphu","Completed"),("20 Mar 2024","Paro → Haa","Completed"),("18 Mar 2024","Thimphu → Paro","Completed")]},
    {"name":"Pema Tshering","license":"DL-2022-0789","contact":"17234567","status":"On Trip","vehicle":"Maruti WagonR","plate":"BP-3-C9012","dzongkhag":"Chukha","trips":"180","rating":"4.4 / 5","cancellations":"8","activity":[("21 Mar 2024","Chukha → Thimphu","On Trip"),("20 Mar 2024","Chukha → Paro","Completed"),("17 Mar 2024","Thimphu → Chukha","Completed")]},
    {"name":"Tshering Dorji","license":"DL-2021-0345","contact":"17876543","status":"Available","vehicle":"Toyota Corolla","plate":"BP-4-D2468","dzongkhag":"Punakha","trips":"412","rating":"4.9 / 5","cancellations":"1","activity":[("21 Mar 2024","Punakha → Thimphu","Completed"),("20 Mar 2024","Thimphu → Punakha","Completed"),("19 Mar 2024","Punakha → Paro","Completed")]},
    {"name":"Ugyen Namgay","license":"DL-2024-0098","contact":"17456789","status":"Review","vehicle":"Hyundai Accent","plate":"BP-5-E1357","dzongkhag":"Wangdue Phodrang","trips":"95","rating":"4.2 / 5","cancellations":"12","activity":[("20 Mar 2024","Wangdue → Thimphu","Completed"),("15 Mar 2024","Thimphu → Wangdue","Completed")]},
    {"name":"Jigme Thinley","license":"DL-2023-0672","contact":"17567890","status":"Available","vehicle":"Maruti Swift","plate":"BP-6-F8642","dzongkhag":"Samtse","trips":"210","rating":"4.7 / 5","cancellations":"3","activity":[("21 Mar 2024","Samtse → Thimphu","Completed"),("20 Mar 2024","Thimphu → Samtse","Completed"),("19 Mar 2024","Samtse → Paro","Completed")]},
    {"name":"Sangay Wangmo","license":"DL-2024-0511","contact":"17678901","status":"On Trip","vehicle":"Suzuki Celerio","plate":"BP-1-G7834","dzongkhag":"Phuentsholing","trips":"150","rating":"4.5 / 5","cancellations":"4","activity":[("21 Mar 2024","Phuentsholing → Thimphu","On Trip"),("20 Mar 2024","Thimphu → Phuentsholing","Completed")]},
    {"name":"Tenzin Norbu","license":"DL-2022-0912","contact":"17789012","status":"Available","vehicle":"Honda City","plate":"BP-7-H4921","dzongkhag":"Trashigang","trips":"275","rating":"4.6 / 5","cancellations":"4","activity":[("21 Mar 2024","Trashigang → Mongar","Completed"),("20 Mar 2024","Mongar → Trashigang","Completed"),("18 Mar 2024","Trashigang → Thimphu","Completed")]},
    {"name":"Chimi Wangmo","license":"DL-2023-0445","contact":"17890123","status":"On Trip","vehicle":"Maruti Dzire","plate":"BP-8-J5810","dzongkhag":"Mongar","trips":"198","rating":"4.5 / 5","cancellations":"6","activity":[("21 Mar 2024","Mongar → Trashigang","On Trip"),("20 Mar 2024","Trashigang → Mongar","Completed")]},
    {"name":"Karma Chophel","license":"DL-2021-0234","contact":"17901234","status":"Available","vehicle":"Toyota Prius","plate":"BP-9-K1234","dzongkhag":"Bumthang","trips":"340","rating":"4.9 / 5","cancellations":"0","activity":[("21 Mar 2024","Bumthang → Trongsa","Completed"),("19 Mar 2024","Trongsa → Bumthang","Completed"),("17 Mar 2024","Bumthang → Thimphu","Completed")]},
    {"name":"Kinley Dem","license":"DL-2024-0678","contact":"17012345","status":"Review","vehicle":"Hyundai Santro","plate":"BP-1-L5678","dzongkhag":"Samdrup Jongkhar","trips":"78","rating":"4.0 / 5","cancellations":"14","activity":[("18 Mar 2024","Samdrup Jongkhar → Trashigang","Completed"),("15 Mar 2024","Trashigang → Samdrup Jongkhar","Completed")]},
    {"name":"Pema Lhamo","license":"DL-2023-0556","contact":"17123498","status":"Available","vehicle":"Maruti Alto","plate":"BP-2-M9012","dzongkhag":"Haa","trips":"142","rating":"4.7 / 5","cancellations":"2","activity":[("21 Mar 2024","Haa → Paro","Completed"),("19 Mar 2024","Paro → Haa","Completed"),("17 Mar 2024","Haa → Thimphu","Completed")]},
    {"name":"Sonam Choden","license":"DL-2022-0389","contact":"17234987","status":"On Trip","vehicle":"Hyundai i10","plate":"BP-3-N3456","dzongkhag":"Dagana","trips":"156","rating":"4.4 / 5","cancellations":"7","activity":[("21 Mar 2024","Dagana → Tsirang","On Trip"),("19 Mar 2024","Tsirang → Dagana","Completed")]},
    {"name":"Namgay Wangdi","license":"DL-2021-0789","contact":"17345678","status":"Available","vehicle":"Toyota Corolla","plate":"BP-4-P7890","dzongkhag":"Sarpang","trips":"289","rating":"4.8 / 5","cancellations":"1","activity":[("21 Mar 2024","Sarpang → Tsirang","Completed"),("20 Mar 2024","Tsirang → Sarpang","Completed"),("18 Mar 2024","Sarpang → Thimphu","Completed")]},
    {"name":"Rinchen Zangmo","license":"DL-2023-0823","contact":"17456712","status":"On Trip","vehicle":"Maruti WagonR","plate":"BP-5-Q2345","dzongkhag":"Zhemgang","trips":"112","rating":"4.3 / 5","cancellations":"9","activity":[("21 Mar 2024","Zhemgang → Trongsa","On Trip"),("19 Mar 2024","Trongsa → Zhemgang","Completed")]},
    {"name":"Tashi Phuntsho","license":"DL-2022-0145","contact":"17567823","status":"Available","vehicle":"Honda Civic","plate":"BP-6-R6789","dzongkhag":"Trongsa","trips":"334","rating":"4.9 / 5","cancellations":"0","activity":[("21 Mar 2024","Trongsa → Bumthang","Completed"),("20 Mar 2024","Bumthang → Trongsa","Completed"),("19 Mar 2024","Trongsa → Thimphu","Completed")]},
    {"name":"Dechen Wangmo","license":"DL-2024-0298","contact":"17678934","status":"Review","vehicle":"Kia Picanto","plate":"BP-7-S1234","dzongkhag":"Gasa","trips":"56","rating":"3.9 / 5","cancellations":"11","activity":[("15 Mar 2024","Gasa → Punakha","Completed"),("12 Mar 2024","Punakha → Gasa","Completed")]},
    {"name":"Leki Dorji","license":"DL-2023-0176","contact":"17789045","status":"Available","vehicle":"Suzuki Celerio","plate":"BP-8-T5678","dzongkhag":"Lhuentse","trips":"167","rating":"4.6 / 5","cancellations":"3","activity":[("21 Mar 2024","Lhuentse → Mongar","Completed"),("19 Mar 2024","Mongar → Lhuentse","Completed")]},
    {"name":"Kinley Wangchuk","license":"DL-2022-0523","contact":"17890156","status":"On Trip","vehicle":"Maruti Swift","plate":"BP-9-U9012","dzongkhag":"Pema Gatshel","trips":"143","rating":"4.5 / 5","cancellations":"5","activity":[("21 Mar 2024","Pema Gatshel → Trashigang","On Trip"),("20 Mar 2024","Trashigang → Pema Gatshel","Completed")]},
    {"name":"Yeshi Lhamo","license":"DL-2023-0987","contact":"17901267","status":"Available","vehicle":"Hyundai Accent","plate":"BP-1-V3456","dzongkhag":"Tsirang","trips":"201","rating":"4.7 / 5","cancellations":"2","activity":[("21 Mar 2024","Tsirang → Sarpang","Completed"),("20 Mar 2024","Sarpang → Tsirang","Completed"),("18 Mar 2024","Tsirang → Thimphu","Completed")]},
    {"name":"Tandin Wangmo","license":"DL-2021-0654","contact":"17012378","status":"Available","vehicle":"Toyota Corolla","plate":"BP-2-W7890","dzongkhag":"Chukha","trips":"398","rating":"4.9 / 5","cancellations":"0","activity":[("21 Mar 2024","Chukha → Thimphu","Completed"),("20 Mar 2024","Thimphu → Chukha","Completed"),("19 Mar 2024","Chukha → Paro","Completed")]},
    {"name":"Nima Tshering","license":"DL-2024-0389","contact":"17123489","status":"Review","vehicle":"Maruti Dzire","plate":"BP-3-X1234","dzongkhag":"Trashi Yangtse","trips":"67","rating":"4.1 / 5","cancellations":"10","activity":[("15 Mar 2024","Trashi Yangtse → Trashigang","Completed"),("12 Mar 2024","Trashigang → Trashi Yangtse","Completed")]},
    {"name":"Phub Dorji","license":"DL-2023-0745","contact":"17234590","status":"Available","vehicle":"Honda City","plate":"BP-4-Y5678","dzongkhag":"Punakha","trips":"256","rating":"4.8 / 5","cancellations":"1","activity":[("21 Mar 2024","Punakha → Wangdue","Completed"),("20 Mar 2024","Wangdue → Punakha","Completed"),("18 Mar 2024","Punakha → Thimphu","Completed")]},
    {"name":"Choki Wangmo","license":"DL-2022-0812","contact":"17345601","status":"On Trip","vehicle":"Suzuki Celerio","plate":"BP-5-Z9012","dzongkhag":"Wangdue Phodrang","trips":"188","rating":"4.6 / 5","cancellations":"4","activity":[("21 Mar 2024","Wangdue → Punakha","On Trip"),("20 Mar 2024","Punakha → Wangdue","Completed")]},
]

REGISTRATION_BARS = [
    ("Thimphu",       74),
    ("Paro",          52),
    ("Phuentsholing", 42),
    ("Chukha",        34),
    ("Punakha",       27),
]

MONTHLY_TRIPS = [
    ("Oct", 40), ("Nov", 55), ("Dec", 48),
    ("Jan", 72), ("Feb", 68), ("Mar", 90),
]

FLEET_SHARE = [
    ("Sedan",     42, "#3d7eb8"),
    ("Hatchback", 35, "#d9a441"),
    ("SUV",       23, "#7aa5cc"),
]