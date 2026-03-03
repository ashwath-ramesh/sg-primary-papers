# Content model (draft)

## Entities

### Paper
- id
- title
- level (P1–P6)
- subject (eng/maths/sci/chinese/hcl)
- year
- assessment_type (prelim/eoy/wa1/wa2/wa3/other)
- school (reference)
- has_answers (bool)
- file_format (pdf/zip)
- file_size
- source_url (where it is hosted)
- hosted_by_us (bool)
- checksum (optional)
- tags (array)
- created_at / updated_at

### School
- id
- name
- slug
- type (primary)

### Collection
- id
- title
- description
- criteria (filters snapshot)
- papers (many)

## Derived pages
- Level page = papers filtered by level
- Subject page = papers filtered by subject
- Year page = papers filtered by year
- Paper detail page = single paper + metadata + similar papers

## Data ingestion idea
- Start with **manual curation** for quality.
- Later: semi-automated extraction of metadata from source pages (without copying the actual PDFs).
