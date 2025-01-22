CRIME_PATTERNS = {
    "drug_crimes": r"DRUG|NARCOTIC",
    "disorderly_conduct": r"HARASS|OBSCENE|THREAT|DISPUT|DISTURB|DISORDER|DRUNK|LIQUOR|NOISY|RESTRAIN|VIOLATION.*ORDER",
    "violent_crimes": r"ASSAULT|MURDER|KIDNAP|INTIMIDAT.*WITNESS|NEGLIG|SUICIDE|AFFRAY|HOMICIDE",
    "property_crimes": r"LARC|VANDAL|BREAK.*ENTER|AUTO.*THEFT|ARSON|BURGL|STOLEN|GRAFFITI|TRESPASS|ROBBERY|PROPERTY",
    "investigation": r"INVEST|MISSING|LOST|SEARCH.*WARRANT|FUGITIVE|BOMB|AIRCRAFT|ESCAPE|EVIDENCE|FOUND|CONFISCATED",
    "disorderly_conduct": r"HARASS|OBSCENE|THREAT|DISPUT|DISTURB|DISORDER|DRUNK|LIQUOR|NOISY|RESTRAIN|VIOLATION.*ORDER",
    "public_safety": r"SICK|FIRE|CHILD.*ASSIST|PROTECT|HAZARD|SUDDEN.*DEATH|DRUG RELATED ILLNESS|RUNAWAY",
    "animal_related": r"ANIMAL|DOG|BITES",
    "legal_violations": r"VIOLATION|WARRANT|PROSTITUTION|TRUANCY",
    "weapons_crimes": r"WEAPON|FIREARM|EXPLOS|BALLIST|BALLISTICS",
    "fraud_crimes": r"FRAUD|FORG|COUNTER|EMBEZZLE|EVAD.*FARE|EXTORT|BLACKMAIL",
    "traffic_related": r"[MV]/V|VEHICLE|OPERAT.*INFLUENCE|OUI|LEAVING SCENE|TOWED",
}

CATEGORY_DISPLAY_NAMES = {
    "violent_crimes": "Violent Crimes",
    "property_crimes": "Property Crimes",
    "investigation": "Investigation",
    "disorderly_conduct": "Disorderly Conduct",
    "public_safety": "Public Safety",
    "animal_related": "Animal Related",
    "legal_violations": "Legal Violations",
    "weapons_crimes": "Weapons Crimes",
    "fraud_crimes": "Fraud & Financial",
    "drug_crimes": "Drug Related",
    "traffic_related": "Traffic Related",
    "other": "Other",
}
