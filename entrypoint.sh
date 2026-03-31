#!/bin/sh
set -e

# Fetch latest IDC skill documentation at startup.
# adhoc_data is bind-mounted from the host, so this must happen at runtime rather than during build.
IDC_SKILL_URL="https://raw.githubusercontent.com/ImagingDataCommons/idc-claude-skill/${IDC_SKILL_REF:-main}/SKILL.md"
IDC_MD_PATH="/jupyter/adhoc_data/specifications/idc/attachments/idc.md"

echo "Fetching IDC skill documentation (ref: ${IDC_SKILL_REF:-main})..."
if curl -sf "${IDC_SKILL_URL}" -o "${IDC_MD_PATH}.tmp"; then
    mv "${IDC_MD_PATH}.tmp" "${IDC_MD_PATH}"
    echo "IDC skill documentation updated."
else
    echo "Warning: could not fetch IDC skill docs, using cached version."
    rm -f "${IDC_MD_PATH}.tmp"
fi

exec python -m beaker_kernel.service.server --ip 0.0.0.0
