#!/bin/sh
set -e

# Fetch latest IDC skill documentation at startup.
# adhoc_data is bind-mounted from the host, so this must happen at runtime rather than during build.
# Fetches SKILL.md and each reference file into their own attachment, which are then
# composed into the final documentation via Jinja templates in the IDC api.yaml spec.

IDC_BASE_URL="https://raw.githubusercontent.com/ImagingDataCommons/idc-claude-skill/${IDC_SKILL_REF:-main}"
IDC_ATTACHMENTS="/jupyter/adhoc_data/specifications/idc/attachments"

echo "Fetching IDC skill documentation (ref: ${IDC_SKILL_REF:-main})..."

if curl -sf "${IDC_BASE_URL}/SKILL.md" -o "${IDC_ATTACHMENTS}/skill.md.tmp"; then
    mv "${IDC_ATTACHMENTS}/skill.md.tmp" "${IDC_ATTACHMENTS}/skill.md"
    echo "  Fetched SKILL.md"
else
    echo "  Warning: could not fetch SKILL.md, using cached version."
fi

for ref in index_tables_guide sql_patterns use_cases clinical_data_guide cloud_storage_guide dicomweb_guide digital_pathology_guide bigquery_guide cli_guide; do
    if curl -sf "${IDC_BASE_URL}/references/${ref}.md" -o "${IDC_ATTACHMENTS}/${ref}.md.tmp"; then
        mv "${IDC_ATTACHMENTS}/${ref}.md.tmp" "${IDC_ATTACHMENTS}/${ref}.md"
        echo "  Fetched references/${ref}.md"
    else
        echo "  Warning: could not fetch references/${ref}.md, using cached version."
        rm -f "${IDC_ATTACHMENTS}/${ref}.md.tmp"
    fi
done

exec python -m beaker_kernel.service.server --ip 0.0.0.0
