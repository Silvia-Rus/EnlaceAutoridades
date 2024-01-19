SELECT 
     CONCAT('<a href=\"/cgi-bin/koha/catalogue/detail.pl?biblionumber=', biblionumber, '\">', biblionumber, '</a>' ) AS biblionumber
     /* 
     
     ExtractValue(metadata, '//datafield[@tag="650"]/subfield[@code="a"]') as '650$a', 
     ExtractValue(metadata, '//datafield[@tag="650"]/subfield[@code="9"]') as '650$9',
     */
FROM biblio_metadata
WHERE
    (length(ExtractValue(metadata, '//datafield[@tag="650"]/subfield[@code="a"]')) != 0
    AND 
    length(ExtractValue(metadata, '//datafield[@tag="650"]/subfield[@code="9"]')) = 0)
