class TextConverter:
    """
    Handles conversion of text responses into numerical values.
    """

    categorical_mappings = [
        {
            "": 0, "true": 1, "false": 0, "no": 0, "yes": 1,
            "No": 0, "Yes": 1
        },
        {
            "Grade 0-8": 1, "Grade 9": 2, "Grade 10": 3, "Grade 11": 4,
            "Grade 12 or equivalent": 5, "OAC or Grade 13": 6,
            "Some college": 7, "Some university": 8, "Some apprenticeship": 9,
            "Certificate of Apprenticeship": 10, "Journeyperson": 11,
            "Certificate/Diploma": 12, "Bachelor's degree": 13,
            "Post graduate": 14
        },
        {
            "Renting-private": 1, "Renting-subsidized": 2,
            "Boarding or lodging": 3, "Homeowner": 4,
            "Living with family/friend": 5, "Institution": 6,
            "Temporary second residence": 7, "Band-owned home": 8,
            "Homeless or transient": 9, "Emergency hostel": 10
        },
        {
            "No Source of Income": 1, "Employment Insurance": 2,
            "Workplace Safety and Insurance Board": 3,
            "Ontario Works applied or receiving": 4,
            "Ontario Disability Support Program applied or receiving": 5,
            "Dependent of someone receiving OW or ODSP": 6, "Crown Ward": 7,
            "Employment": 8, "Self-Employment": 9, "Other (specify)": 10
        }
    ]

    @classmethod
    def convert_text(cls, text_data: str):
        """Convert text answers into numerical values using predefined mappings."""
        for category in cls.categorical_mappings:
            if text_data in category:
                return category[text_data]
        return int(text_data) if text_data.isnumeric() else text_data