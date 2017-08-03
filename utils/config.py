KICKS_TABLE_NAME = 'DailyKicks'
KICKS_METADATA_TABLE_NAME = 'DailyKicksMetadata'

KICKS_PROPERTY_TYPES_FOR_DYNAMO = {
    'Title': 'S',
    'Style': 'S',
    'Color': 'S',
    'Price': 'S',
    'ReleaseDate': 'S',
    'Description': 'S',
    'ImageUrls': 'SS',
    'Site': 'S',
    'Url': 'S'
}

KICKS_METADATA_PROPERTY_TYPES_FOR_DYNAMO = {
    'ReleaseDate': 'S',
    'Count': 'N'
}
