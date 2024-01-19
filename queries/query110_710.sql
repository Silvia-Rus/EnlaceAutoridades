SELECT 
     CONCAT('<a href=\"/cgi-bin/koha/catalogue/detail.pl?biblionumber=', biblionumber, '\">', biblionumber, '</a>' ) AS biblionumber
     /* 
     ,
     ExtractValue(metadata, '//datafield[@tag="110"]/subfield[@code="a"]') as '110$a', 
     ExtractValue(metadata, '//datafield[@tag="110"]/subfield[@code="9"]') as '110$9',
     
     ExtractValue(metadata, '//datafield[@tag="710"]/subfield[@code="a"]') as '710$a', 
     ExtractValue(metadata, '//datafield[@tag="710"]/subfield[@code="9"]') as '710$9' 
     */
FROM biblio_metadata
WHERE

    (length(ExtractValue(metadata, '//datafield[@tag="110"]/subfield[@code="a"]')) != 0
    AND 
    length(ExtractValue(metadata, '//datafield[@tag="110"]/subfield[@code="9"]')) = 0)
     OR
    (length(ExtractValue(metadata, '//datafield[@tag="710"]/subfield[@code="a"]')) != 0
    AND 
    length(ExtractValue(metadata, '//datafield[@tag="710"]/subfield[@code="9"]')) = 0)
